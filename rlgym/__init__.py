from rlgym.gym import Gym
from rlgym.distributed_gym import DistributedGym
from rlgym.envs.duel import Duel
from rlgym.envs.doubles import Doubles
from rlgym.envs.standard import Standard
import sys
import time


def make(env_name):
    if env_name == 'Duel':
        env = Duel(False)
    elif env_name == 'DuelSelf':
        env = Duel(True)
    elif env_name == 'Doubles':
        env = Doubles(False)
    elif env_name == 'DoublesSelf':
        env = Doubles(True)
    elif env_name == 'Standard':
        env = Standard(False)
    elif env_name == 'StandardSelf':
        env = Standard(True)
    else:
        raise RuntimeError('Invalid env_name', env_name)
    return Gym(env, pipe_id=time.time())


def make_distributed(env_names, wait_count=sys.maxsize, wait_ratio=1.0):
    return DistributedGym(env_names, wait_count, wait_ratio)