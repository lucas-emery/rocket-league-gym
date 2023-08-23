"""
An RLGym renderer.
"""
from abc import abstractmethod
from typing import Any, Dict, Generic
from rlgym.api.typing import StateType


class Renderer(Generic[StateType]):
    #TODO docs

    @abstractmethod
    def render(self, state: StateType, shared_info: Dict[str, Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError
