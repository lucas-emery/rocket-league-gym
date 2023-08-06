"""
    Object to contain all relevant information about the game state.
"""
import numpy as np
from dataclasses import dataclass
from typing import Dict, Generic

from rlgym.api.typing import AgentID
from rlgym.rocket_league.engine.car import Car
from rlgym.rocket_league.engine.game_config import GameConfig
from rlgym.rocket_league.engine.physics_object import PhysicsObject


@dataclass(init=False)
class GameState(Generic[AgentID]):
    blue_score: int
    orange_score: int
    config: GameConfig
    cars: Dict[AgentID, Car[AgentID]]
    ball: PhysicsObject
    inverted_ball: PhysicsObject
    # List of "booleans" (1 or 0)
    #TODO change type? do we want to expose timer too?
    # we can use the float to represent seconds until active and set to inf if disabled
    # Is pad size part of the state? I think not, can't even be modified
    boost_pads: np.ndarray
    inverted_boost_pads: np.ndarray

    __slots__ = tuple(__annotations__)

    def __init__(self):
        for attr in self.__slots__:
            self.__setattr__(attr, None)
