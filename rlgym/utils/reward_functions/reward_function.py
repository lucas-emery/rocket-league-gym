from abc import ABC, abstractmethod
from rlgym.utils.gamestates import GameState, PlayerData
import numpy as np


class RewardFunction(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def reset(self, initial_state: GameState, optional_data=None):
        raise NotImplementedError

    @abstractmethod
    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        raise NotImplementedError

    @abstractmethod
    def get_final_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None):
        raise NotImplementedError
