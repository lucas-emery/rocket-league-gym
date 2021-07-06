import numpy as np

from rlgym.utils import RewardFunction, math
from rlgym.utils.common_values import BALL_RADIUS
from rlgym.utils.gamestates import GameState, PlayerData


class DistancePlayerToBallReward(RewardFunction):
    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        dist = np.linalg.norm(player.car_data.position - state.ball.position) - 94  # Compensate for ball radius
        return np.exp(-0.5 * dist / 2300)  # Inspired by https://arxiv.org/abs/2105.12196


class VelocityPlayerToBallReward(RewardFunction):
    def __init__(self, use_scalar_projection=False):
        super().__init__()
        self.use_scalar_projection = use_scalar_projection

    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        vel = player.car_data.linear_velocity
        pos_diff = state.ball.position - player.car_data.position
        if self.use_scalar_projection:
            # Vector version of v=d/t <=> t=d/v <=> 1/t=v/d
            # Max value should be max_speed / ball_radius = 2300 / 92.75 = 24.8
            # Used to guide the agent towards the ball
            inv_t = math.scalar_projection(vel, pos_diff)
            return inv_t
        else:
            # Regular component velocity
            norm_pos_diff = pos_diff / np.linalg.norm(pos_diff)
            vel /= 2300  # Supersonic (max speed)
            return float(np.dot(norm_pos_diff, vel))


class FaceBallReward(RewardFunction):
    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        pos_diff = state.ball.position - player.car_data.position
        norm_pos_diff = pos_diff / np.linalg.norm(pos_diff)
        return float(np.dot(player.car_data.forward(), norm_pos_diff))


class TouchBallReward(RewardFunction):
    def __init__(self, aerial_weight=1.):
        self.aerial_weight = aerial_weight

    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        if player.ball_touched:
            return (0.5 + state.ball.position[2] / (2 * BALL_RADIUS)) ** self.aerial_weight
        return 0
