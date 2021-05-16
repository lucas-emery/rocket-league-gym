from rlgym.gym import Gym
from rlgym.wrappers.pettingzoo_wrapper import PettingZooWrapper
from ray.rllib.env.wrappers.pettingzoo_env import PettingZooEnv


def rllib_wrapper(env: Gym):
    """Preliminary solution"""
    return PettingZooEnv(PettingZooWrapper(env))
