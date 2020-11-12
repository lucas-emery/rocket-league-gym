from rlgym.gym import Gym
from rlgym.distributed_gym import DistributedGym
from rlgym.envs import MatchFactory

from rlgym.envs import Match
from rlgym.utils import CommonValues
from rlgym.utils.terminal_conditions import CommonConditions
from rlgym.utils.reward_functions import ShootBallReward
from rlgym.utils.obs_builders import RhobotObs

import sys
import os

def make(env_name, custom_args=None):
    match = MatchFactory.build_match(env_name, custom_args=custom_args)
    if match is None:
        RuntimeError("RLGym was unable to construct match!\nMatch ID: {}\nCustom match params: {}".format(env_name, custom_args))
    return Gym(match, pipe_id=os.getpid())


def make_distributed(env_names, wait_count=sys.maxsize, wait_ratio=1.0):
    return DistributedGym(env_names, wait_count, wait_ratio)