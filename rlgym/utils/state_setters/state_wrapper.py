"""
Data classes to permit the manipulation of environment variables.
"""

from rlgym.utils.gamestates.player_data import PlayerData
from rlgym.utils.gamestates.physics_object import PhysicsObject
from rlgym.utils.gamestates.game_state import GameState
from typing import List
import numpy as np

BLUE_ID1 = 1
ORANGE_ID1 = 5


class StateWrapper(object):

    def __init__(self, blue_count: int = 0, orange_count: int = 0, game_state=None):
        """
        StateWrapper constructor. Under most circumstances, users should not expect to instantiate their own StateWrapper objects.

        :param blue_count: Integer indicating the amount of players on the blue team.
        :param orange_count: Integer indicating The amount of players on the orange team.
        :param game_state: GameState object for values to be copied from.

        NOTE: blue_count and orange_count will be ignored if a GameState object is passed.
        """
        if game_state is None:
            self.ball: PhysicsWrapper = PhysicsWrapper()
            self.cars: List[CarWrapper] = []
            for i in range(blue_count):
                self.cars.append(CarWrapper(0, BLUE_ID1 + i))
            for i in range(orange_count):
                self.cars.append(CarWrapper(1, ORANGE_ID1 + i))
        else:
            self._read_from_gamestate(game_state)

    def _read_from_gamestate(self, game_state: GameState):
        """
        A function to modify the StateWrapper with values read in from a GameState object.
        """
        self.ball: PhysicsWrapper = PhysicsWrapper(game_state.ball)
        self.cars: List[CarWrapper] = []
        for player in game_state.players:
            self.cars.append(CarWrapper(player_data=player))

    def format_state(self) -> str:
        """
        A function to format the values stored within a StateWrapper object. 
        These values are sent as a string to be applied to the game engine upon an environment reset.

        :return: String containing all state values.
        """
        # Ball: X, Y, Z, VX, VY, VZ, AVX, AVY, AVX
        # Cars: ID, X, Y, Z, VX, VY, VZ, AVX, AVY, AVZ, RX, RY, RZ, Boost

        # retrieve the ball string
        ball_str = self.ball._encode()

        # retrieve car strings
        car_str_list = [c._encode() for c in self.cars]

        return f'{ball_str} {" ".join(car_str_list)}'


class PhysicsWrapper(object):

    def __init__(self, phys_obj: PhysicsObject = None):
        """
        PhysicsWrapper constructor. Under most circumstances, users should not expect to instantiate their own PhysicsWrapper objects.

        :param phys_obj: PhysicsObject object from which values will be read.
        """
        if phys_obj is None:
            self.position: np.ndarray = np.zeros(3)
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

    def _encode(self) -> str:
        """
        Function called by a StateWrapper to produce a state string.

        :return: String containing value data.
        """
        state_arr = np.concatenate((self.position,
                                    self.linear_velocity, self.angular_velocity), dtype=str)
        return " ".join(state_arr)


class CarWrapper(PhysicsWrapper):

    def __init__(self, team_num: int = -1, id: int = -1, player_data: PlayerData = None):
        """
        CarWrapper constructor. Under most circumstances, users should not expect to instantiate their own CarWrapper objects.

        :param team_num: Integer indicating 0 for blue and 1 for orange.
        :param id: Integer indicating the spectator ID assigned to the car.
        :param player_data: PlayerData object for values to be copied from.

        NOTE: team_num and id will be ignored if a PlayerData object is passed.
        """
        if player_data is None:
            super().__init__()
            self.rotation: np.ndarray = np.zeros(3)
            self.team_num: int = team_num
            self.id: int = id
            self.boost: float = 0
        else:
            super().__init__(phys_obj=player_data.car_data)
            self._read_from_player_data(player_data)

    def _read_from_player_data(self, player_data: PlayerData):
        """
        A function to modify CarWrapper values from values in a PlayerData object.
        """
        self.rotation = player_data.car_data.euler_angles()
        self.team_num = player_data.team_num
        self.id = player_data.car_id
        self.boost = player_data.boost_amount

    def set_rot(self, pitch: float = None, yaw: float = None, roll: float = None):
        """
        Sets rotation in terms of euler angles.
        """
        if pitch is not None:
            self.rotation[0] = pitch
        if yaw is not None:
            self.rotation[1] = yaw
        if roll is not None:
            self.rotation[2] = roll

    def _encode(self) -> str:
        """
        Function called by a StateWrapper to produce a state string.

        :return: String containing value data.
        """
        state_arr = np.concatenate((self.position, self.linear_velocity,
                                    self.angular_velocity, self.rotation), dtype=str)
        return f'{self.id} {" ".join(state_arr)} {self.boost}'
