import numpy as np

from dataclasses import dataclass
from typing import Optional, Generic

from rlgym.api.typing import AgentID
from rlgym.rocket_league.engine.physics_object import PhysicsObject


@dataclass(init=False)
class Car(Generic[AgentID]):

    # Misc Data
    team_num: int
    hitbox_type: int  # TODO Match to enum somewhere, should probably be typed?
    ball_touches: int  # number of ball touches since last state was sent
    bump_victim_id: Optional[AgentID]

    # Actual State
    demo_respawn_timer: float  # 0 if alive
    num_wheels_contact: int  # Needed for stuff like AutoRoll and some steering shenanigans
    on_ground: bool  # this is just numWheelsContact >=3
    supersonic_time: float  # greater than 0 when supersonic, needed for state set since ssonic threshold changes with time
    boost_amount: float
    boost_active_time: float  # you're forced to boost for at least 12 ticks
    handbreak: float

    # Jump Stuff
    has_jumped: bool
    is_holding_jump: bool  # whether you pressed jump last tick or not
    is_jumping: bool  # changes to false after max jump time
    jump_time: float  # need jump time for state set, doesn't reset to 0 because of psyonix's landing jump cooldown

    # Flip Stuff
    has_flipped: bool
    has_dbl_jumped: bool
    air_time_since_jump: float
    can_flip: bool  # this is a combination of not dbljumped, not flipped and airtime < max_time
    is_flipping: bool
    flip_time: float
    flip_torque: np.ndarray

    # AutoFlip Stuff - What helps you recover from turtling
    is_autoflipping: bool
    autoflip_timer: float
    autoflip_direction: int  # 1 or -1, determines roll direction

    physics: PhysicsObject
    inverted_physics: PhysicsObject

    __slots__ = tuple(__annotations__)

    def __init__(self):
        for attr in self.__slots__:
            self.__setattr__(attr, None)
