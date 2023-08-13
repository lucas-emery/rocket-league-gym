from typing import Dict, Any

import numpy as np

from rlgym.api.config.action_parser import ActionParser
from rlgym.api.typing import SpaceType, AgentID
from rlgym.rocket_league.engine.game_state import GameState


class RepeatAction(ActionParser[AgentID, np.ndarray, np.ndarray, GameState, SpaceType]):
    """
    A simple wrapper to emulate tick skip
    """

    def __init__(self,
                 parser: ActionParser[AgentID, np.ndarray, np.ndarray, GameState, SpaceType],
                 repeats=8):
        super().__init__()
        self.parser = parser
        self.repeats = repeats

    def get_action_space(self, agent: AgentID) -> SpaceType:
        return self.parser.get_action_space(agent)

    def reset(self, initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        pass

    def parse_actions(self, actions: Dict[AgentID, np.ndarray], state: GameState, shared_info: Dict[str, Any]) -> Dict[AgentID, np.ndarray]:
        repeat_actions = {}
        for agent, action in actions.items():
            # Action can have shape (ActionSpace)
            assert len(action.shape) == 1

            repeat_actions[agent] = np.expand_dims(action, axis=0).repeat(self.repeats, axis=0)

        return self.parser.parse_actions(repeat_actions, state, shared_info)
