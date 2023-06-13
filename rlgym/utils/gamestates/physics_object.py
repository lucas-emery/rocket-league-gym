"""
A class to represent the state of a physics object from the game.
"""

from rlgym.utils import math
import numpy as np
from typing import Optional


class PhysicsObject(object):
    def __init__(self, position=None, quaternion=None, linear_velocity=None, angular_velocity=None):
        self.position: np.ndarray = position if position is not None else np.zeros(3)
        self.quaternion: np.ndarray = quaternion if quaternion is not None else np.array([1, 0, 0, 0], dtype=np.float32)
        self.linear_velocity: np.ndarray = linear_velocity if linear_velocity is not None else np.zeros(3)
        self.angular_velocity: np.ndarray = angular_velocity if angular_velocity is not None else np.zeros(3)
        self._euler_angles: Optional[np.ndarray] = None
        self._rotation_mtx: Optional[np.ndarray] = None
        self._has_computed_rot_mtx = False
        self._has_computed_euler_angles = False

    def decode_car_data(self, car_data: np.ndarray):
        """
        Function to decode the physics state of a car from the game state array.
        :param car_data: Slice of game state array containing the car data to decode.
        """
        self.position = car_data[:3]
        self.quaternion = car_data[3:7]
        self.linear_velocity = car_data[7:10]
        self.angular_velocity = car_data[10:]

    def decode_ball_data(self, ball_data: np.ndarray):
        """
        Function to decode the physics state of the ball from the game state array.
        :param ball_data: Slice of game state array containing the ball data to decode.
        """
        self.position = ball_data[:3]
        self.linear_velocity = ball_data[3:6]
        self.angular_velocity = ball_data[6:9]

    def forward(self) -> np.ndarray:
        return self.rotation_mtx()[:, 0]

    def right(self) -> np.ndarray:
        return self.rotation_mtx()[:, 1]

    def left(self) -> np.ndarray:
        return self.rotation_mtx()[:, 1] * -1

    def up(self) -> np.ndarray:
        return self.rotation_mtx()[:, 2]

    def pitch(self) -> float:
        return self.euler_angles()[0]

    def yaw(self) -> float:
        return self.euler_angles()[1]

    def roll(self) -> float:
        return self.euler_angles()[2]

    # pitch, yaw, roll
    def euler_angles(self) -> np.ndarray:
        if not self._has_computed_euler_angles:
            self._euler_angles = math.quat_to_euler(self.quaternion)
            self._has_computed_euler_angles = True

        return self._euler_angles

    def rotation_mtx(self) -> np.ndarray:
        if not self._has_computed_rot_mtx:
            self._rotation_mtx = math.quat_to_rot_mtx(self.quaternion)
            self._has_computed_rot_mtx = True

        return self._rotation_mtx

    def serialize(self):
        """
        Function to serialize all the values contained by this physics object into a single 1D list. This can be useful
        when constructing observations for a policy.
        :return: List containing the serialized data.
        """
        repr = []

        if self.position is not None:
            for arg in self.position:
                repr.append(arg)
                
        if self.quaternion is not None:
            for arg in self.quaternion:
                repr.append(arg)
                
        if self.linear_velocity is not None:
            for arg in self.linear_velocity:
                repr.append(arg)
                
        if self.angular_velocity is not None:
            for arg in self.angular_velocity:
                repr.append(arg)

        if self._euler_angles is not None:
            for arg in self._euler_angles:
                repr.append(arg)

        if self._rotation_mtx is not None:
            for arg in self._rotation_mtx.ravel():
                repr.append(arg)

        return repr
