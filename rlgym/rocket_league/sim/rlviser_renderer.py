from typing import Any

import RocketSim as rsim

from rlgym.api.engine.renderer import Renderer
from rlgym.rocket_league.common_values import BOOST_LOCATIONS
from rlgym.rocket_league.engine.car import Car
from rlgym.rocket_league.engine.game_state import GameState


class RLViserRenderer(Renderer[GameState]):

    def __init__(self):
        import rlviser_py as rlviser
        rlviser.set_boost_pad_locations(BOOST_LOCATIONS)
        self.rlviser = rlviser
        self.tick_rate = 1/120

    def render(self, state: GameState) -> Any:
        boost_pad_states = state.boost_pad_timers == 0

        ball = rsim.BallState()
        ball.pos = rsim.Vec(*state.ball.position)
        ball.vel = rsim.Vec(*state.ball.linear_velocity)
        ball.ang_vel = rsim.Vec(*state.ball.angular_velocity)

        car_data = []
        for idx, car in enumerate(state.cars.values()):
            car_state = self._get_car_state(car)
            car_data.append((idx, car.team_num, rsim.CarConfig(car.hitbox_type), car_state))

        # TODO I think we're missing tick_count for the clock, fake it till u make it
        self.rlviser.render(state.tick_count, self.tick_rate, boost_pad_states, ball, car_data)

    def close(self):
        self.rlviser.quit()

    # I stole this from SimEngine
    def _get_car_state(self, car: Car):
        car_state = rsim.CarState()
        car_state.pos = rsim.Vec(*car.physics.position)
        car_state.vel = rsim.Vec(*car.physics.linear_velocity)
        car_state.ang_vel = rsim.Vec(*car.physics.angular_velocity)
        car_state.rot_mat = rsim.RotMat(*car.physics.rotation_mtx.transpose().flatten())

        car_state.demo_respawn_timer = car.demo_respawn_timer
        car_state.is_on_ground = car.on_ground
        car_state.supersonic_time = car.supersonic_time
        car_state.boost = car.boost_amount * 100
        car_state.time_spent_boosting = car.boost_active_time
        car_state.handbrake_val = car.handbrake

        car_state.has_jumped = car.has_jumped
        car_state.last_controls.jump = car.is_holding_jump
        car_state.is_jumping = car.is_jumping
        car_state.jump_time = car.jump_time

        car_state.has_flipped = car.has_flipped
        car_state.has_double_jumped = car.has_double_jumped
        car_state.air_time_since_jump = car.air_time_since_jump
        car_state.flip_time = car.flip_time
        car_state.last_rel_dodge_torque = rsim.Vec(*car.flip_torque)

        car_state.is_auto_flipping = car.is_autoflipping
        car_state.auto_flip_timer = car.autoflip_timer
        car_state.auto_flip_torque_scale = car.autoflip_direction

        car_state.car_contact_id = car.bump_victim_id

        return car_state
