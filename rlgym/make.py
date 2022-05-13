import os
from typing import List
from warnings import warn

from rlgym.envs import Match
from rlgym.gamelaunch import LaunchPreference
from rlgym.utils.terminal_conditions import common_conditions
from rlgym.utils.reward_functions import DefaultReward
from rlgym.utils.obs_builders import DefaultObs
from rlgym.utils.action_parsers import DefaultAction
from rlgym.utils.state_setters import DefaultState


def make(game_speed: int = 100,
         tick_skip: int = 8,
         spawn_opponents: bool = False,
         self_play = None,
         team_size: int = 1,
         gravity: float = 1,
         boost_consumption: float = 1,
         terminal_conditions: List[object] = (common_conditions.TimeoutCondition(225), common_conditions.GoalScoredCondition()),
         reward_fn: object = DefaultReward(),
         obs_builder: object = DefaultObs(),
         action_parser: object = DefaultAction(),
         state_setter: object = DefaultState(),
         launch_preference: str = LaunchPreference.EPIC,
         use_injector: bool = False,
         force_paging: bool = False,
         raise_on_crash: bool = False,
         auto_minimize: bool = False):
    """
    :param game_speed: The speed the physics will run at, leave it at 100 unless your game can't run at over 240fps
    :param tick_skip: The amount of physics ticks your action will be repeated for
    :param spawn_opponents: Whether you want opponents or not
    :param team_size: Cars per team
    :param gravity: Game gravity, 1 is normal gravity
    :param boost_consumption: Car boost consumption rate, 1 is normal consumption
    :param terminal_conditions: List of terminal condition objects (rlgym.utils.TerminalCondition)
    :param reward_fn: Reward function object (rlgym.utils.RewardFunction)
    :param obs_builder: Observation builder object (rlgym.utils.ObsBuilder)
    :param action_parser: Action parser object (rlgym.utils.ActionParser)
    :param state_setter: State Setter object (rlgym.utils.StateSetter)
    :param launch_preference: Rocket League launch preference (rlgym.gamelaunch.LaunchPreference) or path to RocketLeague executable
    :param use_injector: Whether to use RLGym's bakkesmod injector or not. Enable if launching multiple instances
    :param force_paging: Enable forced paging of each spawned rocket league instance to reduce memory utilization
                            immediately, instead of allowing the OS to slowly page untouched allocations.
                            WARNING: This will require you to potentially expand your Windows Page File [1]
                            and it may substantially increase disk activity, leading to decreased disk lifetime.
                            Use at your own peril.
                            Default is off: OS dictates the behavior.
    :param raise_on_crash: If enabled, raises an exception when Rocket League crashes instead of attempting to recover.
                            You can attempt a recovery manually by calling attempt_recovery()
    :param auto_minimize: Automatically minimize the game window when launching Rocket League
    :return: Gym object
    [1]: https://www.tomshardware.com/news/how-to-manage-virtual-memory-pagefile-windows-10,36929.html
    """

    # TODO: Remove in v1.3
    if self_play is not None:
        warn('self_play argument is deprecated and will be removed in future rlgym versions.\nPlease use spawn_opponents instead', DeprecationWarning, stacklevel=2)
        spawn_opponents = self_play

    # Imports are inside the function because setup fails otherwise (Missing win32file)
    from rlgym.gym import Gym
    from rlgym.version import print_current_release_notes

    print_current_release_notes()

    match = Match(reward_function=reward_fn,
                  terminal_conditions=terminal_conditions,
                  obs_builder=obs_builder,
                  action_parser=action_parser,
                  state_setter=state_setter,
                  team_size=team_size,
                  tick_skip=tick_skip,
                  game_speed=game_speed,
                  gravity=gravity,
                  boost_consumption=boost_consumption,
                  spawn_opponents=spawn_opponents)

    return Gym(match, pipe_id=os.getpid(), launch_preference=launch_preference, use_injector=use_injector,
               force_paging=force_paging, raise_on_crash=raise_on_crash, auto_minimize=auto_minimize)
