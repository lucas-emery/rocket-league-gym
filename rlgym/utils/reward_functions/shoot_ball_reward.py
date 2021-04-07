import numpy as np
from rlgym.utils import math, common_values
from rlgym.utils.reward_functions import RewardFunction


class ShootBallReward(RewardFunction):
    GOAL_REWARD = 60
    GOAL_PUNISHMENT = -40
    PLAYER_TO_BALL_VEL_WEIGHT = 0.04
    BALL_TO_GOAL_VEL_WEIGHT = 0.065

    def __init__(self):
        super().__init__()
        self.orange_score = 0
        self.blue_score = 0
        self.last_touch = None

    def reset(self, initial_state):
        self.last_touch = None

    def get_reward(self, player, state, previous_action):
        self.last_touch = state.last_touch

        b_rew = self._get_player_ball_reward(player, state) * ShootBallReward.PLAYER_TO_BALL_VEL_WEIGHT
        g_rew = self._get_ball_goal_reward(player, state) * ShootBallReward.BALL_TO_GOAL_VEL_WEIGHT

        return b_rew + g_rew

    def get_final_reward(self, player, state, previous_action):
        return self._get_goal_reward(player, state)

    def _get_ball_goal_reward(self, player, state):
        if player.team_num == common_values.BLUE_TEAM:
            ball = state.ball
        else:
            ball = state.inverted_ball

        b_vel = ball.linear_velocity
        b_pos = ball.position
        g_pos = common_values.ORANGE_GOAL_CENTER

        dist = math.get_dist(g_pos, b_pos)
        vel_to_goal = math.scalar_projection(b_vel, dist)

        return vel_to_goal / 100

    def _get_player_ball_reward(self, player, state):
        if player.team_num == common_values.BLUE_TEAM:
            ball = state.ball
            car = player.car_data
        else:
            ball = state.inverted_ball
            car = player.inverted_car_data

        p_vel = car.linear_velocity
        b_pos = ball.position
        p_pos = car.position

        dist = math.get_dist(b_pos, p_pos)
        vel_to_ball = math.scalar_projection(p_vel, dist)

        return vel_to_ball / 100

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
