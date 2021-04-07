from rlgym.envs import Match
from rlgym.utils import common_values
from rlgym.utils.terminal_conditions import common_conditions
from rlgym.utils.reward_functions import DefaultReward
from rlgym.utils.obs_builders import DefaultObs


def basic_duel_match(**kwargs):
    if kwargs["team_size"] is None:
        kwargs["team_size"] = 1

    game_speed, tick_skip, spawn_opponents, random_resets, self_play, team_size, terminal_conditions, reward_fn, obs_builder \
        = get_default_params(**kwargs)

    return Match(team_size=team_size,
                 tick_skip=tick_skip,
                 game_speed=game_speed,
                 spawn_opponents=spawn_opponents,
                 random_resets=random_resets,
                 self_play=self_play,
                 reward_function=reward_fn,
                 terminal_conditions=terminal_conditions,
                 obs_builder=obs_builder)


def basic_doubles_match(**kwargs):
    if kwargs["team_size"] is None:
        kwargs["team_size"] = 2

    game_speed, tick_skip, spawn_opponents, random_resets, self_play, team_size, terminal_conditions, reward_fn, obs_builder \
        = get_default_params(**kwargs)

    return Match(team_size=team_size,
                 tick_skip=tick_skip,
                 game_speed=game_speed,
                 spawn_opponents=spawn_opponents,
                 random_resets=random_resets,
                 self_play=self_play,
                 reward_function=reward_fn,
                 terminal_conditions=terminal_conditions,
                 obs_builder=obs_builder)


def basic_standard_match(**kwargs):
    if kwargs["team_size"] is None:
        kwargs["team_size"] = 3

    game_speed, tick_skip, spawn_opponents, random_resets, self_play, team_size, terminal_conditions, reward_fn, obs_builder \
        = get_default_params(**kwargs)

    return Match(team_size=team_size,
                 tick_skip=tick_skip,
                 game_speed=game_speed,
                 spawn_opponents=spawn_opponents,
                 random_resets=random_resets,
                 self_play=self_play,
                 reward_function=reward_fn,
                 terminal_conditions=terminal_conditions,
                 obs_builder=obs_builder)

def default_match(**kwargs):
    print(kwargs.keys(), kwargs["ep_len_minutes"])
    if  kwargs["team_size"] is None:
        kwargs["team_size"] = 1

    if kwargs["spawn_opponents"] is None:
        kwargs["spawn_opponents"] = False

    if kwargs["ep_len_minutes"] is None:
        print("setting ep len")
        kwargs["ep_len_minutes"] = 15/60

    game_speed, tick_skip, spawn_opponents, random_resets, self_play, team_size, terminal_conditions, reward_fn, obs_builder \
        = get_default_params(**kwargs)

    if kwargs["terminal_conditions"] is None:
        terminal_conditions.pop(1)

    return Match(team_size=team_size,
                 tick_skip=tick_skip,
                 game_speed=game_speed,
                 spawn_opponents=spawn_opponents,
                 random_resets=random_resets,
                 self_play=self_play,
                 reward_function=reward_fn,
                 terminal_conditions=terminal_conditions,
                 obs_builder=obs_builder)

def get_default_params(**kwargs):
    self_play = False
    if kwargs["self_play"] is not None:
        self_play = kwargs["self_play"]

    ep_len_minutes = 45 / 60
    if kwargs["ep_len_minutes"] is not None:
        ep_len_minutes = kwargs["ep_len_minutes"]

    game_speed = 100
    if kwargs["game_speed"] is not None:
        game_speed = kwargs["game_speed"]

    tick_skip = 8
    if kwargs["tick_skip"] is not None:
        tick_skip = kwargs["tick_skip"]

    ticks_per_sec = 120
    ticks_per_min = ticks_per_sec * 60
    max_ticks = int(round(ep_len_minutes * ticks_per_min / tick_skip))

    spawn_opponents = True
    if "spawn_opponents" in kwargs.keys():
        spawn_opponents = kwargs["spawn_opponents"]

    random_resets = False
    if kwargs["random_resets"] is not None:
        random_resets = kwargs["random_resets"]

    team_size = 1
    if kwargs["team_size"] is not None:
        team_size = kwargs["team_size"]

    terminal_conditions = [common_conditions.TimeoutCondition(max_ticks), common_conditions.GoalScoredCondition()]
    if kwargs["terminal_conditions"] is not None:
        terminal_conditions = kwargs["terminal_conditions"]

    reward_fn = DefaultReward()
    if kwargs["reward_fn"] is not None:
        reward_fn = kwargs["reward_fn"]

    obs_builder = DefaultObs()
    if kwargs["obs_builder"] is not None:
        obs_builder = kwargs["obs_builder"]

    return game_speed, tick_skip, spawn_opponents, random_resets, self_play, team_size, terminal_conditions, reward_fn, obs_builder
