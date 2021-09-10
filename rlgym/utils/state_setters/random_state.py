from rlgym.utils.state_setters import StateSetter
from rlgym.utils.state_setters import StateWrapper
from rlgym.utils.math import rand_vec3
import numpy as np
from numpy import random as rand

X_MAX = 7000
Y_MAX = 9000
Z_MAX_BALL = 1850
Z_MAX_CAR = 1900
PITCH_MAX = np.pi/2
YAW_MAX = np.pi
ROLL_MAX = np.pi


class RandomState(StateSetter):

    def __init__(self, ball_rand_speed: bool = False, cars_rand_speed: bool = False, cars_on_ground: bool = True):
        """
        RandomState constructor.

        :param ball_rand_speed: Boolean indicating whether the ball will have a randomly set velocity.
        :param cars_rand_speed: Boolean indicating whether cars will have a randomly set velocity.
        :param cars_on_ground: Boolean indicating whether cars should only be placed on the ground.
        """
        super().__init__()
        self.ball_rand_speed = ball_rand_speed
        self.cars_rand_speed = cars_rand_speed
        self.cars_on_ground = cars_on_ground

    def reset(self, state_wrapper: StateWrapper):
        """
        Modifies the StateWrapper to contain random values the ball and each car.

        :param state_wrapper: StateWrapper object to be modified with desired state values.
        """
        self._reset_ball_random(state_wrapper, self.ball_rand_speed)
        self._reset_cars_random(state_wrapper, self.cars_on_ground, self.cars_rand_speed)

    def _reset_ball_random(self, state_wrapper: StateWrapper, random_speed: bool):
        """
        Function to set the ball to a random position.

        :param state_wrapper: StateWrapper object to be modified.
        :param random_speed: Boolean indicating whether to randomize velocity values.
        """
        state_wrapper.ball.set_pos(rand.random(
        ) * X_MAX - X_MAX/2, rand.random() * Y_MAX - Y_MAX/2, rand.random() * Z_MAX_BALL + 100)
        if random_speed:
            state_wrapper.ball.set_lin_vel(*rand_vec3(3000))
            state_wrapper.ball.set_ang_vel(*rand_vec3(6))

    def _reset_cars_random(self, state_wrapper: StateWrapper, on_ground: bool, random_speed: bool):
        """
        Function to set all cars to a random position.

        :param state_wrapper: StateWrapper object to be modified.
        :param on_ground: Boolean indicating whether to place cars only on the ground.
        :param random_speed: Boolean indicating whether to randomize velocity values.
        """
        for car in state_wrapper.cars:
            # set random position and rotation for all cars based on pre-determined ranges
            car.set_pos(rand.random() * X_MAX - X_MAX/2, rand.random()
                        * Y_MAX - Y_MAX/2, rand.random() * Z_MAX_CAR + 150)
            car.set_rot(rand.random() * PITCH_MAX - PITCH_MAX/2, rand.random()
                        * YAW_MAX - YAW_MAX/2, rand.random() * ROLL_MAX - ROLL_MAX/2)

            car.boost = rand.random()

            if random_speed:
                # set random linear and angular velocity based on pre-determined ranges
                car.set_lin_vel(*rand_vec3(2300))
                car.set_ang_vel(*rand_vec3(5.5))

            # 100% of cars will be set on ground if on_ground == True
            # otherwise, 50% of cars will be set on ground
            if on_ground or rand.random() < 0.5:
                # z position (up/down) is set to ground
                car.set_pos(z=17)
                # z linear velocity (vertical) set to 0
                car.set_lin_vel(z=0)
                # pitch (front of car up/down) set to 0
                # roll (side of car up/down) set to 0
                car.set_rot(pitch=0, roll=0)
                # x angular velocity (affects pitch) set to 0
                # y angular velocity (affects) roll) set to 0
                car.set_ang_vel(x=0, y=0)
