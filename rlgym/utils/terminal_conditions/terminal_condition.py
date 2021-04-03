"""
A terminal condition.
"""

from abc import ABC, abstractmethod
from rlgym.utils.gamestates import GameState


class TerminalCondition(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def reset(self, initial_state: GameState):
        """
        Function to be called each time the environment is reset.

        :param initial_state: The initial state of the reset environment.
        """
        raise NotImplementedError

    @abstractmethod
    def is_terminal(self, current_state: GameState) -> bool:
        """
        Function to determine if a game state is terminal. This will be called once per step, and must return either
        `True` or `False` if the current episode should be terminated at this state.

        :param current_state: The current state of the game.

        :return: Bool representing whether the current state is a terminal one.
        """
        raise NotImplementedError

    @abstractmethod
    def look_ahead(self, current_state: GameState) -> bool:
        """
        Function to predict if the current game state will be terminal when the `is_terminal` function is called. This is
        used to determine which function should be used to compute the reward at each step. If this function returns `True`,
        then `get_final_reward` will be called from the reward function for this step. Otherwise, `get_reward` will be
        called for this step.

        :param current_state: The current state of the game.

        :return: Bool representing whether the current state will be considered a terminal one when `is_terminal`
        is next called.
        """
        raise NotImplementedError
