import os
from typing import Any, Dict, List

import RocketSim as rsim
import numpy as np
from rlgym.api import TransitionEngine, AgentID
from rlgym.rocket_league.api import Car, GameConfig, GameState, PhysicsObject
from rlgym.rocket_league.common_values import BOOST_CONSUMPTION_RATE, GRAVITY, GOAL_THRESHOLD


class RocketSimEngine(TransitionEngine[AgentID, GameState, np.ndarray]):
    """
    A headless Rocket League TransitionEngine backed by RocketSim.

    Simulates a normal soccar game with a single ball and any number of cars.
    """

    def __init__(self, rlbot_delay=True):
        """
        A headless Rocket League TransitionEngine backed by RocketSim.

        Simulates a normal soccar game with a single ball and any number of cars.

        :param rlbot_delay: Enables RLBot-like 1 tick delay for actions.
            This forces the first action of the episode to no-op
        """
        try:
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            rsim.init(os.path.join(cur_dir, 'collision_meshes'))
        except Exception:
            pass
        self._rlbot_delay = rlbot_delay
        self._state = None
        self._tick_count = None
        self._game_config = None
        self._cars: Dict[AgentID, rsim.Car] = {}
        self._agent_ids: Dict[int, AgentID] = {}
        self._hitboxes: Dict[int, int] = {}
        self._touches: Dict[int, int] = {}
        self._arena = rsim.Arena(rsim.GameMode.SOCCAR)
        self._arena.set_ball_touch_callback(self._ball_touch_callback)

    @property
    def agents(self) -> List[AgentID]:
        return list(self._cars.keys())

    @property
    def max_num_agents(self) -> int:
        return 1337

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def config(self) -> Dict[str, Any]:
        # TODO allow hooking rsim via this config?
        return {
            'rlbot_delay': self._rlbot_delay
        }

    @config.setter
    def config(self, value: Dict[str, Any]):
        self._rlbot_delay = value.get('rlbot_delay', self._rlbot_delay)

    def step(self, actions: Dict[AgentID, np.ndarray], shared_info: Dict[str, Any]) -> GameState:
        if len(self._cars) == 0:
            steps = 1
        elif len(actions) != len(self._cars):
            raise KeyError("Expected actions for {} agents but received {}.".format(len(self._cars), len(actions)))
        else:
            action = next(iter(actions.values()))
            if len(action.shape) != 2:
                raise ValueError("Expected action of shape (N, 8) but received {}".format(action.shape))

            steps = action.shape[0]

        for step in range(steps):
            if self._rlbot_delay:
                self._arena.step(1)

            for agent_id, action in actions.items():
                controls = rsim.CarControls()
                controls.throttle = action[step, 0]
                controls.steer = action[step, 1]
                controls.pitch = action[step, 2]
                controls.yaw = action[step, 3]
                controls.roll = action[step, 4]
                controls.jump = bool(action[step, 5])
                controls.boost = bool(action[step, 6])
                controls.handbrake = bool(action[step, 7])

                self._cars[agent_id].set_controls(controls)

            if not self._rlbot_delay:
                self._arena.step(1)

            self._tick_count += 1

        return self._get_state()

    def set_state(self, desired_state: GameState, shared_info: Dict[str, Any]) -> GameState:
        self._tick_count = desired_state.tick_count

        config = rsim.MutatorConfig()
        config.gravity = rsim.Vec(0, 0, desired_state.config.gravity * -GRAVITY)
        config.boost_used_per_second = desired_state.config.boost_consumption * BOOST_CONSUMPTION_RATE
        self._arena.set_mutator_config(config)
        self._game_config = desired_state.config

        ball_state = rsim.BallState()
        ball_state.pos = rsim.Vec(*desired_state.ball.position)
        ball_state.vel = rsim.Vec(*desired_state.ball.linear_velocity)
        ball_state.ang_vel = rsim.Vec(*desired_state.ball.angular_velocity)
        try:
            ball_state.rot_mat = rsim.RotMat(*desired_state.ball.rotation_mtx.transpose().flatten())
        except ValueError:
            pass
        self._arena.ball.set_state(ball_state)

        # TODO reuse cars? We'd have to check the hitbox
        for car in self._arena.get_cars():
            self._arena.remove_car(car)
        self._cars.clear()
        self._agent_ids.clear()
        self._hitboxes.clear()
        self._touches.clear()

        for agent_id, desired_car in desired_state.cars.items():
            config = rsim.CarConfig(desired_car.hitbox_type)
            config.dodge_deadzone = desired_state.config.dodge_deadzone
            car: rsim.Car = self._arena.add_car(desired_car.team_num, config)
            self._cars[agent_id] = car
            self._agent_ids[car.id] = agent_id
            self._hitboxes[car.id] = desired_car.hitbox_type
            self._touches[car.id] = 0

        # This loop looks dumb here but we need to create the cars before setting the state
        #  so we know the full AgentID->RSimID mapping
        for agent_id, desired_car in desired_state.cars.items():
            self._set_car_state(self._cars[agent_id], desired_car)

        # TODO check if the order is correct, I think mtheall's bindings handle it internally
        for idx, pad in enumerate(self._arena.get_boost_pads()):
            pad_state = rsim.BoostPadState()
            pad_state.cooldown = desired_state.boost_pad_timers[idx]
            pad.set_state(pad_state)

        return self._get_state()

    def _get_state(self) -> GameState:
        gs = GameState()
        gs.tick_count = self._tick_count
        gs.config = self._game_config

        ball_state = self._arena.ball.get_state()
        gs.ball = PhysicsObject()
        gs.ball.position = ball_state.pos.as_numpy()
        gs.ball.linear_velocity = ball_state.vel.as_numpy()
        gs.ball.angular_velocity = ball_state.ang_vel.as_numpy()
        gs.ball.rotation_mtx = np.ascontiguousarray(ball_state.rot_mat.as_numpy().reshape(3, 3).transpose())

        # Only works for soccar
        gs.goal_scored = abs(gs.ball.position[1]) > GOAL_THRESHOLD

        gs.cars = {}
        for agent_id, rsim_car in self._cars.items():
            car_state = rsim_car.get_state()

            car = Car()
            car.team_num = rsim_car.team
            car.hitbox_type = self._hitboxes[rsim_car.id]

            car.physics = PhysicsObject()
            car.physics.position = car_state.pos.as_numpy()
            car.physics.linear_velocity = car_state.vel.as_numpy()
            car.physics.angular_velocity = car_state.ang_vel.as_numpy()
            car.physics.rotation_mtx = np.ascontiguousarray(car_state.rot_mat.as_numpy().reshape(3, 3).transpose())

            car.demo_respawn_timer = car_state.demo_respawn_timer
            car.wheels_with_contact = car_state.wheels_with_contact
            car.supersonic_time = car_state.supersonic_time
            car.boost_amount = car_state.boost
            car.boost_active_time = car_state.time_spent_boosting
            car.handbrake = car_state.handbrake_val

            car.has_jumped = car_state.has_jumped
            car.is_holding_jump = car_state.last_controls.jump
            car.is_jumping = car_state.is_jumping
            car.jump_time = car_state.jump_time

            car.has_flipped = car_state.has_flipped
            car.has_double_jumped = car_state.has_double_jumped
            car.air_time_since_jump = car_state.air_time_since_jump
            car.flip_time = car_state.flip_time
            car.flip_torque = car_state.flip_rel_torque.as_numpy()

            car.is_autoflipping = car_state.is_auto_flipping
            car.autoflip_timer = car_state.auto_flip_timer
            car.autoflip_direction = car_state.auto_flip_torque_scale

            car.bump_victim_id = self._agent_ids[car_state.car_contact_id] if car_state.car_contact_cooldown_timer > 0 else None
            car.ball_touches = self._touches[rsim_car.id]
            self._touches[rsim_car.id] = 0

            gs.cars[agent_id] = car

        # TODO check if the order is correct, I think mtheall's bindings handle it internally
        boost_pads = self._arena.get_boost_pads()
        gs.boost_pad_timers = np.empty(len(boost_pads), dtype=np.float32)
        for idx, pad in enumerate(boost_pads):
            pad_state = pad.get_state()
            gs.boost_pad_timers[idx] = pad_state.cooldown

        self._state = gs
        return gs

    def _set_car_state(self, car: rsim.Car, desired_car: Car):
        car_state = rsim.CarState()
        car_state.pos = rsim.Vec(*desired_car.physics.position)
        car_state.vel = rsim.Vec(*desired_car.physics.linear_velocity)
        car_state.ang_vel = rsim.Vec(*desired_car.physics.angular_velocity)
        car_state.rot_mat = rsim.RotMat(*desired_car.physics.rotation_mtx.transpose().flatten())

        car_state.demo_respawn_timer = desired_car.demo_respawn_timer
        car_state.is_demoed = desired_car.is_demoed
        car_state.wheels_with_contact = desired_car.wheels_with_contact
        car_state.is_on_ground = desired_car.on_ground
        car_state.supersonic_time = desired_car.supersonic_time
        car_state.boost = desired_car.boost_amount
        car_state.time_spent_boosting = desired_car.boost_active_time
        car_state.handbrake_val = desired_car.handbrake

        car_state.has_jumped = desired_car.has_jumped
        car_state.last_controls.jump = desired_car.is_holding_jump
        car_state.is_jumping = desired_car.is_jumping
        car_state.jump_time = desired_car.jump_time

        car_state.has_flipped = desired_car.has_flipped
        car_state.is_flipping = desired_car.is_flipping
        car_state.has_double_jumped = desired_car.has_double_jumped
        car_state.air_time_since_jump = desired_car.air_time_since_jump
        car_state.flip_time = desired_car.flip_time
        car_state.flip_rel_torque = rsim.Vec(*desired_car.flip_torque)

        car_state.is_auto_flipping = desired_car.is_autoflipping
        car_state.auto_flip_timer = desired_car.autoflip_timer
        car_state.auto_flip_torque_scale = desired_car.autoflip_direction

        if desired_car.bump_victim_id is not None:
            car_state.car_contact_id = self._cars[desired_car.bump_victim_id].id
            # Do we want to set the bump cooldown too?

        car.set_state(car_state)

    def _ball_touch_callback(self, arena: rsim.Arena, car: rsim.Car, data):
        self._touches[car.id] += 1

    def create_base_state(self) -> GameState:
        gs = GameState()
        gs.tick_count = 0
        gs.goal_scored = False

        gs.config = GameConfig()
        gs.config.gravity = 1
        gs.config.boost_consumption = 1
        gs.config.dodge_deadzone = 0.5

        gs.ball = PhysicsObject()
        gs.cars = {}
        gs.boost_pad_timers = np.zeros(len(self._arena.get_boost_pads()), dtype=np.float32)

        return gs

    def close(self) -> None:
        pass
