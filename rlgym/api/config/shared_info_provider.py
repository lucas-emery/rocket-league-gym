from abc import abstractmethod
from typing import Generic, Dict, Any, List
from ..typing import AgentID, StateType


class SharedInfoProvider(Generic[AgentID, StateType]):
    """
    The shared information provider. This class is responsible for managing shared information across all config objects.
    """

    @abstractmethod
    def create(self, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Function to be called before anything else each time the environment is set to a particular state,
        either via set_state, reset or __init__.

        :param shared_info: The previous shared information dictionary
        """
        raise NotImplementedError

    @abstractmethod
    def set_state(self, agents: List[AgentID], initial_state: StateType, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Function to be called each time the environment is set to a particular state (either via set_state or reset),
        right after the transition engine is called.

        :param agents: List of AgentIDs for which this SharedInfoProvider will manage the SharedInfo
        :param initial_state: The initial state of the environment
        :param shared_info: The previous shared information dictionary
        """
        raise NotImplementedError

    @abstractmethod
    def step(self, agents: List[AgentID], state: StateType, shared_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Function to be called each time the environment is stepped, right after the transition engine is called.

        :param agents: List of AgentIDs for which this SharedInfoProvider should manage the SharedInfo
        :param state: The new state of the environment
        :param shared_info: The previous shared information dictionary
        """
        raise NotImplementedError
