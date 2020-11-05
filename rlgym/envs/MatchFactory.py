from rlgym.envs import MatchConfigs as conf


def build_match(match_id):
    m = match_id.strip().lower()
    selfplay = "self" in m

    if "rhobot" in m:
        return conf.build_rhobot_match(selfplay)
    if "duel" in m:
        return conf.build_basic_duels_match(selfplay)
    if "double" in m:
        return conf.build_basic_duels_match(selfplay)
    if "standard" in m:
        return conf.build_basic_duels_match(selfplay)