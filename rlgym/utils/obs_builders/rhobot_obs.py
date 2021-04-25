from rlgym.utils.obs_builders import ObsBuilder
from rlgym.utils import common_values, math
import numpy as np


class RhobotObs(ObsBuilder):
    def __init__(self):
        super().__init__()

    def reset(self, initial_state):
        pass

    def build_obs(self, player, state, prev_action) -> np.ndarray:
        if prev_action is None:
            print("!ATTEMPTED TO BUILD RHOBOT OBS WITH NO PREV ACTIONS ARGUMENT!")
            raise AssertionError

        players = state.players
        if player.team_num == common_values.ORANGE_TEAM:
            player_car = player.inverted_car_data
            ball = state.inverted_ball
        else:
            player_car = player.car_data
            ball = state.ball

        ob = []
        ob.append(prev_action)
        ob.append([int(player.has_flip),
                   player.boost_amount,
                   int(player.on_ground)])

        ob.append(player_car.position)
        ob.append(player_car.euler_angles())
        ob.append(np.sin(player_car.euler_angles()))
        ob.append(np.cos(player_car.euler_angles()))
        yaw = player_car.yaw()
        angle_between_bot_and_target = np.arctan2(ball.position[1] - player_car.position[1],
                                                  ball.position[0] - player_car.position[0])
        
        angle_front_to_target = angle_between_bot_and_target - yaw
        ob.append([angle_front_to_target])
        ob.append(player_car.linear_velocity)
        ob.append(player_car.angular_velocity)

        ob.append(ball.position)
        ob.append(ball.linear_velocity)
        ob.append(ball.angular_velocity)

        ob.append(common_values.ORANGE_GOAL_CENTER)
        ob.append(common_values.BLUE_GOAL_CENTER)

        pb_dist = math.vecmag(math.get_dist(player_car.position, ball.position))
        ob.append([pb_dist])

        # Since we invert the car and ball data when the agent is in the Orange team
        # the "Orange Goal" is always the enemy goal
        pg_dist = math.vecmag(math.get_dist(player_car.position, common_values.ORANGE_GOAL_CENTER))
        ob.append([pg_dist])

        pog_dist = math.vecmag(math.get_dist(player_car.position, common_values.BLUE_GOAL_CENTER))
        ob.append([pog_dist])

        for other in players:
            if other.car_id == player.car_id:
                continue

            if player.team_num == common_values.ORANGE_TEAM:
                car_data = other.inverted_car_data
            else:
                car_data = other.car_data

            ob.append(car_data.position)
            ob.append(car_data.euler_angles())
            ob.append(np.sin(car_data.euler_angles()))
            ob.append(np.cos(car_data.euler_angles()))
            ob.append(car_data.linear_velocity)
            ob.append(car_data.angular_velocity)

            pc_dist = math.vecmag(math.get_dist(player_car.position, car_data.position))
            ob.append([pc_dist])

        return np.concatenate(ob)
