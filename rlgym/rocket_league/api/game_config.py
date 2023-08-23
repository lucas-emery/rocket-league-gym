from dataclasses import dataclass

from .utils import create_default_init


@dataclass(init=False)
class GameConfig:
    gravity: float
    boost_consumption: float
    dodge_deadzone: float

    __slots__ = tuple(__annotations__)

    exec(create_default_init(__slots__))
