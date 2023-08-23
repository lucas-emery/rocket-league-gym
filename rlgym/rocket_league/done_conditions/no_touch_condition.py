from typing import List, Dict, Any

from rlgym.api import DoneCondition, AgentID
from rlgym.rocket_league.api import GameState


class NoTouchTimeoutCondition(DoneCondition[AgentID, GameState]):

    def __init__(self, timeout: float, tick_rate=1/120):
        """
        :param timeout: Timeout in seconds
        """
        self.timeout = timeout
        self.tick_rate = tick_rate
        self.last_touch_tick = None

    def reset(self, initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        self.last_touch_tick = initial_state.tick_count

    def is_done(self, agents: List[AgentID], state: GameState, shared_info: Dict[str, Any]) -> Dict[AgentID, bool]:
        if any(car.ball_touches > 0 for car in state.cars.values()):
            self.last_touch_tick = state.tick_count
            done = False
        else:
            time_elapsed = (state.tick_count - self.last_touch_tick) * self.tick_rate
            done = time_elapsed >= self.timeout

        return {agent: done for agent in agents}
