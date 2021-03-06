from abc import ABC, abstractmethod


class RewardFunction(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def reset(self, optional_data=None):
        raise NotImplementedError

    @abstractmethod
    def get_reward(self, player, state, optional_data=None):
        raise NotImplementedError

    @abstractmethod
    def get_final_reward(self, player, state, optional_data=None):
        raise NotImplementedError