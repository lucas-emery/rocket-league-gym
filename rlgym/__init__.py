from rlgym.gym import Gym
from rlgym.distributed_gym import DistributedGym
from rlgym.envs.duel import Duel
from rlgym.envs.doubles import Doubles
from rlgym.envs.standard import Standard
import sys
import time


def _get_env(env_name):
    if env_name == 'Duel':
        return Duel(False)
    elif env_name == 'DuelSelf':
        return Duel(True)
    elif env_name == 'Doubles':
        return Doubles(False)
    elif env_name == 'DoublesSelf':
        return Doubles(True)
    elif env_name == 'Standard':
        return Standard(False)
    elif env_name == 'StandardSelf':
        return Standard(True)
    else:
        raise RuntimeError('Invalid env_name', env_name)


def make(env_name):
    return Gym(_get_env(env_name), pipe_id=time.time())


def make_distributed(env_name):
    return DistributedGym(env_name)
