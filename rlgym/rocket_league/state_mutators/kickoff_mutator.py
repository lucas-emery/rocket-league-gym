import random
from typing import Dict, Any

import numpy as np

from rlgym.api.config.state_mutator import StateMutator
from rlgym.rocket_league.common_values import BLUE_TEAM
from rlgym.rocket_league.engine.car import Car
from rlgym.rocket_league.engine.game_state import GameState


class KickoffMutator(StateMutator[GameState]):
    SPAWN_BLUE_POS = np.array([[-2048, -2560, 17], [2048, -2560, 17], [-256, -3840, 17], [256, -3840, 17], [0, -4608, 17]], dtype=np.float32)
    SPAWN_BLUE_YAW = [0.25 * np.pi, 0.75 * np.pi, 0.5 * np.pi, 0.5 * np.pi, 0.5 * np.pi]
    SPAWN_ORANGE_POS = np.array([[2048, 2560, 17], [-2048, 2560, 17], [256, 3840, 17], [-256, 3840, 17], [0, 4608, 17]], dtype=np.float32)
    SPAWN_ORANGE_YAW = [-0.75 * np.pi, -0.25 * np.pi, -0.5 * np.pi, -0.5 * np.pi, -0.5 * np.pi]

    def apply(self, state: GameState, shared_info: Dict[str, Any]) -> None:
        # possible kickoff indices are shuffled
        spawn_idx = [0, 1, 2, 3, 4]
        random.shuffle(spawn_idx)

        blue_count = 0
        orange_count = 0
        for car in state.cars.values():
            if car.team_num == BLUE_TEAM:
                # select a unique spawn state from pre-determined values
                pos = self.SPAWN_BLUE_POS[spawn_idx[blue_count]]
                yaw = self.SPAWN_BLUE_YAW[spawn_idx[blue_count]]
                blue_count += 1
            else:
                # select a unique spawn state from pre-determined values
                pos = self.SPAWN_ORANGE_POS[spawn_idx[orange_count]]
                yaw = self.SPAWN_ORANGE_YAW[spawn_idx[orange_count]]
                orange_count += 1

            car.physics.position = pos
            car.physics.euler_angles = np.array([0, yaw, 0], dtype=np.float32)
            car.boost_amount = 0.33
            
            self._fill_other_car_data(car)

    def _fill_other_car_data(self, car: Car):
        car.physics.linear_velocity = np.zeros(3, dtype=np.float32)
        car.physics.angular_velocity = np.zeros(3, dtype=np.float32)

        car.demo_respawn_timer = 0.
        car.on_ground = True
        car.supersonic_time = 0.
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
