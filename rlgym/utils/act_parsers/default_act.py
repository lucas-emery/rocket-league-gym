import math
import numpy as np
import gym.spaces
from rlgym.utils import common_values
from rlgym.utils.gamestates import PlayerData, GameState
from rlgym.utils.act_parsers import ContinuousAct
from typing import Union, List


class DefaultAct(ContinuousAct):
    """
        Continuous Action space, that also accepts a few other input formats for QoL reasons and to remain
        compatible with older versions.
    """
    
    def __init__(self):
        super().__init__()

    def get_action_space(self) -> gym.spaces.Space:
        return super().get_action_space()

    def parse_actions(self, actions: Union[np.ndarray, List[np.ndarray], List[float]], state: GameState) -> np.ndarray:
        
        # allow other data types, this part should not be necessary but is nice to have in the default action parser.
        if type(actions) != np.ndarray:
            actions = np.asarray(actions)
        
        return super().parse_actions(actions)