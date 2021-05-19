import numpy as np

from rlgym.utils import math
from rlgym.utils.reward_functions import RewardFunction
from rlgym.utils.common_values import BLUE_TEAM, ORANGE_GOAL_CENTER, BLUE_GOAL_CENTER
from rlgym.utils.gamestates import GameState, PlayerData


class TouchBallReward(RewardFunction):
    def reset(self, initial_state: GameState, optional_data=None):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        return 1 if player.ball_touched else 0

    def get_final_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        return 0


class MoveTowardsBallReward(RewardFunction):
    def reset(self, initial_state: GameState, optional_data=None):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        # Vector version of v=d/t <=> t=d/v <=> 1/t=v/d
        # Max value should be max_speed / ball_radius = 2300 / 94 = 24.5
        # Used to guide the agent towards the ball
        inv_t = math.scalar_projection(player.car_data.linear_velocity, state.ball.position - player.car_data.position)
        return inv_t

    def get_final_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        return 0


class GoalReward(RewardFunction):
    def __init__(self, per_goal: float = 1., team_score_coeff: float = 0., concede_coeff: float = 0.):
        super().__init__()
        self.per_goal = per_goal
        self.team_score_coeff = team_score_coeff
        self.concede_coeff = concede_coeff

        # Need to keep track of last registered value to detect changes
        self.goals_scored = {}
        self.blue_goals = 0
        self.orange_goals = 0

    def reset(self, initial_state: GameState, optional_data=None):
        # Update every reset since rocket league may crash and be restarted with clean values
        self.blue_goals = initial_state.blue_score
        self.orange_goals = initial_state.orange_score
        for player in initial_state.players:
            self.goals_scored[player.car_id] = player.match_goals

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        self.goals_scored[player.car_id], d_player = player.match_goals, player.match_goals - self.goals_scored[player.car_id]
        self.blue_goals, d_blue = state.blue_score, state.blue_score - self.blue_goals
        self.orange_goals, d_orange = state.orange_score, state.orange_score - self.orange_goals

        if player.team_num == BLUE_TEAM:
            return self.per_goal * d_player + self.team_score_coeff * d_blue - self.concede_coeff * d_orange
        else:
            return self.per_goal * d_player + self.team_score_coeff * d_orange - self.concede_coeff * d_blue

    def get_final_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        return 0


class MoveTowardsGoalReward(RewardFunction):
    def reset(self, initial_state: GameState, optional_data=None):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        objective = np.array(ORANGE_GOAL_CENTER if player.team_num == BLUE_TEAM else BLUE_GOAL_CENTER)
        objective[1] *= 6000 / 5120  # Use back of net instead to prevent exploding reward
        # Max value should be max_speed / min_dist = 6000 / 786 = 7.6
        inv_t = math.scalar_projection(state.ball.linear_velocity, objective - player.car_data.position)
        return inv_t

    def get_final_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        return 0


class StandStillReward(RewardFunction):
    # Simple reward function to ensure the model is training.
    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        return - np.linalg.norm(player.car_data.linear_velocity) - np.linalg.norm(player.car_data.angular_velocity)

    def get_final_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        return 0
