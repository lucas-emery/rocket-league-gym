"""
    Object to contain all relevant information about the game state.
"""
import numpy as np
from dataclasses import dataclass
from typing import Dict, Generic, Optional

from rlgym.api.typing import AgentID
from rlgym.rocket_league.engine.car import Car
from rlgym.rocket_league.engine.game_config import GameConfig
from rlgym.rocket_league.engine.physics_object import PhysicsObject
from rlgym.rocket_league.engine.utils import create_default_init


@dataclass(init=False)
class GameState(Generic[AgentID]):
    goal_scored: bool
    config: GameConfig
    cars: Dict[AgentID, Car[AgentID]]
    ball: PhysicsObject
    inverted_ball: PhysicsObject
    boost_pad_timers: np.ndarray
    _inverted_boost_pad_timers: np.ndarray

    __slots__ = tuple(__annotations__)

    exec(create_default_init(__slots__))

    @property
    def scoring_team(self) -> Optional[int]:
        if self.goal_scored:
            return 0 if self.ball.position[1] > 0 else 1
        return None

    @property
    def inverted_boost_pad_timers(self):
        if self._inverted_boost_pad_timers is None:
            self._inverted_boost_pad_timers = np.ascontiguousarray(self.boost_pad_timers[::-1])
        return self._inverted_boost_pad_timers
