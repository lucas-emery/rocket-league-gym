from rlgym.utils.reward_functions import RewardFunction
from rlgym.utils import math
from rlgym.utils.gamestates import GameState, PlayerData
import numpy as np


# THIS REWARD IS FOR DEMONSTRATION PURPOSES ONLY
class DefaultReward(RewardFunction):
    def __init__(self):
        super().__init__()
        self.last_touch = None

    def reset(self, initial_state: GameState):
        self.last_touch = initial_state.last_touch

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        return - math.vecmag(player.car_data.angular_velocity) / 100

    def get_final_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        return self.get_reward(player, state, previous_action)
