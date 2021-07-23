"""
Base state setter class.
"""
from abc import ABC, abstractmethod
from rlgym.utils.state_setters.wrappers.state_wrapper import StateWrapper


class StateSetter(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def reset(self, state_wrapper: StateWrapper):
        """
        Function to be called each time the environment is reset.

        :param state_wrapper: StateWrapper object to be modified with desired state values.

        NOTE: This function should change any desired values of the StateWrapper, which are all defaulted to 0.
        The values within StateWrapper are sent to the game each time the match is reset.
        """
        raise NotImplementedError
