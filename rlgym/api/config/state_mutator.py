from abc import abstractmethod
from typing import Any, Dict, Generic
from ..typing import StateType


class StateMutator(Generic[StateType]):
    """
    The state mutator class. This class is responsible for modifying the state of the environment.
    """

    @abstractmethod
    def apply(self, state: StateType, shared_info: Dict[str, Any]) -> None:
        """
        Function to be called each time the environment is reset.
        This function should change any desired values of the State.
        The values within State are sent to the transition engine to set up the initial state.

        :param state: State object to be modified with desired state values.
        :param shared_info: A dictionary with shared information across all config objects.
        """
        raise NotImplementedError
