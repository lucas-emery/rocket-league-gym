from rlgym.envs import MatchConfigs as conf
from rlgym.envs import Match

def build_match(match_id, custom_args=None):
    m = match_id.strip().lower()
    self_play = "self" in m


    preconfigured_match = None
    if "rhobot" in m:
        preconfigured_match = conf.rhobot_match
    if "duel" in m:
        preconfigured_match = conf.basic_duels_match
    if "double" in m:
        preconfigured_match = conf.basic_duels_match
    if "standard" in m:
        preconfigured_match = conf.basic_duels_match

    if preconfigured_match is not None:
        match = preconfigured_match(self_play=self_play, custom_args=custom_args)
    else:
        if custom_args is not None:
            game_speed, tick_skip, spawn_opponents, random_resets, team_size, terminal_conditions, reward_fn, obs_builder \
                = conf.get_default_params(custom_args=custom_args)

            match = Match(team_size=team_size,
                         tick_skip=tick_skip,
                         game_speed=game_speed,
                         spawn_opponents=spawn_opponents,
                         random_resets=random_resets,
                         self_play=self_play,
                         reward_function=reward_fn,
                         terminal_conditions=terminal_conditions,
                         obs_builder=obs_builder)
        else:
            match = None

    return match
