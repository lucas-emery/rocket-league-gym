from typing import List, Dict, Any

from rlgym.api.config.done_condition import DoneCondition
from rlgym.api.typing import AgentID
from rlgym.rocket_league.engine.game_state import GameState


class AllCondition(DoneCondition[AgentID, GameState]):

    def __init__(self, *conditions: DoneCondition):
        self.conditions = tuple(conditions)

    def reset(self, initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        for condition in self.conditions:
            condition.reset(initial_state, shared_info)

    def is_done(self, agents: List[AgentID], state: GameState, shared_info: Dict[str, Any]) -> Dict[AgentID, bool]:
        # TODO can we optimize this with numpy?
        combined_dones = {agent: False for agent in agents}
        for condition in self.conditions:
            dones = condition.is_done(agents, state, shared_info)
            for agent in agents:
                combined_dones[agent] &= dones[agent]

        return combined_dones
