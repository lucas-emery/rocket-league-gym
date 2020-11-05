from rlgym.envs import Match
from rlgym.utils import CommonValues
from rlgym.utils.terminal_conditions import CommonConditions
from rlgym.utils.reward_functions import ShootBallReward
from rlgym.utils.obs_builders import RhobotObs

def build_rhobot_match(self_play=False):
    tick_skip = 8

    ep_len_minutes = 20 / 60
    ticks_per_sec = 120
    ticks_per_min = ticks_per_sec * 60
    max_ticks = int(round(ep_len_minutes * ticks_per_min / tick_skip))

    terminal_conditions = [CommonConditions.TimeoutCondition(max_ticks), CommonConditions.GoalScoredCondition()]
    reward_fn = ShootBallReward()
    obs_builder = RhobotObs()

    return Match(team_size=1,
                 tick_skip=tick_skip,
                 spawn_opponents=False,
                 random_resets=True,
                 self_play=self_play,
                 reward_function=reward_fn,
                 terminal_conditions=terminal_conditions,
                 obs_builder=obs_builder)

def build_basic_duels_match(self_play=False):
    tick_skip = 8

    ep_len_minutes = 5
    ticks_per_sec = 120
    ticks_per_min = ticks_per_sec * 60
    max_ticks = int(round(ep_len_minutes * ticks_per_min / tick_skip))

    terminal_conditions = [CommonConditions.TimeoutCondition(max_ticks), CommonConditions.GoalScoredCondition()]
    reward_fn = ShootBallReward()
    obs_builder = RhobotObs()

    return Match(team_size=1,
                 tick_skip=tick_skip,
                 spawn_opponents=True,
                 random_resets=False,
                 self_play=self_play,
                 reward_function=reward_fn,
                 terminal_conditions=terminal_conditions,
                 obs_builder=obs_builder)

def build_basic_doubles_match(self_play=False):
    tick_skip = 8

    ep_len_minutes = 5
    ticks_per_sec = 120
    ticks_per_min = ticks_per_sec * 60
    max_ticks = int(round(ep_len_minutes * ticks_per_min / tick_skip))

    terminal_conditions = [CommonConditions.TimeoutCondition(max_ticks), CommonConditions.GoalScoredCondition()]
    reward_fn = ShootBallReward()
    obs_builder = RhobotObs()

    return Match(team_size=2,
                 tick_skip=tick_skip,
                 spawn_opponents=True,
                 random_resets=False,
                 self_play=self_play,
                 reward_function=reward_fn,
                 terminal_conditions=terminal_conditions,
                 obs_builder=obs_builder)

def build_basic_standard_match(self_play=False):
    tick_skip = 8

    ep_len_minutes = 5
    ticks_per_sec = 120
    ticks_per_min = ticks_per_sec * 60
    max_ticks = int(round(ep_len_minutes * ticks_per_min / tick_skip))

    terminal_conditions = [CommonConditions.TimeoutCondition(max_ticks), CommonConditions.GoalScoredCondition()]
    reward_fn = ShootBallReward()
    obs_builder = RhobotObs()

    return Match(team_size=3,
                 tick_skip=tick_skip,
                 spawn_opponents=True,
                 random_resets=False,
                 self_play=self_play,
                 reward_function=reward_fn,
                 terminal_conditions=terminal_conditions,
                 obs_builder=obs_builder)