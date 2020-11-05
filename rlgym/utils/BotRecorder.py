from rlgym.communication import Message, CommunicationHandler
from rlgym.utils import Math, CommonValues
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
        if len(obs) != 52:
            print(obs)
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
        print("Saving", len(self.bot_actions))
        with open("data/recordings/bot_recording_4.txt", 'a') as f:
            for state, action in zip(self.bot_obs, self.bot_actions):
                s = ''.join(["{} ".format(x) for x in state])
                #a = ["{} ".format(x) for x in action]
                line = "{}|{}\n".format(s[:-1], action)#a[:-1])
                f.write(line)
            f.write("END EPISODE\n")

    def build_obs_for_player(self, state):
        player = self.player
        if player is None:
            for p in state.players:
                if p.team_num == CommonValues.ORANGE_TEAM:
                    self.player = p
                    player = p
                    break

        player_car = player.inverted_car_data
        ball = state.inv_ball

        ob = [arg for arg in self.prev_action]

        ob.append(int(player.has_flip))
        ob.append(int(player.boost_amount))
        ob.append(int(player.on_ground))

        ob += player_car.serialize()
        ob += ball.position
        ob += ball.linear_velocity
        ob += ball.angular_velocity

        ob += CommonValues.ORANGE_GOAL_CENTER
        ob += CommonValues.BLUE_GOAL_CENTER

        for other in state.players:
            if other.car_id == player.car_id:
                continue

            if other.team_num == CommonValues.ORANGE_TEAM:
                car_data = other.car_data
            else:
                car_data = other.inverted_car_data

            ob += car_data.serialize()

        return ob