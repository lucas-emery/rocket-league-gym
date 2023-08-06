"""
A termination/truncation condition.
"""
from abc import abstractmethod
from typing import Any, Dict, List, Generic
from rlgym.api.typing import AgentID, StateType


class DoneCondition(Generic[AgentID, StateType]):

    @abstractmethod
    def reset(self, initial_state: StateType, shared_info: Dict[str, Any]) -> None:
        """
        Function to be called each time the environment is reset.

        :param initial_state: The initial state of the reset environment.
        :param shared_info: A dictionary with shared information across all config objects.
        """
        raise NotImplementedError

    @abstractmethod
    def is_done(self, agents: List[AgentID], current_state: StateType, shared_info: Dict[str, Any]) -> Dict[AgentID, bool]:
        #TODO update docs, now evals for each agent and returns Dict
        """
        Function to determine if a game state is terminal. This will be called once per step, and must return either
        `True` or `False` if the current episode should be terminated at this state.

        :param agents: List of AgentIDs for which this DoneCondition should be evaluated
        :param current_state: The current state of the game.
        :param shared_info: A dictionary with shared information across all config objects.

        :return: Dict of bools representing whether the current state meets this done condition for each AgentID in agents.
        """
        raise NotImplementedError

