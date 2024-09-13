from typing import List, Dict, Any

from rlgym.api import DoneCondition, AgentID
from rlgym.rocket_league.api import GameState


class AllCondition(DoneCondition[AgentID, GameState]):
    """
    A DoneCondition that is satisfied when all the provided conditions are satisfied.
    """
    def __init__(self, *conditions: DoneCondition):
        self.conditions = tuple(conditions)

    def reset(self, agents: List[AgentID], initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        for condition in self.conditions:
            condition.reset(agents, initial_state, shared_info)

    def is_done(self, agents: List[AgentID], state: GameState, shared_info: Dict[str, Any]) -> Dict[AgentID, bool]:
        # TODO can we optimize this with numpy?
        combined_dones = {agent: False for agent in agents}
        for condition in self.conditions:
            dones = condition.is_done(agents, state, shared_info)
            for agent, done in dones.items():
                combined_dones[agent] &= done

        return combined_dones
