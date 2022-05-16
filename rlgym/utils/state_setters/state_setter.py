"""
Base state setter class.
"""
from abc import ABC, abstractmethod
from rlgym.utils.state_setters.wrappers.state_wrapper import StateWrapper


class StateSetter(ABC):

    def build_wrapper(self, max_team_size: int, spawn_opponents: bool) -> StateWrapper:
        """
        Function to be called each time the environment is reset.

        :param max_team_size: The maximum supported team size in the current rlgym instance.
        :param spawn_opponents: If the user expects agents in the orange side or not, only provided for backwards compatibility.

        :returns: The StateWrapper object that will be received in StateSetter.reset(), any team shapes are supported as
        long as team size is smaller or equal to max_team_size
        """
        return StateWrapper(blue_count=max_team_size, orange_count=max_team_size if spawn_opponents else 0)

    @abstractmethod
    def reset(self, state_wrapper: StateWrapper):
        """
        Function to be called each time the environment is reset.

        :param state_wrapper: StateWrapper object to be modified with desired state values.

        NOTE: This function should change any desired values of the StateWrapper, which are all defaulted to 0.
        The values within StateWrapper are sent to the game each time the match is reset.
        """
        raise NotImplementedError
