from typing import Any, Dict

import rlviser_py as rlviser
import RocketSim as rsim

from rlgym.api import Renderer
from rlgym.rocket_league.api import Car, GameState
from rlgym.rocket_league.common_values import BOOST_LOCATIONS


class RLViserRenderer(Renderer[GameState]):
    """
    A renderer that uses RLViser to render the game state.
    """

    def __init__(self, tick_rate=120/8):
        rlviser.set_boost_pad_locations(BOOST_LOCATIONS)
        self.tick_rate = tick_rate
        self.packet_id = 0

    def render(self, state: GameState, shared_info: Dict[str, Any]) -> Any:
        boost_pad_states = [bool(timer == 0) for timer in state.boost_pad_timers]

        ball = rsim.BallState()
        ball.pos = rsim.Vec(*state.ball.position)
        ball.vel = rsim.Vec(*state.ball.linear_velocity)
        ball.ang_vel = rsim.Vec(*state.ball.angular_velocity)
        ball.rot_mat = rsim.RotMat(*state.ball.rotation_mtx.transpose().flatten())

        car_data = []
        for idx, car in enumerate(state.cars.values()):
            car_state = self._get_car_state(car)
            car_data.append((idx + 1, car.team_num, rsim.CarConfig(car.hitbox_type), car_state))

        self.packet_id += 1
        rlviser.render(tick_count=self.packet_id, tick_rate=self.tick_rate, game_mode=rsim.GameMode.SOCCAR,
                       boost_pad_states=boost_pad_states, ball=ball, cars=car_data)

    def close(self):
        rlviser.quit()

    # I stole this from RocketSimEngine
    def _get_car_state(self, car: Car):
        car_state = rsim.CarState()
        car_state.pos = rsim.Vec(*car.physics.position)
        car_state.vel = rsim.Vec(*car.physics.linear_velocity)
        car_state.ang_vel = rsim.Vec(*car.physics.angular_velocity)
        car_state.rot_mat = rsim.RotMat(*car.physics.rotation_mtx.transpose().flatten())

        car_state.demo_respawn_timer = car.demo_respawn_timer
        car_state.is_on_ground = car.on_ground
        car_state.supersonic_time = car.supersonic_time
        car_state.boost = car.boost_amount
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
        car_state.flip_rel_torque = rsim.Vec(*car.flip_torque)

        car_state.is_auto_flipping = car.is_autoflipping
        car_state.auto_flip_timer = car.autoflip_timer
        car_state.auto_flip_torque_scale = car.autoflip_direction

        return car_state
