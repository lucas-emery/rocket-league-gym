import numpy as np
from rlgym.utils import Math, CommonValues
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

    def reset(self):
        pass

    def get_reward(self, state):
        b_rew = self._get_player_ball_reward(state) * ShootBallReward.PLAYER_TO_BALL_VEL_WEIGHT
        g_rew = self._get_ball_goal_reward(state) * ShootBallReward.BALL_TO_GOAL_VEL_WEIGHT

        # print("{:3.6f}  |  {:3.6f}".format(b_rew, g_rew))
        return b_rew + g_rew

    def get_final_reward(self, state):
        return self._get_goal_reward(state)

    def _get_ball_goal_reward(self, state):
        b_vel = state.player.ball_data.linear_velocity
        b_pos = state.player.ball_data.position
        g_pos = CommonValues.ORANGE_GOAL_CENTER

        dist = Math.get_dist(g_pos, b_pos)
        vel_to_goal = Math.scalar_projection(b_vel, dist)

        return vel_to_goal / 100

    def _get_player_ball_reward(self, state):
        p_vel = state.player.car_data.linear_velocity
        b_pos = state.player.ball_data.position
        p_pos = state.player.car_data.position

        dist = Math.get_dist(b_pos, p_pos)
        vel_to_ball = Math.scalar_projection(p_vel, dist)

        return vel_to_ball / 100

    def _get_goal_reward(self, state):
        os = state.orange_score
        bs = state.blue_score

        if os != self.orange_score:
            self.orange_score = os
            return ShootBallReward.GOAL_PUNISHMENT

        if bs != self.blue_score:
            self.blue_score = bs
            return ShootBallReward.GOAL_REWARD

        return 0
