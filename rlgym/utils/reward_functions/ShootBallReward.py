import numpy as np
from rlgym.utils import Math

class ShootBallReward(object):
    def __init__(self):
        self._best_player_ball_dist = None
        self._start_player_ball_dist = None

        self._best_goal_ball_dist = None
        self._start_goal_ball_dist = None

        self._prev_ball_dist = None

        y = 5120
        x = 0
        #half the goal height
        z = 642.775 /2
        self.goal_location = [x,y,z]

        self.goal_dist_weight = 20
        self.ball_dist_weight = 1

    def reset(self):
        self._best_player_ball_dist = None
        self._start_player_ball_dist = None

        self._best_goal_ball_dist = None
        self._start_goal_ball_dist = None

        self._prev_ball_dist = None

    def get_reward(self, state):
        b_rew = self._get_player_ball_reward(state) * self.ball_dist_weight
        g_rew = self._get_ball_goal_reward(state) * self.goal_dist_weight
        return b_rew + g_rew
        #return b_rew

    def get_final_reward(self, state):
        return 0 #self.get_reward(state)

    def _get_ball_goal_reward(self, state):
        dist = Math.get_distance_to_ball_2d(self.goal_location, state.player.ball_data[:3])
        if self._start_goal_ball_dist is None:
            self._start_goal_ball_dist = dist
            self._best_goal_ball_dist = dist

        elif self._best_goal_ball_dist > dist:
            current = 1.0 - (self._best_goal_ball_dist / self._start_goal_ball_dist)
            self._best_goal_ball_dist = dist
            new = 1.0 - (self._best_goal_ball_dist / self._start_goal_ball_dist)
            return new - current

        return 0

    def _get_player_ball_reward(self, state):
        dist = Math.get_distance_to_ball_2d(state.player.car_data, state.player.ball_data)
        if self._start_player_ball_dist is None:
            self._start_player_ball_dist = dist
            self._best_player_ball_dist = dist

        elif self._best_player_ball_dist > dist:
            current = 1.0 - (self._best_player_ball_dist / self._start_player_ball_dist)
            self._best_player_ball_dist = dist
            new = 1.0 - (self._best_player_ball_dist / self._start_player_ball_dist)
            return new - current

        return 0