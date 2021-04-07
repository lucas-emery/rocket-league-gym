import os
from typing import List


def make(env_name: str,
         ep_len_minutes: float = None,
         game_speed: int = None,
         tick_skip: int = None,
         spawn_opponents: bool = None,
         random_resets: bool = None,
         team_size: int = None,
         terminal_conditions: List[object] = None,
         reward_fn: object = None,
         obs_builder: object = None,
         path_to_rl: str = None,
         use_injector: bool = False):
    """
    :param env_name: Name of your env, can be any of (Custom, Duel, Doubles, Standard, Basic) with or without Self
    :param ep_len_minutes: The episode length in minutes, seconds granularity can be achieved with a float
    :param game_speed: The speed the physics will run at, leave it at 100 unless your game can't run at over 240fps
    :param tick_skip: The amount of physics ticks your action will be repeated for
    :param spawn_opponents: Whether you want opponents or not
    :param random_resets: If enabled cars and ball will spawn in random locations after every reset
    :param team_size: Cars per team
    :param terminal_conditions: List of terminal condition objects (rlgym.utils.TerminalCondition)
    :param reward_fn: Reward function object (rlgym.utils.RewardFunction)
    :param obs_builder: Observation builder object (rlgym.utils.ObsBuilder)
    :param path_to_rl: Path to RocketLeague executable, this is optional
    :param use_injector: Whether to use a custom injector or not
    :return: Gym object
    """

    # Imports are inside the function because setup fails otherwise (Missing win32file)
    from rlgym.gym import Gym
    from rlgym.envs import match_factory
    from rlgym.version import print_current_release_notes

    print_current_release_notes()

    custom_args = dict(ep_len_minutes=ep_len_minutes, game_speed=game_speed, tick_skip=tick_skip,
                       spawn_opponents=spawn_opponents, random_resets=random_resets, team_size=team_size,
                       terminal_conditions=terminal_conditions, reward_fn=reward_fn, obs_builder=obs_builder)
    match = match_factory.build_match(env_name, **custom_args)
    if match is None:
        raise ValueError("RLGym was unable to construct match!\n"
                         "Match ID: {}\n"
                         "Custom match params: {}".format(env_name, custom_args))

    return Gym(match, pipe_id=os.getpid(), path_to_rl=path_to_rl, use_injector=use_injector)