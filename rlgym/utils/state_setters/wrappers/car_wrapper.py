from rlgym.utils.state_setters.wrappers import PhysicsWrapper
from rlgym.utils.gamestates import PlayerData
import numpy as np



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
            self.position = np.asarray([id * 100, 0, 17])
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

    def _encode(self) -> list:
        """
        Function called by a StateWrapper to produce a state string.

        :return: String containing value data.
        """
        encoded = np.concatenate(((self.id,), self.position, self.linear_velocity,
                                    self.angular_velocity, self.rotation, (self.boost,)))

        return encoded.tolist()