from rlgym.utils import math
import numpy as np
from typing import Optional


class PhysicsObject(object):
    def __init__(self, position=None, quaternion=None, linear_velocity=None, angular_velocity=None):
        self.position: np.ndarray = position if position else np.zeros(3)

        # ones by default to prevent mathematical errors when converting quat to rot matrix on empty physics state
        self.quaternion: np.ndarray = quaternion if quaternion else np.ones(4)

        self.linear_velocity: np.ndarray = linear_velocity if linear_velocity else np.zeros(3)
        self.angular_velocity: np.ndarray = angular_velocity if angular_velocity else np.zeros(3)
        self._euler_angles: Optional[np.ndarray] = math.quat_to_euler(self.quaternion)
        self._rotation_mtx: Optional[np.ndarray] = math.quat_to_rot_mtx(self.quaternion)

    def decode_car_data(self, car_data: np.ndarray):
        self.position = car_data[:3]
        self.quaternion = car_data[3:7]
        self.linear_velocity = car_data[7:10]
        self.angular_velocity = car_data[10:]

    # roll, pitch, yaw
    def euler_angles(self) -> np.ndarray:
        return self._euler_angles

    def rotation_mtx(self) -> np.ndarray:
        return self._rotation_mtx

    def forward(self) -> np.ndarray:
        return self.rotation_mtx()[:, 0]

    def right(self) -> np.ndarray:
        return self.rotation_mtx()[:, 1]

    def up(self) -> np.ndarray:
        return self.rotation_mtx()[:, 2]

    def decode_ball_data(self, ball_data: np.ndarray):
        self.position = ball_data[:3]
        self.linear_velocity = ball_data[3:6]
        self.angular_velocity = ball_data[6:9]

    def serialize(self):
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

        return repr
