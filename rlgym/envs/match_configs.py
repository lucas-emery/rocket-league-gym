from rlgym.envs import Match
from rlgym.utils import common_values
from rlgym.utils.terminal_conditions import common_conditions
from rlgym.utils.reward_functions import DefaultReward
from rlgym.utils.obs_builders import DefaultObs


def basic_duel_match(**kwargs):
    if "team_size" not in kwargs.keys() or kwargs["team_size"] is None:
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
    if "team_size" not in kwargs.keys() or kwargs["team_size"] is None:
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
    if "team_size" not in kwargs.keys() or kwargs["team_size"] is None:
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
    if "team_size" not in kwargs.keys() or kwargs["team_size"] is None:
        kwargs["team_size"] = 1

    kwargs["ep_len_minutes"] = 15/60
    kwargs["spawn_opponents"] = False

    game_speed, tick_skip, spawn_opponents, random_resets, self_play, team_size, terminal_conditions, reward_fn, obs_builder \
        = get_default_params(**kwargs)

    terminal_conditions.pop(1)
    terminal_conditions.append(common_conditions.BallTouchedCondition())

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
    if "self_play" in kwargs.keys():
        self_play = kwargs["self_play"]

    ep_len_minutes = 45 / 60
    if "ep_len_minutes" in kwargs.keys():
        ep_len_minutes = kwargs["ep_len_minutes"]

    game_speed = 100
    if "game_speed" in kwargs.keys():
        game_speed = kwargs["game_speed"]

    tick_skip = 8
    if "tick_skip" in kwargs.keys():
        tick_skip = kwargs["tick_skip"]

    ticks_per_sec = 120
    ticks_per_min = ticks_per_sec * 60
    max_ticks = int(round(ep_len_minutes * ticks_per_min / tick_skip))

    spawn_opponents = True
    if "spawn_opponents" in kwargs.keys():
        spawn_opponents = kwargs["spawn_opponents"]

    random_resets = False
    if "random_resets" in kwargs.keys():
        random_resets = kwargs["random_resets"]

    team_size = 1
    if "team_size" in kwargs.keys():
        team_size = kwargs["team_size"]

    terminal_conditions = [common_conditions.TimeoutCondition(max_ticks), common_conditions.GoalScoredCondition()]
    if "terminal_conditions" in kwargs.keys() and kwargs["terminal_conditions"] is not None:
        terminal_conditions = kwargs["terminal_conditions"]

    reward_fn = DefaultReward()
    if "reward_fn" in kwargs.keys() and kwargs["reward_fn"] is not None:
        reward_fn = kwargs["reward_fn"]

    obs_builder = DefaultObs()
    if "obs_builder" in kwargs.keys() and kwargs["obs_builder"] is not None:
        obs_builder = kwargs["obs_builder"]

    return game_speed, tick_skip, spawn_opponents, random_resets, self_play, team_size, terminal_conditions, reward_fn, obs_builder
