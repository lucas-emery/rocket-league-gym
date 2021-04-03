from typing import Union, List, Tuple, Dict

import numpy as np
from gym import Env

from rlgym.gym import Gym


class SingleAgentGym(Env):
    """
    Single agent version of the RL Gym (compatible with stable baselines)
    Simply gets the observation and reward for a single agent at each step
    """

    def __init__(self, env: Gym, index=0):
        super().__init__()
        self.env = env
        self.index = index
        self.observation_space = env.observation_space
        self.action_space = env.action_space

    def step(self, actions: Union[np.ndarray, List[np.ndarray], List[float]]) -> Tuple[List, List, bool, Dict]:
        obs, reward, done, info = self.env.step(actions)
        return obs[self.index], reward[self.index], done, info

    def reset(self) -> List:
        res = self.env.reset()
        return res[self.index]

    def render(self, mode='human'):
        self.env.render(mode)
