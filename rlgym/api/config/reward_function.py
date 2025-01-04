from abc import abstractmethod
from typing import Any, Dict, List, Generic
from ..typing import AgentID, RewardType, StateType


class RewardFunction(Generic[AgentID, StateType, RewardType]):
    """
    The reward function. This class is responsible for computing the reward for each agent in the environment.
    """

    @abstractmethod
    def reset(self, agents: List[AgentID], initial_state: StateType, shared_info: Dict[str, Any]) -> None:
        """
        Function to be called each time the environment is reset. This is meant to enable users to design stateful reward
        functions that maintain information about the game throughout an episode to determine a reward.

        :param agents: List of AgentIDs for which this RewardFunc will return a Reward
        :param initial_state: The initial state of the reset environment.
        :param shared_info: A dictionary with shared information across all config objects.
        """
        raise NotImplementedError

    @abstractmethod
    def get_rewards(self, agents: List[AgentID], state: StateType, is_terminated: Dict[AgentID, bool],
                    is_truncated: Dict[AgentID, bool], shared_info: Dict[str, Any]) -> Dict[AgentID, RewardType]:
        # TODO update docs
        """
        Function to compute the reward for a player. This function is given a player argument, and it is expected that
        the reward returned by this function will be for that player.

        :param agents: List of AgentIDs for which this RewardFunc should return a Reward
        :param state: The current state of the game.
        :param is_terminated: TODO.
        :param is_truncated: TODO.
        :param shared_info: A dictionary with shared information across all config objects.

        :return: A dict of rewards, one for each AgentID in agents.
        """
        raise NotImplementedError
