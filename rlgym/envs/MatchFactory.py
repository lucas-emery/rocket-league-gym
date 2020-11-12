from rlgym.envs import MatchConfigs as conf


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
        match = None

    return match
