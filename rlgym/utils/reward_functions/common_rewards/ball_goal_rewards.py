import numpy as np

from rlgym.utils import RewardFunction, math
from rlgym.utils.common_values import BLUE_TEAM, ORANGE_TEAM, ORANGE_GOAL_CENTER, BLUE_GOAL_CENTER, ORANGE_GOAL_BACK, \
    BLUE_GOAL_BACK
from rlgym.utils.gamestates import GameState, PlayerData


class DistanceBallToGoalReward(RewardFunction):
    def __init__(self, own_goal=False):
        super().__init__()
        self.own_goal = own_goal

    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        if player.team_num == BLUE_TEAM and not self.own_goal \
                or player.team_num == ORANGE_TEAM and self.own_goal:
            objective = np.array(ORANGE_GOAL_BACK)
        else:
            objective = np.array(BLUE_GOAL_BACK)

        dist = np.linalg.norm(state.ball.position - objective) - 786  # Compensate for moving objective to back of net
        return np.exp(-0.5 * dist / 2300)  # Inspired by https://arxiv.org/abs/2105.12196


class VelocityBallToGoalReward(RewardFunction):
    def __init__(self, own_goal=False, use_scalar_projection=False):
        super().__init__()
        self.own_goal = own_goal
        self.use_scalar_projection = use_scalar_projection

    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        if player.team_num == BLUE_TEAM and not self.own_goal \
                or player.team_num == ORANGE_TEAM and self.own_goal:
            objective = np.array(ORANGE_GOAL_BACK)
        else:
            objective = np.array(BLUE_GOAL_BACK)

        vel = state.ball.linear_velocity
        pos_diff = objective - state.ball.position
        if self.use_scalar_projection:
            # Vector version of v=d/t <=> t=d/v <=> 1/t=v/d
            # Max value should be max_speed / ball_radius = 2300 / 94 = 24.5
            # Used to guide the agent towards the ball
            inv_t = math.scalar_projection(vel, pos_diff)
            return inv_t
        else:
            # Regular component velocity
            norm_pos_diff = pos_diff / np.linalg.norm(pos_diff)
            vel /= 2300  # Supersonic, but ball can go faster
            return float(np.dot(norm_pos_diff, vel))


class BallYCoordinateReward(RewardFunction):
    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        if player.team_num == BLUE_TEAM:
            return (state.ball.position[1] / (5120 + 94)) ** 3
        else:
            return (state.inverted_ball.position[1] / (5120 + 94)) ** 3