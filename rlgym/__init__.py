from rlgym.gym import Gym
from rlgym.distributed_gym import DistributedGym
from rlgym.envs import MatchFactory
import sys
import os

def make(env_name):
    match = MatchFactory.build_match(env_name)
    if match is None:
        RuntimeError('Invalid env_name', env_name)
    return Gym(match, pipe_id=os.getpid())


def make_distributed(env_names, wait_count=sys.maxsize, wait_ratio=1.0):
    return DistributedGym(env_names, wait_count, wait_ratio)