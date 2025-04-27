import numpy as np
from dataclasses import dataclass
from typing import TypeVar, Optional

from .utils import create_default_init
from ..math import euler_to_rotation, quat_to_euler, quat_to_rot_mtx, rotation_to_quaternion

T = TypeVar('T')


@dataclass(init=False)
class PhysicsObject:
    INV_VEC = np.array([-1, -1, 1], dtype=np.float32)
    INV_MTX = np.array([[-1, -1, -1], [-1, -1, -1], [1, 1, 1]], dtype=np.float32)

    position: np.ndarray
    linear_velocity: np.ndarray
    angular_velocity: np.ndarray
    _quaternion: Optional[np.ndarray]
    _rotation_mtx: Optional[np.ndarray]
    _euler_angles: Optional[np.ndarray]

    __slots__ = tuple(__annotations__)

    exec(create_default_init(__slots__))

    def inverted(self: T) -> T:
        inv = PhysicsObject()
        inv.position = self.position * PhysicsObject.INV_VEC
        inv.linear_velocity = self.linear_velocity * PhysicsObject.INV_VEC
        inv.angular_velocity = self.angular_velocity * PhysicsObject.INV_VEC
        if self._rotation_mtx is not None or self._quaternion is not None or self._euler_angles is not None:
            inv.rotation_mtx = self.rotation_mtx * PhysicsObject.INV_MTX
        return inv

    @property
    def quaternion(self) -> np.ndarray:
        if self._quaternion is None:
            if self._rotation_mtx is not None:
                self._quaternion = rotation_to_quaternion(self._rotation_mtx)
            elif self._euler_angles is not None:
                self._quaternion = rotation_to_quaternion(euler_to_rotation(self._euler_angles))
            else:
                raise ValueError
        return self._quaternion

    @quaternion.setter
    def quaternion(self, val: np.ndarray):
        self._quaternion = val
        self._rotation_mtx = None
        self._euler_angles = None

    @property
    def rotation_mtx(self) -> np.ndarray:
        if self._rotation_mtx is None:
            if self._quaternion is not None:
                self._rotation_mtx = quat_to_rot_mtx(self._quaternion)
            elif self._euler_angles is not None:
                self._rotation_mtx = euler_to_rotation(self._euler_angles)
            else:
                raise ValueError
        return self._rotation_mtx

    @rotation_mtx.setter
    def rotation_mtx(self, val: np.ndarray):
        self._rotation_mtx = val
        self._quaternion = None
        self._euler_angles = None

    @property
    def euler_angles(self) -> np.ndarray:
        if self._euler_angles is None:
            if self._quaternion is not None:
                self._euler_angles = quat_to_euler(self._quaternion)
            elif self._rotation_mtx is not None:
                self._euler_angles = quat_to_euler(rotation_to_quaternion(self._rotation_mtx))
            else:
                raise ValueError
        return self._euler_angles

    @euler_angles.setter
    def euler_angles(self, val: np.ndarray):
        self._euler_angles = val
        self._quaternion = None
        self._rotation_mtx = None

    @property
    def forward(self) -> np.ndarray:
        return self.rotation_mtx[:, 0]

    @property
    def right(self) -> np.ndarray:
        return self.rotation_mtx[:, 1]

    @property
    def left(self) -> np.ndarray:
        return self.rotation_mtx[:, 1] * -1

    @property
    def up(self) -> np.ndarray:
        return self.rotation_mtx[:, 2]

    @property
    def pitch(self) -> float:
        return self.euler_angles[0]

    @property
    def yaw(self) -> float:
        return self.euler_angles[1]

    @property
    def roll(self) -> float:
        return self.euler_angles[2]
