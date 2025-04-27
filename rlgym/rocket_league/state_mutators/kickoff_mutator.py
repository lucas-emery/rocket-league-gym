import random
from typing import Dict, Any

import numpy as np

from rlgym.api import StateMutator
from rlgym.rocket_league.api import GameState
from rlgym.rocket_league.common_values import BLUE_TEAM, BALL_RESTING_HEIGHT


class KickoffMutator(StateMutator[GameState]):
    """
    A StateMutator that sets up the game state for a kickoff.
    """

    SPAWN_BLUE_POS = np.array([[-2048, -2560, 17], [2048, -2560, 17], [-256, -3840, 17], [256, -3840, 17], [0, -4608, 17]], dtype=np.float32)
    SPAWN_BLUE_YAW = [0.25 * np.pi, 0.75 * np.pi, 0.5 * np.pi, 0.5 * np.pi, 0.5 * np.pi]
    SPAWN_ORANGE_POS = np.array([[2048, 2560, 17], [-2048, 2560, 17], [256, 3840, 17], [-256, 3840, 17], [0, 4608, 17]], dtype=np.float32)
    SPAWN_ORANGE_YAW = [-0.75 * np.pi, -0.25 * np.pi, -0.5 * np.pi, -0.5 * np.pi, -0.5 * np.pi]

    def apply(self, state: GameState, shared_info: Dict[str, Any]) -> None:
        # Put ball in center
        state.ball.position = np.array([0, 0, BALL_RESTING_HEIGHT], dtype=np.float32)
        state.ball.linear_velocity = np.zeros(3, dtype=np.float32)
        state.ball.angular_velocity = np.zeros(3, dtype=np.float32)

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

            car.physics.position = pos.copy()  # Copy so users can freely modify in subsequent mutators
            car.physics.linear_velocity = np.zeros(3, dtype=np.float32)
            car.physics.angular_velocity = np.zeros(3, dtype=np.float32)
            car.physics.euler_angles = np.array([0, yaw, 0], dtype=np.float32)
            car.boost_amount = 33.3
