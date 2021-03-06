from rlgym.envs import Match
from rlgym.utils import common_values
from rlgym.utils.terminal_conditions import common_conditions
from rlgym.utils.reward_functions import ShootBallReward
from rlgym.utils.obs_builders import RhobotObs


def basic_duels_match(self_play=False, custom_args=None):
    if custom_args is None:
        custom_args = {"ep_len_minutes": 5}

    keys = custom_args.keys()
    if "ep_len_minutes" not in keys:
        custom_args["ep_len_minutes"] = 5

    game_speed, tick_skip, spawn_opponents, random_resets, team_size, terminal_conditions, reward_fn, obs_builder \
        = get_default_params(custom_args=custom_args)

    return Match(team_size=team_size,
                 tick_skip=tick_skip,
                 game_speed=game_speed,
                 spawn_opponents=spawn_opponents,
                 random_resets=random_resets,
                 self_play=self_play,
                 reward_function=reward_fn,
                 terminal_conditions=terminal_conditions,
                 obs_builder=obs_builder)

def basic_doubles_match(self_play=False, custom_args=None):
    if custom_args is None:
        custom_args = {"ep_len_minutes": 5}

    keys = custom_args.keys()
    if "ep_len_minutes" not in keys:
        custom_args["ep_len_minutes"] = 5
    if "team_size" not in keys:
        custom_args["team_size"] = 2

    game_speed, tick_skip, spawn_opponents, random_resets, team_size, terminal_conditions, reward_fn, obs_builder \
        = get_default_params(custom_args=custom_args)

    return Match(team_size=team_size,
                 tick_skip=tick_skip,
                 game_speed=game_speed,
                 spawn_opponents=spawn_opponents,
                 random_resets=random_resets,
                 self_play=self_play,
                 reward_function=reward_fn,
                 terminal_conditions=terminal_conditions,
                 obs_builder=obs_builder)

def basic_standard_match(self_play=False, custom_args=None):
    if custom_args is None:
        custom_args = {"ep_len_minutes": 5}

    keys = custom_args.keys()
    if "ep_len_minutes" not in keys:
        custom_args["ep_len_minutes"] = 5
    if "team_size" not in keys:
        custom_args["team_size"] = 3

    game_speed, tick_skip, spawn_opponents, random_resets, team_size, terminal_conditions, reward_fn, obs_builder \
        = get_default_params(custom_args=custom_args)

    return Match(team_size=team_size,
                 tick_skip=tick_skip,
                 game_speed=game_speed,
                 spawn_opponents=spawn_opponents,
                 random_resets=random_resets,
                 self_play=self_play,
                 reward_function=reward_fn,
                 terminal_conditions=terminal_conditions,
                 obs_builder=obs_builder)


def get_default_params(custom_args=None):
    ep_len_minutes = 45 / 60
    if custom_args is not None:
        if "ep_len_minutes" in custom_args.keys():
            ep_len_minutes = custom_args["ep_len_minutes"]

    game_speed = 100
    if custom_args is not None:
        if "game_speed" in custom_args.keys():
            game_speed = custom_args["game_speed"]

    tick_skip = 8
    if custom_args is not None:
        if "tick_skip" in custom_args.keys():
            tick_skip = custom_args["tick_skip"]

    ticks_per_sec = 120
    ticks_per_min = ticks_per_sec * 60
    max_ticks = int(round(ep_len_minutes * ticks_per_min / tick_skip))

    spawn_opponents = True
    if custom_args is not None:
        if "spawn_opponents" in custom_args.keys():
            spawn_opponents = custom_args["spawn_opponents"]

    random_resets = False
    if custom_args is not None:
        if "random_resets" in custom_args.keys():
            random_resets = custom_args["random_resets"]

    team_size = 1
    if custom_args is not None:
        if "team_size" in custom_args.keys():
            team_size = custom_args["team_size"]

    terminal_conditions = [common_conditions.TimeoutCondition(max_ticks), common_conditions.GoalScoredCondition()]
    if custom_args is not None:
        if "terminal_conditions" in custom_args.keys():
            terminal_conditions = custom_args["terminal_conditions"]

    reward_fn = ShootBallReward()
    if custom_args is not None:
        if "reward_fn" in custom_args.keys():
            reward_fn = custom_args["reward_fn"]

    obs_builder = RhobotObs()
    if custom_args is not None:
        if "obs_builder" in custom_args.keys():
            obs_builder = custom_args["obs_builder"]

    return game_speed, tick_skip, spawn_opponents, random_resets, team_size, terminal_conditions, reward_fn, obs_builder
