from rlgym.envs import match_configs as conf
from rlgym.envs import Match


def build_match(match_id, **kwargs):
    m = match_id.strip().lower()

    if "self" in m:
        kwargs["self_play"] = True
    else:
        kwargs["self_play"] = False

    preconfigured_match = None
    if "duel" in m:
        preconfigured_match = conf.basic_duel_match
    elif "double" in m:
        preconfigured_match = conf.basic_doubles_match
    elif "standard" in m:
        preconfigured_match = conf.basic_standard_match
    elif "default" in m:
        preconfigured_match = conf.default_match

    if preconfigured_match is not None:
        match = preconfigured_match(**kwargs)
    else:
        game_speed, tick_skip, spawn_opponents, random_resets, self_play, team_size, terminal_conditions, reward_fn, obs_builder \
            = conf.get_default_params(**kwargs)

        match = Match(team_size=team_size,
                      tick_skip=tick_skip,
                      game_speed=game_speed,
                      spawn_opponents=spawn_opponents,
                      random_resets=random_resets,
                      self_play=self_play,
                      reward_function=reward_fn,
                      terminal_conditions=terminal_conditions,
                      obs_builder=obs_builder)

    return match
