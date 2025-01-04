from typing import List, Dict, Any

from rlgym.api import DoneCondition, AgentID
from rlgym.rocket_league.api import GameState
from rlgym.rocket_league.common_values import TICKS_PER_SECOND


class TimeoutCondition(DoneCondition[AgentID, GameState]):

    def __init__(self, timeout_seconds: float):
        """
        :param timeout_seconds: Timeout in seconds
        """

        self.timeout_seconds = timeout_seconds
        self.initial_tick = None

    def reset(self, agents: List[AgentID], initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        self.initial_tick = initial_state.tick_count

    def is_done(self, agents: List[AgentID], state: GameState, shared_info: Dict[str, Any]) -> Dict[AgentID, bool]:
        time_elapsed = (state.tick_count - self.initial_tick) / TICKS_PER_SECOND
        done = time_elapsed >= self.timeout_seconds
        return {agent: done for agent in agents}
