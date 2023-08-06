from dataclasses import dataclass

from rlgym.rocket_league.engine.utils import create_default_init


@dataclass(init=False)
class GameConfig:
    gravity: float
    boost_consumption: float

    __slots__ = tuple(__annotations__)

    exec(create_default_init(__slots__))
