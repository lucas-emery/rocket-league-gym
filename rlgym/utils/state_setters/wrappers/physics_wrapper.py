from rlgym.utils.gamestates import PhysicsObject
import numpy as np


class PhysicsWrapper(object):

    def __init__(self, phys_obj: PhysicsObject = None):
        """
        PhysicsWrapper constructor. Under most circumstances, users should not expect to instantiate their own PhysicsWrapper objects.

        :param phys_obj: PhysicsObject object from which values will be read.
        """
        if phys_obj is None:
            self.position: np.ndarray = np.asarray([0, 0, 93])
            self.linear_velocity: np.ndarray = np.zeros(3)
            self.angular_velocity: np.ndarray = np.zeros(3)
        else:
            self._read_from_physics_object(phys_obj)

    def _read_from_physics_object(self, phys_obj: PhysicsObject):
        """
        A function to modify PhysicsWrapper values from values in a PhysicsObject object.
        """
        self.position = phys_obj.position
        self.linear_velocity = phys_obj.linear_velocity
        self.angular_velocity = phys_obj.angular_velocity

    def set_pos(self, x: float = None, y: float = None, z: float = None):
        """
        Sets position.

        :param x: Float indicating x position value.
        :param y: Float indicating y position value.
        :param z: Float indicating z position value.
        """
        if x is not None:
            self.position[0] = x
        if y is not None:
            self.position[1] = y
        if z is not None:
            self.position[2] = z

    def set_lin_vel(self, x: float = None, y: float = None, z: float = None):
        """
        Sets linear velocity.

        :param x: Float indicating x velocity value.
        :param y: Float indicating y velocity value.
        :param z: Float indicating z velocity value.
        """
        if x is not None:
            self.linear_velocity[0] = x
        if y is not None:
            self.linear_velocity[1] = y
        if z is not None:
            self.linear_velocity[2] = z

    def set_ang_vel(self, x: float = None, y: float = None, z: float = None):
        """
        Sets angular velocity.

        :param x: Float indicating x angular velocity value.
        :param y: Float indicating y angular velocity value.
        :param z: Float indicating z angular velocity value.
        """
        if x is not None:
            self.angular_velocity[0] = x
        if y is not None:
            self.angular_velocity[1] = y
        if z is not None:
            self.angular_velocity[2] = z

    def _encode(self) -> list:
        """
        Function called by a StateWrapper to produce a state string.

        :return: String containing value data.
        """
        encoded = np.concatenate((self.position, self.linear_velocity, self.angular_velocity))
        return encoded.tolist()
