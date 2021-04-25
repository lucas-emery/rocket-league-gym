from rlgym.utils.reward_functions import RewardFunction
from rlgym.utils import math, common_values
from rlgym.utils.gamestates import GameState, PlayerData
import numpy as np
import math as mathpy


class MyReward(RewardFunction):
    GOAL_REWARD = 60
    GOAL_PUNISHMENT = -40
    PLAYER_TO_BALL_VEL_WEIGHT = 0.04
    BALL_TO_GOAL_VEL_WEIGHT = 0.065

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
        p_pos = car.position

        distance_ball_car = math.get_dist(b_pos, p_pos)
        distance_norm = math.vecmag(distance_ball_car)
        p_vel = car.linear_velocity

        vel_to_ball = math.scalar_projection(p_vel, distance_ball_car)
        reward =  .04*vel_to_ball player.ball_touched*10 - 1
        #reward =  (player.facing_ball-.5)*3 + player.ball_touched*160 + (np.dot(math.unitvec(player.car_data.linear_velocity), math.unitvec(distance_ball_car))-.3)*velocity_num/10 - 20/(velocity_num+1)- 3
        #- mathpy.log(player.ticks_since_last_touch/100 + 1) + player.ball_touched*500 + np.dot(player.car_data.linear_velocity, distance_ball_car)*4
        #4/(distance_norm + 1)
        return reward

    def get_final_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        return self.get_reward(player, state, previous_action)


    def _get_goal_reward(self, player, state):
        os = state.orange_score
        bs = state.blue_score
        team = player.team_num

        if os != self.orange_score:
            self.orange_score = os
            if team == common_values.ORANGE_TEAM and self.last_touch == player.car_id:
                return ShootBallReward.GOAL_REWARD
            return ShootBallReward.GOAL_PUNISHMENT

        if bs != self.blue_score:
            self.blue_score = bs
            if team == common_values.BLUE_TEAM and self.last_touch == player.car_id:
                return ShootBallReward.GOAL_REWARD
            return ShootBallReward.GOAL_PUNISHMENT

        return 0