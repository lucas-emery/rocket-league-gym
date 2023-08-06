"""
An RLGym renderer.
"""
from abc import abstractmethod
from typing import Any, Generic
from rlgym.api.typing import StateType


class Renderer(Generic[StateType]):
    #TODO docs

    @abstractmethod
    def render(self, state: StateType) -> Any:
        raise NotImplementedError
