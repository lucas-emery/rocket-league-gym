from typing import Any

import numpy as np

from rlgym.utils import ObsBuilder
from rlgym.utils.gamestates import PlayerData, GameState


class StateObs(ObsBuilder):
    def reset(self, initial_state: GameState):
        pass

    def build_obs(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> Any:
        return state
