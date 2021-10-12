"""
The action parser.
"""

from abc import ABC, abstractmethod
from rlgym.utils.gamestates import PlayerData, GameState
import gym.spaces
import numpy as np
from typing import List, Union, Tuple, Dict, Any


class ActionParser(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_action_space(self) -> gym.spaces.Space:
        """
        Function that returns the action space type. It will be called during the initialization of the environment.
        
        :return: The type of the action space
        """
        raise NotImplementedError

    @abstractmethod
    def parse_actions(self, actions: Any, state: GameState) -> np.ndarray:
        """
        Function that parses actions from the action space into a format that rlgym understands.
        The expected return value is a numpy float array of size (n, 8) where n is the number of agents.
        The second dimension is indexed as follows: throttle, steer, yaw, pitch, roll, jump, boost, handbrake.
        The first five values are expected to be in the range [-1, 1], while the last three values should be either 0 or 1.

        :param actions: An object of actions, as passed to the `env.step` function.
        :param state: The GameState object of the current state that were used to generate the actions.

        :return: the parsed actions in the rlgym format.
        """
        raise NotImplementedError
