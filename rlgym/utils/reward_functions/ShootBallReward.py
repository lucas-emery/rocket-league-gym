import numpy as np
from rlgym.utils import Math

class ShootBallReward(object):
    GOAL_REWARD = 60
    GOAL_PUNISHMENT = -40
    PLAYER_TO_BALL_VEL_WEIGHT = 0.04
    BALL_TO_GOAL_VEL_WEIGHT = 0.065

    def __init__(self):
        y = 5120
        x = 0
        #half the goal height
        z = 642.775 /2
        self.goal_location = [x,y,z]

        self.orange_score = 0
        self.blue_score = 0

    def reset(self):
        pass

    def get_reward(self, state):
        b_rew = self._get_player_ball_reward(state) * ShootBallReward.PLAYER_TO_BALL_VEL_WEIGHT
        g_rew = self._get_ball_goal_reward(state) * ShootBallReward.BALL_TO_GOAL_VEL_WEIGHT

        return b_rew + g_rew

    def get_final_reward(self, state):
        return self._get_goal_reward(state)

    def _get_ball_goal_reward(self, state):
        b_vel = state.player.ball_data[3:6]
        b_pos = state.player.ball_data[:3]
        g_pos = self.goal_location
        dist = Math.get_dist(g_pos, b_pos)

        return np.sum(Math.project_vec(dist, b_vel)) / 100

    def _get_player_ball_reward(self, state):
        p_vel = state.player.car_data[7:10]
        b_pos = state.player.ball_data[:3]
        p_pos = state.player.car_data[:3]
        dist = Math.get_dist(b_pos, p_pos)

        return np.sum(Math.project_vec(dist, p_vel)) / 100

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