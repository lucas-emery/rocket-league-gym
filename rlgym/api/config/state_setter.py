"""
Base state setter class.
"""
from abc import abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic

StateType = TypeVar("StateType")
StateWrapperType = TypeVar("StateWrapperType")


class StateSetter(Generic[StateType, StateWrapperType]):

    @abstractmethod
    def build_wrapper(self, prev_state: Optional[StateType], shared_info: Dict[str, Any]) -> StateWrapperType:
        """
        Function to be called each time the environment is reset, before StateSetter.reset()

        :param prev_state: The previous state of the environment before resetting, can be None if this is the first reset.
        :param shared_info: A dictionary with shared information across all config objects.

        :returns: The StateWrapper object that will be received in StateSetter.reset(), any team shapes are supported as
        long as team size is smaller or equal to the max team size allowed by the TransitionEngine
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self, state_wrapper: StateWrapperType, shared_info: Dict[str, Any]) -> None:
        """
        Function to be called each time the environment is reset.

        :param state_wrapper: StateWrapper object to be modified with desired state values.
        :param shared_info: A dictionary with shared information across all config objects.

        NOTE: This function should change any desired values of the StateWrapper, which are all defaulted to 0.
        The values within StateWrapper are sent to the game each time the match is reset.
        """
        raise NotImplementedError