from rlgym.communication import Message, CommunicationHandler
from rlgym.utils import math, common_values
from rlgym.utils.obs_builders import ObsBuilder
import numpy as np

class BotRecorder(object):
    def __init__(self, comm_handler):
        self.comm_handler = comm_handler
        self.orange_score = 0
        self.bot_actions = []
        self.bot_obs = []
        self.prev_action = [0 for _ in range(8)]

        self.last_touch = None
        self.player = None

    def step(self, state):
        obs = self.build_obs_for_player(state)
        if len(obs) != 62:
            print("INVALID OBS ENCOUNTERED BY BOT RECORDER:",obs)
            return

        self.request()
        self.bot_obs.append(obs)
        if state.orange_score != self.orange_score and state.last_touch == self.player.car_id:
            self.orange_score = state.orange_score
            self.save()
            self.reset()

    def reset(self):
        self.bot_obs = []
        self.bot_actions = []
        self.prev_action = [0 for _ in range(8)]

    def request(self):
        self.comm_handler.send_message(header=Message.RLGYM_REQUEST_LAST_BOT_INPUT_MESSAGE_HEADER)
        response = self.comm_handler.receive_message(header=Message.RLGYM_LAST_BOT_INPUT_MESSAGE_HEADER)
        self.bot_actions.append(response.body)
        self.prev_action = [float(x.strip()) for x in response.body.split(" ")]

    def save(self):
        print("Bot Recorder Saving", len(self.bot_actions))
        with open("data/recordings/val_recording.txt", 'a') as f:
            for state, action in zip(self.bot_obs, self.bot_actions):
                s = ''.join(["{} ".format(x) for x in state])
                #a = ["{} ".format(x) for x in action]
                line = "{}|{}\n".format(s[:-1], action)#a[:-1])
                f.write(line)
            f.write("END EPISODE\n")

    def build_obs_for_player(self, state):
        if self.player is None:
            for p in state.players:
                if p.team_num == common_values.ORANGE_TEAM:
                    self.player = p
                    break
        player = self.player
        if player is None:
            return []

        prev_actions = self.prev_action
        if prev_actions is None:
            print("ATTEMPTED TO BUILD RHOBOT OBS WITH NO PREV ACTIONS ARGUMENT!")
            raise ArithmeticError

        players = state.players
        if player.team_num == common_values.ORANGE_TEAM:
            player_car = player.inverted_car_data
            ball = state.inv_ball
        else:
            player_car = player.car_data
            ball = state.ball

        ob = [arg for arg in prev_actions]
        ob.append(int(player.has_flip))
        ob.append(int(player.boost_amount))
        ob.append(int(player.on_ground))

        ob += player_car.position
        ob += player_car.orientation
        ob += [np.sin(arg) for arg in player_car.orientation]
        ob += [np.cos(arg) for arg in player_car.orientation]
        ob += player_car.linear_velocity
        ob += player_car.angular_velocity

        ob += ball.position
        ob += ball.linear_velocity
        ob += ball.angular_velocity

        ob += common_values.ORANGE_GOAL_CENTER
        ob += common_values.BLUE_GOAL_CENTER

        for other in players:
            if other.car_id == player.car_id:
                continue

            if other.team_num == common_values.BLUE_TEAM and player.team_num == other.team_num:
                car_data = other.car_data
            else:
                car_data = other.inverted_car_data

            # TODO: COMMENT THIS OUT
            #car_data = ObsBuilder.get_random_physics_state()

            ob += car_data.position
            ob += car_data.orientation
            ob += [np.sin(arg) for arg in car_data.orientation]
            ob += [np.cos(arg) for arg in car_data.orientation]
            ob += car_data.linear_velocity
            ob += car_data.angular_velocity

        return ob