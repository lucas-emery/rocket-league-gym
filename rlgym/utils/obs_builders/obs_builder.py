from abc import ABC, abstractmethod
from rlgym.utils.gamestates import PhysicsObject, PlayerData, GameState
from rlgym.utils import common_values
import numpy as np
from typing import Any


class ObsBuilder(ABC):
    def __init__(self):
        pass

    # This method is optional
    @abstractmethod
    def reset(self, initial_state: GameState, optional_data=None):
        raise NotImplementedError

    # This is the function that rlgym calls to make the obs for each agent
    # A List of whatever you return here will be the value of "obs" returned from gym.step
    @abstractmethod
    def build_obs(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None) -> Any:
        raise NotImplementedError