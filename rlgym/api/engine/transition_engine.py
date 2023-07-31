"""
The Transition Engine class.
"""
from abc import abstractmethod
from typing import Any, Dict, List, TypeVar, Generic

AgentID = TypeVar("AgentID", bound=str)
StateType = TypeVar("StateType")
StateWrapperType = TypeVar("StateWrapperType")
EngineActionType = TypeVar("EngineActionType")


class TransitionEngine(Generic[AgentID, StateType, StateWrapperType, EngineActionType]):

    @property
    @abstractmethod
    def agents(self) -> List[AgentID]:
        # TODO docs
        raise NotImplementedError

    @property
    @abstractmethod
    def max_num_agents(self) -> int:
        # TODO docs
        raise NotImplementedError

    @property
    @abstractmethod
    def state(self) -> StateType:
        # TODO docs
        raise NotImplementedError

    @property
    @abstractmethod
    def config(self) -> Dict[str, Any]:
        # TODO docs
        raise NotImplementedError

    @config.setter
    @abstractmethod
    def config(self, value: Dict[str, Any]):
        # TODO docs
        raise NotImplementedError

    @abstractmethod
    def step(self, actions: Dict[AgentID, EngineActionType]) -> StateType:
        #TODO docs
        raise NotImplementedError

    @abstractmethod
    def set_state(self, state_wrapper: StateWrapperType) -> StateType:
        # TODO docs
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        # TODO docs
        raise NotImplementedError
