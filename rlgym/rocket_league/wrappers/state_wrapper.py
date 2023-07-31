from typing import Dict, TypeVar

from rlgym.rocket_league.wrappers.ball_wrapper import BallWrapper
from rlgym.rocket_league.wrappers.car_wrapper import CarWrapper

AgentID = TypeVar("AgentID", bound=str)


class StateWrapper:
    gravity: float
    boost_consumption: float
    ball: BallWrapper
    cars: Dict[AgentID, CarWrapper]
