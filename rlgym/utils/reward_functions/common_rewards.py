from collections import defaultdict

import numpy as np

from rlgym.utils import math
from rlgym.utils.reward_functions import RewardFunction
from rlgym.utils.common_values import BLUE_TEAM, ORANGE_GOAL_CENTER, BLUE_GOAL_CENTER, ORANGE_TEAM
from rlgym.utils.gamestates import GameState, PlayerData


class TouchBallReward(RewardFunction):
    def reset(self, initial_state: GameState, optional_data=None):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        return 1 if player.ball_touched else 0


class PlayerTowardsBallReward(RewardFunction):
    def reset(self, initial_state: GameState, optional_data=None):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        # Vector version of v=d/t <=> t=d/v <=> 1/t=v/d
        # Max value should be max_speed / ball_radius = 2300 / 94 = 24.5
        # Used to guide the agent towards the ball
        inv_t = math.scalar_projection(player.car_data.linear_velocity, state.ball.position - player.car_data.position)
        return inv_t


class GoalReward(RewardFunction):
    def __init__(self, per_goal: float = 1., team_score_coeff: float = 0., concede_coeff: float = 0.):
        super().__init__()
        self.per_goal = per_goal
        self.team_score_coeff = team_score_coeff
        self.concede_coeff = concede_coeff

        # Need to keep track of last registered value to detect changes
        self.last_registered_values = {}

    def reset(self, initial_state: GameState, optional_data=None):
        # Update every reset since rocket league may crash and be restarted with clean values
        for player in initial_state.players:
            self.last_registered_values[player.car_id] = {
                "goals": player.match_goals,
                "blue": initial_state.blue_score,
                "orange": initial_state.orange_score
            }

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        values = self.last_registered_values[player.car_id]

        d_player = player.match_goals - values["goals"]
        values["goals"] = player.match_goals

        d_blue = state.blue_score - values["blue"]
        values["blue"] = state.blue_score

        d_orange = state.orange_score - values["orange"]
        values["orange"] = state.orange_score

        if player.team_num == BLUE_TEAM:
            return self.per_goal * d_player + self.team_score_coeff * d_blue - self.concede_coeff * d_orange
        else:
            return self.per_goal * d_player + self.team_score_coeff * d_orange - self.concede_coeff * d_blue


class BallTowardsGoalReward(RewardFunction):
    def __init__(self, away_from_own_goal=False):
        super().__init__()

        # If set, gives negative reward for ball heading towards player's net
        self.away_from_own_goal = away_from_own_goal

    def reset(self, initial_state: GameState, optional_data=None):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        if player.team_num == BLUE_TEAM and not self.away_from_own_goal\
                or player.team_num == ORANGE_TEAM and self.away_from_own_goal:
            objective = np.array(ORANGE_GOAL_CENTER)
        else:
            objective = np.array(BLUE_GOAL_CENTER)
        objective[1] *= 6000 / 5120  # Use back of net instead to prevent exploding reward
        # Max value should be max_speed / min_dist = 6000 / 786 = 7.6
        inv_t = math.scalar_projection(state.ball.linear_velocity, objective - player.car_data.position)
        if self.away_from_own_goal:
            return -inv_t
        else:
            return inv_t


class StandStillReward(RewardFunction):
    # Simple reward function to ensure the model is training.
    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        return - np.linalg.norm(player.car_data.linear_velocity) - np.linalg.norm(player.car_data.angular_velocity)


class SaveBoostReward(RewardFunction):
    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        # 1 reward for each frame with 100 boost, sqrt because 0->20 makes bigger difference than 80->100
        return np.sqrt(player.boost_amount)
