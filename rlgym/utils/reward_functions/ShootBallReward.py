import numpy as np
from rlgym.utils import Math

class ShootBallReward(object):
    def __init__(self):
        self._best_player_ball_dist = None
        self._start_player_ball_dist = None

        self._best_goal_ball_dist = None
        self._start_goal_ball_dist = None

        self._prev_ball_dist = None

        #back of goal y-coord + depth of goal
        y = 8064 - 880

        #half the field width
        x = 4096/2

        #half the goal height
        z = 642.775 /2
        self.goal_location = [x,y,z]

        self.goal_dist_weight = 10
        self.ball_dist_weight = 1

    def reset(self):
        self._best_player_ball_dist = None
        self._start_player_ball_dist = None

        self._best_goal_ball_dist = None
        self._start_goal_ball_dist = None

        self._prev_ball_dist = None

    def get_reward(self,state):
        b_rew = self._get_player_ball_reward(state) * self.ball_dist_weight
        g_rew = self._get_ball_goal_reward(state) * self.goal_dist_weight
        return b_rew + g_rew

    def _get_ball_goal_reward(self, state):
        dist_to_goal = Math.get_dist(state.player.ball_data[:3], self.goal_location)

        if self._start_goal_ball_dist is None:
            self._start_goal_ball_dist = dist_to_goal
            self._best_goal_ball_dist = dist_to_goal
            self._prev_ball_dist = dist_to_goal

        if dist_to_goal != self._prev_ball_dist:
            current = 1.0 - (self._prev_ball_dist / self._start_goal_ball_dist)

            self._prev_ball_dist = dist_to_goal

            new = 1.0 - (dist_to_goal / self._start_goal_ball_dist)
            best = 1.0 - (self._best_goal_ball_dist / self._start_goal_ball_dist)

            current_rew = round(current - best, 5)
            new_rew = round(new - best, 5)

            rew = new_rew - current_rew
        else:
            rew = 0

        #print(rew," | ", dist_to_goal, " | ", self._best_goal_ball_dist)

        if self._best_goal_ball_dist > dist_to_goal:
            self._best_goal_ball_dist = dist_to_goal

        return rew

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