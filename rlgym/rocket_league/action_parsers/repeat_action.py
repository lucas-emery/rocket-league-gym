from typing import Dict, Any, List

import numpy as np

from rlgym.api import ActionParser, ActionType, StateType, ActionSpaceType, AgentID


class RepeatAction(ActionParser[AgentID, ActionType, np.ndarray, StateType, ActionSpaceType]):
    """
    A simple wrapper to emulate tick skip.

    Repeats every action for a specified number of ticks.
    """

    def __init__(self,
                 parser: ActionParser[AgentID, ActionType, np.ndarray, StateType, ActionSpaceType],
                 repeats=8):
        super().__init__()
        self.parser = parser
        self.repeats = repeats

    def get_action_space(self, agent: AgentID) -> ActionSpaceType:
        return self.parser.get_action_space(agent)

    def reset(self, agents: List[AgentID], initial_state: StateType, shared_info: Dict[str, Any]) -> None:
        self.parser.reset(agents, initial_state, shared_info)

    def parse_actions(self, actions: Dict[AgentID, ActionType], state: StateType, shared_info: Dict[str, Any]) -> Dict[AgentID, np.ndarray]:
        rlgym_actions = self.parser.parse_actions(actions, state, shared_info)
        repeat_actions = {}
        for agent, action in rlgym_actions.items():
            if action.shape == (8,):
                action = np.expand_dims(action, axis=0)
            elif action.shape != (1, 8):
                raise ValueError(f"Expected action to have shape (8,) or (1,8), got {action.shape}")

            repeat_actions[agent] = action.repeat(self.repeats, axis=0)

        return repeat_actions
