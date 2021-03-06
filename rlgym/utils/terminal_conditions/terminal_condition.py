from abc import ABC, abstractmethod


class TerminalCondition(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def reset(self, optional_data=None):
        raise NotImplementedError

    @abstractmethod
    def is_terminal(self, state, optional_data=None):
        raise NotImplementedError

    @abstractmethod
    def look_ahead(self, state, optional_data=None):
        raise NotImplementedError