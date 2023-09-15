import math
from typing import Any, List

import numpy as np

from rlgym.utils import common_values
from rlgym.utils.gamestates import GameState, PlayerData
from rlgym.utils.obs_builders import ObsBuilder


class DefaultObs(ObsBuilder):
    def __init__(
        self,
        pos_coef=1 / 2300,
        ang_coef=1 / math.pi,
        lin_vel_coef=1 / 2300,
        ang_vel_coef=1 / math.pi,
        boost_coef: float = 1,
    ):
        """
        :param pos_coef: Position normalization coefficient
        :param ang_coef: Rotation angle normalization coefficient
        :param lin_vel_coef: Linear velocity normalization coefficient
        :param ang_vel_coef: Angular velocity normalization coefficient
        :param boost_coef: Boost normalization coefficient
        """
        super().__init__()
        self.POS_COEF = pos_coef
        self.ANG_COEF = ang_coef
        self.LIN_VEL_COEF = lin_vel_coef
        self.ANG_VEL_COEF = ang_vel_coef
        self.BOOST_COEF = boost_coef

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
            ball.position * self.POS_COEF,
            ball.linear_velocity * self.LIN_VEL_COEF,
            ball.angular_velocity * self.ANG_VEL_COEF,
            previous_action,
            pads,
        ]

        self._add_player_to_obs(obs, player, inverted)

        allies = []
        enemies = []

        for other in state.players:
            if other.car_id == player.car_id:
                continue

            team_obs = allies if other.team_num == player.team_num else enemies
            self._add_player_to_obs(team_obs, other, inverted)

        obs.extend(allies)
        obs.extend(enemies)
        return np.concatenate(obs)

    def _add_player_to_obs(self, obs: List, player: PlayerData, inverted: bool):
        player_car = player.inverted_car_data if inverted else player.car_data
        obs.extend(
            [
                player_car.position * self.POS_COEF,
                player_car.forward(),
                player_car.up(),
                player_car.linear_velocity * self.LIN_VEL_COEF,
                player_car.angular_velocity * self.ANG_VEL_COEF,
                [
                    player.boost_amount * self.BOOST_COEF,
                    int(player.on_ground),
                    int(player.has_flip),
                    int(player.is_demoed),
                ],
            ]
        )

        return player_car
