from abc import abstractmethod
from typing import Any, Dict, List, Generic
from ..typing import AgentID, ObsType, StateType, ObsSpaceType


class ObsBuilder(Generic[AgentID, ObsType, StateType, ObsSpaceType]):
    """
    The observation builder. This class is responsible for building observations for each agent in the environment.
    """

    @abstractmethod
    def get_obs_space(self, agent: AgentID) -> ObsSpaceType:
        """
        Function that returns the observation space type. It will be called during the initialization of the environment.

        :return: The type of the observation space
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self, agents: List[AgentID], initial_state: StateType, shared_info: Dict[str, Any]) -> None:
        """
        Function to be called each time the environment is reset. Note that this does not need to return anything,
        the environment will call `build_obs` automatically after reset, so the initial observation for a policy will be
        constructed in the same way as every other observation.

        :param agents: List of AgentIDs for which this ObsBuilder will return an Obs
        :param initial_state: The initial game state of the reset environment.
        :param shared_info: A dictionary with shared information across all config objects.
        """
        raise NotImplementedError

    @abstractmethod
    def build_obs(self, agents: List[AgentID], state: StateType, shared_info: Dict[str, Any]) -> Dict[AgentID, ObsType]:
        """
        Function to build observations for N agents. This is where observations will be constructed every step and
        every reset. This function is given the current state, and it is expected that the observations returned by this
        function will contain information from the perspective of each agent. This function is called only once per step.

        :param agents: List of AgentIDs for which this ObsBuilder should return an Obs
        :param state: The current state of the game.
        :param shared_info: A dictionary with shared information across all config objects.

        :return: An dictionary of observations, one for each AgentID in agents.
        """
        raise NotImplementedError
