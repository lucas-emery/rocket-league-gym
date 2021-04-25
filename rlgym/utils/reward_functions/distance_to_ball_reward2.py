from rlgym.utils.reward_functions import RewardFunction
from rlgym.utils import math, common_values
from rlgym.utils.gamestates import GameState, PlayerData
import numpy as np
import math as mathpy


class distance_to_ball2(RewardFunction):
    def __init__(self):
        super().__init__()
        self.last_touch = None

    def reset(self, initial_state: GameState):
        self.last_touch = initial_state.last_touch
        print('reset')
        return

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        self.last_touch = state.last_touch
        if player.team_num == common_values.BLUE_TEAM:
            ball = state.ball
            car = player.car_data
        else:
            ball = state.inv_ball
            car = player.inverted_car_data

        b_pos = ball.position
        car_pos = player.car_data.position
        distance_ball_car = math.get_dist(b_pos, car_pos)
        distance_norm = math.vecmag(distance_ball_car)
        velocity_num = math.vecmag(player.car_data.linear_velocity)
        not_fast_enough = velocity_num < 400
        reward = max(0, (np.dot(math.unitvec(player.car_data.linear_velocity), math.unitvec(distance_ball_car))-.5)*velocity_num/1000) - not_fast_enough - 1 
        #reward =  (player.facing_ball-.5)*3 + player.ball_touched*160 + (np.dot(math.unitvec(player.car_data.linear_velocity), math.unitvec(distance_ball_car))-.3)*velocity_num/10 - 20/(velocity_num+1)- 3
        #- mathpy.log(player.ticks_since_last_touch/100 + 1) + player.ball_touched*500 + np.dot(player.car_data.linear_velocity, distance_ball_car)*4
        #4/(distance_norm + 1)
        #print(reward)
        return reward

    def get_final_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        return self.get_reward(player, state, previous_action)