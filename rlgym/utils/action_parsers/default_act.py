import numpy as np
import gym.spaces
from rlgym.utils.gamestates import GameState
from rlgym.utils.action_parsers import ContinuousAction
from typing import Union, List


class DefaultAction(ContinuousAction):
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

        if len(actions.shape) == 1:
            actions = actions.reshape((-1, 8))
        elif len(actions.shape) > 2:
            raise ValueError('{} is not a valid action shape'.format(actions.shape))
        
        return super().parse_actions(actions, state)
