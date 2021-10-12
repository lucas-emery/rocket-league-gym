import math
import numpy as np
import gym.spaces
from rlgym.utils import common_values
from rlgym.utils.gamestates import GameState
from rlgym.utils.action_parsers import ActionParser


class ContinuousAction(ActionParser):
    """
        Simple continuous action space. Operates in the range -1 to 1, even for the binary actions which are converted back to binary later.
        This is for improved compatibility, stable baselines doesn't support tuple spaces right now.
    """

    def __init__(self):
        super().__init__()

    def get_action_space(self) -> gym.spaces.Space:
        # return gym.spaces.Tuple((gym.spaces.Box(-1, 1, shape=(5,)), gym.spaces.MultiBinary(3)))
        return gym.spaces.Box(-1, 1, shape=(common_values.NUM_ACTIONS,))

    def parse_actions(self, actions: np.ndarray, state: GameState) -> np.ndarray:
        actions = actions.reshape((-1, 8))

        actions[..., :5] = actions[..., :5].clip(-1, 1)
        # The final 3 actions handle are jump, boost and handbrake. They are inherently discrete so we convert them to either 0 or 1.
        actions[..., 5:] = actions[..., 5:] > 0

        return actions
