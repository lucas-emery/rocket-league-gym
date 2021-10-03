import math
import numpy as np
import gym.spaces
from rlgym.utils import common_values
from rlgym.utils.gamestates import PlayerData, GameState
from rlgym.utils.act_parsers import ActParser

class DiscreteAct(ActParser):
    """
        Simple discrete action space. All the analog actions have 3 bins: -1, 0 and 1.
    """

    def __init__(self):
        super().__init__()

    def get_action_space(self) -> gym.spaces.Space:
        return gym.spaces.MultiDiscrete([3, 3, 3, 3, 3, 2, 2, 2])


    def parse_actions(self, actions: np.ndarray) -> np.ndarray:
        actions = actions.reshape((-1, 8))

        # map all ternary actions from {0, 1, 2} to {-1, 0, 1}.
        actions[..., :5] = actions[..., :5] - 1

        return actions
