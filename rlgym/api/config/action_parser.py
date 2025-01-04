from abc import abstractmethod
from typing import Any, Dict, Generic, List
from ..typing import AgentID, ActionType, EngineActionType, StateType, ActionSpaceType


class ActionParser(Generic[AgentID, ActionType, EngineActionType, StateType, ActionSpaceType]):
    """
    The action parser. This class is responsible for receiving actions from the agents and parsing them into a format
    supported by the TransitionEngine.
    """

    @abstractmethod
    def get_action_space(self, agent: AgentID) -> ActionSpaceType:
        """
        Function that returns the action space type. It will be called during the initialization of the environment.

        :return: The type of the action space
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self, agents: List[AgentID], initial_state: StateType, shared_info: Dict[str, Any]) -> None:
        """
        Function to be called each time the environment is reset.

        :param agents: List of AgentIDs for which this ActionParser will receive actions
        :param initial_state: The initial state of the reset environment.
        :param shared_info: A dictionary with shared information across all config objects.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_actions(self, actions: Dict[AgentID, ActionType], state: StateType, shared_info: Dict[str, Any]) \
            -> Dict[AgentID, EngineActionType]:
        # TODO update docs with new time dimension, array is now (ticks, actiondim=8)
        """
        Function that parses actions from the action space into a format that rlgym understands.
        The expected return value is a numpy float array of size (n, 8) where n is the number of agents.
        The second dimension is indexed as follows: throttle, steer, yaw, pitch, roll, jump, boost, handbrake.
        The first five values are expected to be in the range [-1, 1], while the last three values should be either 0 or 1.

        :param actions: An dict of actions, as passed to the `env.step` function.
        :param state: The GameState object of the current state that were used to generate the actions.
        :param shared_info: A dictionary with shared information across all config objects.

        :return: the parsed actions in the rlgym format.
        """
        raise NotImplementedError
