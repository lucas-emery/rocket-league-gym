import logging
from collections import Counter
from typing import Union

import carball as cb
import numpy as np
from carball.analysis.analysis_manager import AnalysisManager
from carball.controls.controls import ControlsCreator

from rlgym.utils import math
from rlgym.utils.common_values import ORANGE_TEAM, BLUE_TEAM, BOOST_LOCATIONS
from rlgym.utils.gamestates import GameState, PhysicsObject, PlayerData

boost_locations = np.array(BOOST_LOCATIONS)  # Need ndarray for speed

invert = np.array((-1, -1, 1))


def convert_replay(replay: Union[str, AnalysisManager]):
    if isinstance(replay, str):
        replay = cb.analyze_replay_file(replay, logging_level=logging.CRITICAL)
    ControlsCreator().get_controls(replay.game)

    boost_timers = np.zeros(34)
    demo_timers = np.zeros(len(replay.game.players))

    blue_goals = 0
    orange_goals = 0
    goals = list(replay.game.goals)[::-1]
    touches = list(replay.protobuf_game.game_stats.hits)[::-1]
    demos = list(replay.game.demos)[::-1]

    match_goals = Counter()
    match_saves = Counter()
    match_shots = Counter()
    match_demos = Counter()
    match_boost_pickups = Counter()

    boost_amounts = {}
    last_locations = {}

    player_pos_pyr_vel_angvel_boost_controls = {  # Preload useful arrays so we can fetch by index later
        player.online_id: (
            player.data[["pos_x", "pos_y", "pos_z"]].values.astype(float),
            player.data[["rot_x", "rot_y", "rot_z"]].fillna(0).values.astype(float),
            player.data[["vel_x", "vel_y", "vel_z"]].fillna(0).values.astype(float) / 10,
            player.data[["ang_vel_x", "ang_vel_y", "ang_vel_z"]].fillna(0).values.astype(float) / 1000,
            player.data["boost"].fillna(0).astype(float) / 255,
            player.controls[["throttle", "steer", "pitch", "yaw", "roll",
                             "jump", "boost", "handbrake"]].fillna(0).values.astype(float),
        )
        for player in replay.game.players
    }

    ball_pos_pyr_vel_angvel = (
            replay.game.ball[["pos_x", "pos_y", "pos_z"]].values.astype(float),
            replay.game.ball[["rot_x", "rot_y", "rot_z"]].fillna(0).values.astype(float),
            replay.game.ball[["vel_x", "vel_y", "vel_z"]].fillna(0).values.astype(float) / 10,
            replay.game.ball[["ang_vel_x", "ang_vel_y", "ang_vel_z"]].fillna(0).values.astype(float) / 1000,
        )

    rallies = []
    for kf1, kf2 in zip(replay.game.kickoff_frames, replay.game.kickoff_frames[1:] + [replay.game.frames.index[-1]]):
        for goal in replay.game.goals:
            if kf1 < goal.frame_number < kf2:
                rallies.append((kf1, goal.frame_number))
                break
        else:  # No goal between kickoffs
            rallies.append((kf1, kf2))

    last_frame = 0
    for i, (frame, ball_row) in enumerate(replay.game.ball.iterrows()):
        for start, end in rallies:
            if start <= frame < end:
                # del rallies[0]
                break
        else:
            continue

        state = GameState()

        # game_type
        state.game_type = -1

        # blue_score/orange_score
        if len(goals) > 0 and goals[-1].frame_number <= frame:
            goal = goals.pop()
            match_goals[goal.player.online_id] += 1
            if goal.player_team == 0:
                blue_goals += 1
            else:
                orange_goals += 1
        state.blue_score = blue_goals
        state.orange_score = orange_goals

        # last_touch
        touched = set()
        while len(touches) > 0 and touches[-1].frame_number <= frame:
            touch = touches.pop()
            p_id = touch.player_id.id
            state.last_touch = p_id
            touched.add(p_id)
            if touch.save:
                match_saves[p_id] += 1
            if touch.shot:
                match_shots[p_id] += 1

        # demos for players
        demoed = set()
        while len(demos) > 0 and demos[-1]["frame_number"] <= frame:
            demo = demos.pop()
            attacker = demo["attacker"].online_id
            victim = demo["victim"].online_id
            match_demos[attacker] += 1
            demoed.add(victim)

        # players
        actions = []
        for n, player in enumerate(replay.game.players):
            player_data = PlayerData()
            if player.online_id in demoed:
                demo_timers[n] = 3

            player_data.car_id = player.online_id
            player_data.team_num = ORANGE_TEAM if player.team.is_orange else BLUE_TEAM
            player_data.match_goals = match_goals[player.online_id]
            player_data.match_saves = match_saves[player.online_id]
            player_data.match_shots = match_shots[player.online_id]
            player_data.match_demolishes = match_demos[player.online_id]
            player_data.boost_pickups = match_boost_pickups[player.online_id]
            player_data.is_demoed = demo_timers[n] > 0
            player_data.on_ground = None  # Undefined
            player_data.ball_touched = player.online_id in touched
            player_data.has_flip = None  # Undefined, TODO use jump_active, double_jump_active and dodge_active?
            pos, pyr, vel, ang_vel, boost, controls = (v[i] for v in
                                                       player_pos_pyr_vel_angvel_boost_controls[player.online_id])

            player_data.boost_amount = boost
            if np.isnan(pos).any():
                pos = last_locations[player.online_id]
            else:
                last_locations[player.online_id] = pos
            player_data.car_data = PhysicsObject(
                position=pos,
                quaternion=math.rotation_to_quaternion(math.euler_to_rotation(pyr)),
                linear_velocity=vel,
                angular_velocity=ang_vel
            )
            player_data.inverted_car_data = PhysicsObject(
                position=pos * invert,
                quaternion=math.rotation_to_quaternion(math.euler_to_rotation(pyr * invert[::-1])),
                linear_velocity=vel * invert,
                angular_velocity=ang_vel * invert
            )

            old_boost = boost_amounts.get(player.online_id, float("inf"))
            boost_change = boost - old_boost
            boost_amounts[player.online_id] = player_data.boost_amount
            if boost_change > 0 and not (old_boost == 0 and boost == 85 / 255):  # Ignore boost gains on spawn
                closest_boost = np.linalg.norm(boost_locations - pos, axis=-1).argmin()
                if boost_locations[closest_boost][1] > 72:
                    boost_timers[closest_boost] = 10
                else:
                    boost_timers[closest_boost] = 4
                match_boost_pickups[player.online_id] += 1

            state.players.append(player_data)

            actions.append(controls)

        # ball
        pos, pyr, vel, ang_vel = (v[i] for v in ball_pos_pyr_vel_angvel)
        if np.isnan(pos).any():
            continue  # Goal scored, go next
        state.ball = PhysicsObject(
                position=pos,
                quaternion=math.rotation_to_quaternion(math.euler_to_rotation(pyr)),
                linear_velocity=vel,
                angular_velocity=ang_vel
            )

        # inverted_ball
        state.inverted_ball = PhysicsObject(
                position=pos * invert,
                quaternion=math.rotation_to_quaternion(math.euler_to_rotation(pyr * invert[::-1])),
                linear_velocity=vel * invert,
                angular_velocity=ang_vel * invert
            )

        # boost_pads
        state.boost_pads = (boost_timers == 0) * 1

        # inverted_boost_pads
        state.inverted_boost_pads = state.boost_pads[::-1]

        d_time = (frame - last_frame) / 30  # Maybe use time delta from replay instead?
        boost_timers -= d_time  # Should this be before or after values are set?
        demo_timers -= d_time
        boost_timers[boost_timers < 0] = 0
        demo_timers[demo_timers < 0] = 0
        last_frame = frame

        yield state, actions
