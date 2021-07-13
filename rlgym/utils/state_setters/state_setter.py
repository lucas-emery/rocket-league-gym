"""
Base state setter class.
"""
from typing import NoReturn
from abc import ABC, abstractmethod
from rlgym.utils.gamestates.state_wrapper import StateWrapper


class StateSetter(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def reset(self, state_wrapper: StateWrapper) -> NoReturn:
        """
        Function to be called each time the environment is reset.

        This function should change any desired values of the StateWrapper, which are all defaulted to 0.
        The StateWrapper is what is sent to the game each time the match is reset.
        """
        raise NotImplementedError
