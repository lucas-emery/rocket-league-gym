from dataclasses import dataclass


@dataclass(init=False)
class GameConfig:
    gravity: float
    boost_consumption: float

    __slots__ = tuple(__annotations__)

    def __init__(self):
        for attr in self.__slots__:
            self.__setattr__(attr, None)
