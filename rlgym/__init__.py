from rlgym.gym import Gym
from rlgym.distributed_gym import DistributedGym
from rlgym.envs import MatchFactory

from rlgym.envs import Match
from rlgym.utils import CommonValues
from rlgym.utils.terminal_conditions import CommonConditions
from rlgym.utils.reward_functions import ShootBallReward
from rlgym.utils.obs_builders import RhobotObs
from rlgym.communication import CommunicationHandler

import os

def make(env_name, custom_args=None):
    match = MatchFactory.build_match(env_name, custom_args=custom_args)
    if match is None:
        RuntimeError("RLGym was unable to construct match!\n"
                     "Match ID: {}\n"
                     "Custom match params: {}".format(env_name, custom_args))

    return Gym(match, pipe_id=os.getpid())

def make_distributed(env_names, custom_arg_dicts=None):
    envs = []
    for i in range(len(env_names)):
        name = env_names[i]
        args = custom_arg_dicts[i]
        match = MatchFactory.build_match(name, custom_args=args)
        if match is not None:
            env = Gym(match, pipe_id=i)
            envs.append(env)
        else:
            RuntimeError("RLGym was unable to construct match while building matches for distributed env!"
                  "\nMatch ID: {}"
                  "\nCustom match params: {}".format(name, args))

    if len(envs) == 0:
        raise RuntimeError("RLGym was unable to build any matches for distributed env!")

    return DistributedGym(envs)