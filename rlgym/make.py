import os
from typing import List

from rlgym.envs import Match
from rlgym.utils import common_values
from rlgym.utils.terminal_conditions import common_conditions
from rlgym.utils.reward_functions import DefaultReward
from rlgym.utils.obs_builders import DefaultObs


def make(game_speed: int = 100,
         tick_skip: int = 8,
         spawn_opponents: bool = True,
         self_play: bool = False,
         random_resets: bool = False,
         team_size: int = 1,
         terminal_conditions: List[object] = (common_conditions.TimeoutCondition(225), common_conditions.GoalScoredCondition()),
         reward_fn: object = DefaultReward(),
         obs_builder: object = DefaultObs(),
         path_to_rl: str = None,
         use_injector: bool = False,
         force_paging: bool = False):
    """
    :param game_speed: The speed the physics will run at, leave it at 100 unless your game can't run at over 240fps
    :param tick_skip: The amount of physics ticks your action will be repeated for
    :param spawn_opponents: Whether you want opponents or not
    :param self_play: If there are agent controller opponents or not
    :param random_resets: If enabled cars and ball will spawn in random locations after every reset
    :param team_size: Cars per team
    :param terminal_conditions: List of terminal condition objects (rlgym.utils.TerminalCondition)
    :param reward_fn: Reward function object (rlgym.utils.RewardFunction)
    :param obs_builder: Observation builder object (rlgym.utils.ObsBuilder)
    :param path_to_rl: Path to RocketLeague executable, this is optional
    :param use_injector: Whether to use RLGym's bakkesmod injector or not. Enable if launching multiple instances
    :param force_paging: Enable forced paging of each spawned rocket league instance to reduce memory utilization
                             immediately, instead of allowing the OS to slowly page untouched allocations.
                             WARNING: This will require you to potentially expand your Windows Page File [1]
                             and it may substantially increase disk activity, leading to decreased disk lifetime.
                             Use at your own peril.
                             Default is off: OS dictates the behavior.
    :return: Gym object

    [1]: https://www.tomshardware.com/news/how-to-manage-virtual-memory-pagefile-windows-10,36929.html
    """

    # Imports are inside the function because setup fails otherwise (Missing win32file)
    from rlgym.gym import Gym
    from rlgym.version import print_current_release_notes

    print_current_release_notes()

    match = Match(team_size=team_size,
                  tick_skip=tick_skip,
                  game_speed=game_speed,
                  spawn_opponents=spawn_opponents,
                  random_resets=random_resets,
                  self_play=self_play,
                  reward_function=reward_fn,
                  terminal_conditions=terminal_conditions,
                  obs_builder=obs_builder)

    return Gym(match, pipe_id=os.getpid(), path_to_rl=path_to_rl, use_injector=use_injector, force_paging=force_paging)
