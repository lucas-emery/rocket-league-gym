import math
from typing import Any, List

import numpy as np

from rlgym.utils import common_values
from rlgym.utils.gamestates import GameState, PhysicsObject, PlayerData
from rlgym.utils.obs_builders import ObsBuilder


class AdvancedObs(ObsBuilder):
    POS_STD = (
        2300  # If you read this and wonder why, ping Rangler in the dead of night.
    )
    ANG_STD = math.pi

    def __init__(self, std_boost: bool = False):
        super().__init__()
        self.BOOST_STD = 100 if std_boost else 1

    def reset(self, initial_state: GameState):
        pass

    def build_obs(
        self, player: PlayerData, state: GameState, previous_action: np.ndarray
    ) -> Any:
        if player.team_num == common_values.ORANGE_TEAM:
            inverted = True
            ball = state.inverted_ball
            pads = state.inverted_boost_pads
        else:
            inverted = False
            ball = state.ball
            pads = state.boost_pads

        obs = [
            ball.position / self.POS_STD,
            ball.linear_velocity / self.POS_STD,
            ball.angular_velocity / self.ANG_STD,
            previous_action,
            pads,
        ]

        player_car = self._add_player_to_obs(obs, player, ball, inverted)

        allies = []
        enemies = []

        for other in state.players:
            if other.car_id == player.car_id:
                continue

            team_obs = allies if other.team_num == player.team_num else enemies
            other_car = self._add_player_to_obs(team_obs, other, ball, inverted)

            # Extra info
            team_obs.extend(
                [
                    (other_car.position - player_car.position) / self.POS_STD,
                    (other_car.linear_velocity - player_car.linear_velocity)
                    / self.POS_STD,
                ]
            )

        obs.extend(allies)
        obs.extend(enemies)
        return np.concatenate(obs)

    def _add_player_to_obs(
        self, obs: List, player: PlayerData, ball: PhysicsObject, inverted: bool
    ):
        player_car = player.inverted_car_data if inverted else player.car_data
        rel_pos = ball.position - player_car.position
        rel_vel = ball.linear_velocity - player_car.linear_velocity

        obs.extend(
            [
                rel_pos / self.POS_STD,
                rel_vel / self.POS_STD,
                player_car.position / self.POS_STD,
                player_car.forward(),
                player_car.up(),
                player_car.linear_velocity / self.POS_STD,
                player_car.angular_velocity / self.ANG_STD,
                [
                    player.boost_amount / self.BOOST_STD,
                    int(player.on_ground),
                    int(player.has_flip),
                    int(player.is_demoed),
                ],
            ]
        )

        return player_car
