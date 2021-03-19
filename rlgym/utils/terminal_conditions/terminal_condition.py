from abc import ABC, abstractmethod
from rlgym.utils.gamestates import GameState


class TerminalCondition(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def reset(self, initial_state: GameState, optional_data=None):
        raise NotImplementedError

    @abstractmethod
    def is_terminal(self, state: GameState, optional_data=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def look_ahead(self, state: GameState, optional_data=None) -> bool:
        raise NotImplementedError
