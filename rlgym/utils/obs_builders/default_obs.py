from rlgym.utils.obs_builders import ObsBuilder
from rlgym.utils import common_values
import numpy as np


class DefaultObs(ObsBuilder):
    def __init__(self):
        super().__init__()

    def reset(self, initial_state):
        pass

    def build_obs(self, player, state, prev_action) -> np.ndarray:
        players = state.players
        if player.team_num == common_values.ORANGE_TEAM:
            player_car = player.inverted_car_data
            ball = state.inverted_ball
        else:
            player_car = player.car_data
            ball = state.ball

        ob = []
        ob.append([int(player.has_flip),
                   player.boost_amount,
                   int(player.on_ground)])

        ob.append(player_car.position)
        ob.append(player_car.linear_velocity)
        ob.append(player_car.angular_velocity)

        ob.append(ball.position)
        ob.append(ball.linear_velocity)
        ob.append(ball.angular_velocity)

        for other in players:
            if other.car_id == player.car_id:
                continue

            if player.team_num == common_values.ORANGE_TEAM:
                car_data = other.inverted_car_data
            else:
                car_data = other.car_data

            ob.append(car_data.position)
            ob.append(car_data.linear_velocity)
            ob.append(car_data.angular_velocity)
            
        return np.concatenate(ob)
