from dataclasses import dataclass
from typing import Optional, Generic, Tuple

import numpy as np
from rlgym.api import AgentID

from .physics_object import PhysicsObject
from .utils import create_default_init
from ..common_values import DOUBLEJUMP_MAX_DELAY, FLIP_TORQUE_TIME, BLUE_TEAM, ORANGE_TEAM


@dataclass(init=False)
class Car(Generic[AgentID]):
    # Misc Data
    team_num: int  # the team of this car, constants in common_values.py
    hitbox_type: int  # the hitbox of this car, constants in common_values.py
    ball_touches: int  # number of ball touches since last state was sent
    bump_victim_id: Optional[AgentID]  # The agent ID of the car you had car contact with if any

    # Actual State
    demo_respawn_timer: float  # time, in seconds, until respawn, or 0 if alive (in [0,3] unless changed in mutator config)
    wheels_with_contact: Tuple[bool, bool, bool, bool]  # front_left, front_right, back_left, back_right
    supersonic_time: float  # time, in seconds, since car entered supersonic state (reset to 0 when exited supersonic state) (in [0, infinity) but only relevant values are in [0,1] (1 comes from SUPERSONIC_MAINTAIN_MAX_TIME in RLConst.h))
    boost_amount: float  # (in [0,100])
    boost_active_time: float  # time, in seconds, since car started pressing boost (reset to 0 when boosting stops) (in [0, infinity) but only relevant values are in [0,0.1] (0.1 comes from BOOST_MIN_TIME in RLConst.h))
    handbrake: float  # indicates the magnitude of the handbrake, which ramps up and down when handbrake is pressed/released (in [0,1])

    # Jump Stuff
    is_jumping: bool  # whether the car is currently jumping (you gain a little extra velocity while holding jump)
    has_jumped: bool  # whether the car has jumped since last time it was on ground
    is_holding_jump: bool  # whether you pressed jump last tick or not
    jump_time: float  # time, in seconds, since jump was pressed while car was on ground, clamped to 0.2 (reset to 0 when car presses jump while on ground) (in [0,0.2] (0.2 comes from JUMP_MAX_TIME in RLConst.h))

    # Flip Stuff
    has_flipped: bool  # whether the car has flipped since last time it was on ground
    has_double_jumped: bool  # whether the car has double jumped since last time it was on ground
    air_time_since_jump: float  # time, in seconds, since a jump off ground ended (reset to 0 when car is on ground or has not jumped or is jumping) (in [0, infinity) but only relevant values are in [0,1.25] (1.25 comes from DOUBLEJUMP_MAX_DELAY in RLConst.h))
    flip_time: float  # time, in seconds, since flip (or stall) was initiated (reset to 0 when car is on ground) (in [0, infinity) but only relevant values are in [0, 0.95] (0.95 comes from FLIP_TORQUE_TIME + FLIP_PITCHLOCK_EXTRA_TIME in RLConst.h))
    flip_torque: np.ndarray  # torque applied to the car for the duration of the flip (in [0,1])

    # AutoFlip Stuff - What helps you recover from turtling
    is_autoflipping: bool  # changes to false after max autoflip time
    autoflip_timer: float  # time, in seconds, until autoflip force ends (in [0,0.4] (0.4 comes from CAR_AUTOFLIP_TIME in RLConst.h))
    autoflip_direction: float  # 1 or -1, determines roll direction

    # Physics
    physics: PhysicsObject
    _inverted_physics: PhysicsObject  # Cache for inverted physics

    __slots__ = tuple(__annotations__)

    exec(create_default_init(__slots__))

    @property
    def is_blue(self) -> bool:
        return self.team_num == BLUE_TEAM

    @property
    def is_orange(self) -> bool:
        return self.team_num == ORANGE_TEAM

    @property
    def is_demoed(self) -> bool:
        return self.demo_respawn_timer > 0

    @property
    def is_boosting(self) -> bool:
        return self.boost_active_time > 0

    @property
    def is_supersonic(self) -> bool:
        return self.supersonic_time > 0

    @property
    def on_ground(self) -> bool:
        return sum(self.wheels_with_contact) >= 3

    @on_ground.setter
    def on_ground(self, value: bool):
        self.wheels_with_contact = (value, value, value, value)

    @property
    def has_flip(self) -> bool:
        return not self.has_double_jumped and not self.has_flipped and self.air_time_since_jump < DOUBLEJUMP_MAX_DELAY

    @property
    def can_flip(self) -> bool:
        return not self.on_ground and not self.is_holding_jump and self.has_flip

    @property
    def is_flipping(self) -> bool:
        return self.has_flipped and self.flip_time < FLIP_TORQUE_TIME

    @is_flipping.setter
    def is_flipping(self, value: bool):
        if value:
            self.has_flipped = True
            if self.flip_time >= FLIP_TORQUE_TIME:
                self.flip_time = 0
        else:
            self.flip_time = FLIP_TORQUE_TIME

    @property
    def had_car_contact(self) -> bool:
        return self.bump_victim_id is not None

    @property
    def inverted_physics(self) -> PhysicsObject:
        if self._inverted_physics is None:
            self._inverted_physics = self.physics.inverted()
        return self._inverted_physics
