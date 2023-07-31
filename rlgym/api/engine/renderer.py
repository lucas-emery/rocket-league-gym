"""
An RLGym renderer.
"""
from abc import abstractmethod
from typing import Any, Generic, TypeVar

StateType = TypeVar("StateType")


class Renderer(Generic[StateType]):
    #TODO docs

    @abstractmethod
    def render(self, state: StateType) -> Any:
        raise NotImplementedError
