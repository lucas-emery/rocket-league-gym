"""
The Transition Engine class.
"""
from abc import abstractmethod
from typing import Any, Dict, List, TypeVar, Generic

AgentID = TypeVar("AgentID", bound=str)
StateType = TypeVar("StateType")
EngineActionType = TypeVar("EngineActionType")


class TransitionEngine(Generic[AgentID, StateType, EngineActionType]):

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
    def create_base_state(self) -> StateType:
        # TODO docs - Creates a minimal State object for the state mutators to modify,
        #  can we let the mutators know which fields they can modify by not populating those?
        raise NotImplementedError

    @abstractmethod
    def set_state(self, desired_state: StateType) -> StateType:
        # TODO docs - returns the actual initial state,
        #  the transition engine may not be able to set every requested state attribute
        # Can we use a setter instead? It's hard to convey that the actual state may be different from the desired state
        #  Can we just rely on warnings?
        #  What's the execution cost of printing all these warning that will be ignored most of the time?
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        # TODO docs
        raise NotImplementedError
