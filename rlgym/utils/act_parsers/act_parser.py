"""
The action parser.
"""

from abc import ABC, abstractmethod
from rlgym.utils.gamestates import PlayerData, GameState
import gym.spaces
import numpy as np
from typing import List, Union, Tuple, Dict, Any


class ActParser(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_action_space(self) -> gym.spaces.Space:
        """
        Function that returns the action space type. It will be called during the initialization of the environment.
        For now, only simple action spaces are supported: actions must support the `fill()` function.
        
        :return: The type of the action space
        """
        raise NotImplementedError

    @abstractmethod
    def parse_actions(self, actions: Any) -> np.ndarray:
        """
        Function that parses actions from the action space into a format that rlgym understands.
        The expected return value is a numpy float array of size (n, 8) where n is the number of agents.
        The second dimension is indexed as follows: throttle, steer, yaw, pitch, roll, jump, boost, handbrake.
        The first five values are expected to be in the range [-1, 1], while the last three values should be either 0 or 1.

        Function to build observations for a policy. This is where all observations will be constructed every step and
        every reset. This function is given a player argument, and it is expected that the observation returned by this
        function will contain information from the perspective of that player. This function is called once for each
        agent automatically at every step.

        :param actions: An object of actions, as passed to the `env.step` function.

        :return: the parsed actions in the rlgym format.
        """
        raise NotImplementedError
