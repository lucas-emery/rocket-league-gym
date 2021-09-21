import numpy as np
from typing import Dict

from rlgym.gym import Gym
from rlgym.utils import StateSetter
from rlgym.utils.gamestates import GameState
from rlgym.utils.state_setters import StateWrapper
from tests.utils.base_test import BaseTest


class _StateSetter(StateSetter):
    def __init__(self):
        super().__init__()
        self.initial_state = True

    def reset(self, state_wrapper: StateWrapper):
        if self.initial_state:
            self.initial_state = False
            state_wrapper.ball.set_pos(1000, 0, 100)
            state_wrapper.cars[0].set_pos(0, -4608, 17)
            state_wrapper.cars[0].set_rot(0, 0.5 * np.pi, 0)
            state_wrapper.cars[0].boost = 0
        else:
            state_wrapper.ball.set_pos(1000, 0, 100)
            state_wrapper.cars[0].set_pos(0, 4608, 17)
            state_wrapper.cars[0].set_rot(0, 0.5 * np.pi, 0)
            state_wrapper.cars[0].boost = 0


class BoostPadTest(BaseTest):
    def get_config(self) -> Dict:
        return {}

    def get_state_setter(self) -> StateSetter:
        return _StateSetter()

    def run(self, env: Gym):
        action = [0,0,0,0,0,0,0,0]
        state: GameState

        # Wait for 5 seconds
        for _ in range(15 * 5):
            state, _, _, _ = env.step(action)

        assert state.players[0].boost_amount == 0
        assert np.all(state.boost_pads)

        env.reset()

        assert state.players[0].boost_amount == 0
        assert np.all(state.boost_pads)

        # Wait for 5 seconds
        for _ in range(15 * 5):
            state, _, _, _ = env.step(action)

        assert state.players[0].boost_amount == 0
        assert np.all(state.boost_pads)
