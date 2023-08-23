"""
    Object to contain all relevant information about the game state.
"""
import numpy as np
from dataclasses import dataclass
from typing import Dict, Generic, Optional

from rlgym.api import AgentID
from .car import Car
from .game_config import GameConfig
from .physics_object import PhysicsObject
from .utils import create_default_init


@dataclass(init=False)
class GameState(Generic[AgentID]):
    tick_count: int
    goal_scored: bool
    config: GameConfig
    cars: Dict[AgentID, Car[AgentID]]
    ball: PhysicsObject
    _inverted_ball: PhysicsObject
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
    def inverted_ball(self) -> PhysicsObject:
        if self._inverted_ball is None:
            self._inverted_ball = self.ball.inverted()
        return self._inverted_ball

    @property
    def inverted_boost_pad_timers(self) -> np.ndarray:
        if self._inverted_boost_pad_timers is None:
            self._inverted_boost_pad_timers = np.ascontiguousarray(self.boost_pad_timers[::-1])
        return self._inverted_boost_pad_timers
