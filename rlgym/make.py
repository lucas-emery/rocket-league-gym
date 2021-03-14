import os
from typing import Dict


def make(env_name: str, custom_args: Dict = None, path_to_rl: str = None):
    # Imports are inside the function because setup fails otherwise (Missing win32file)
    from rlgym.gym import Gym
    from rlgym.envs import match_factory
    from rlgym.version import print_current_release_notes

    print_current_release_notes()

    match = match_factory.build_match(env_name, custom_args=custom_args)
    if match is None:
        raise ValueError("RLGym was unable to construct match!\n"
                     "Match ID: {}\n"
                     "Custom match params: {}".format(env_name, custom_args))

    return Gym(match, pipe_id=os.getpid(), path_to_rl=path_to_rl)


# FIXME i think this doesn't work [env = Gym]
def make_distributed(env_names, custom_arg_dicts=None, path_to_rl=None):
    from rlgym.gym import Gym
    from rlgym.distributed_gym import DistributedGym
    from rlgym.envs import match_factory
    from rlgym.version import print_current_release_notes

    print_current_release_notes()

    envs = []
    for i in range(len(env_names)):
        name = env_names[i]
        args = custom_arg_dicts[i]
        match = match_factory.build_match(name, custom_args=args)
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