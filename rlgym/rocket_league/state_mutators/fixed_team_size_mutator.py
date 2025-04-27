from typing import Dict, Any

import numpy as np

from rlgym.api import StateMutator
from rlgym.rocket_league.api import Car, GameState, PhysicsObject
from rlgym.rocket_league.common_values import BLUE_TEAM, OCTANE, ORANGE_TEAM


class FixedTeamSizeMutator(StateMutator[GameState]):
    """
    A StateMutator that initializes the game with a fixed number of cars on each team.
    """

    def __init__(self, blue_size=1, orange_size=1):
        self.blue_size = blue_size
        self.orange_size = orange_size

    def apply(self, state: GameState, shared_info: Dict[str, Any]) -> None:
        assert len(state.cars) == 0  # This mutator doesn't support other team size mutators

        for idx in range(self.blue_size):
            car = self._new_car()
            car.team_num = BLUE_TEAM
            state.cars['blue-{}'.format(idx)] = car

        for idx in range(self.orange_size):
            car = self._new_car()
            car.team_num = ORANGE_TEAM
            state.cars['orange-{}'.format(idx)] = car

    def _new_car(self) -> Car:
        car = Car()
        car.hitbox_type = OCTANE
        car.ball_touches = 0

        car.physics = PhysicsObject()

        car.demo_respawn_timer = 0.
        car.on_ground = True
        car.supersonic_time = 0.
        car.boost_amount = 0.
        car.boost_active_time = 0.
        car.handbrake = 0.

        car.has_jumped = False
        car.is_holding_jump = False
        car.is_jumping = False
        car.jump_time = 0.

        car.has_flipped = False
        car.has_double_jumped = False
        car.air_time_since_jump = 0.
        car.flip_time = 0.
        car.flip_torque = np.zeros(3, dtype=np.float32)

        car.is_autoflipping = False
        car.autoflip_timer = 0.
        car.autoflip_direction = 0.
        return car
