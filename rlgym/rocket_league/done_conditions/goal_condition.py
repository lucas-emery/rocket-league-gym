from typing import List, Dict, Any

from rlgym.api.config.done_condition import DoneCondition
from rlgym.api.typing import AgentID
from rlgym.rocket_league.engine.game_state import GameState


class GoalCondition(DoneCondition[AgentID, GameState]):
    def reset(self, initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        pass

    def is_done(self, agents: List[AgentID], state: GameState, shared_info: Dict[str, Any]) -> Dict[AgentID, bool]:
        return {agent: state.goal_scored for agent in agents}
