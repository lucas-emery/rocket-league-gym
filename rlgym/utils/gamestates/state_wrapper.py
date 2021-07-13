"""
Data class to permit the construction and manipulation of a game state. 
"""

from typing import List
from rlgym.utils.gamestates.physics_object import PhysicsObject
from rlgym.utils.gamestates.game_state import GameState
import numpy as np

BLUE_ID1 = 1
ORANGE_ID1 = 5


class StateWrapper(object):

    def __init__(self, blue_count: int = 0, orange_count: int = 0, game_state=None):
        """
        StateWrapper constructor. Under most circumstances, users should not expect to instantiate their own StateWrapper objects.

        Parameters:
        -----------
        blue_count: int. The amount of players on the blue team.
        orange_count: int. The amount of players on the orange team.
        game_state (optional): GameState. A GameState object for values to be copied from.
        """
        if game_state is None:
            self.ball: PhysicsObject = PhysicsObject()
            self.blue: List[PhysicsObject] = [PhysicsObject()
                                              for _ in range(blue_count)]
            self.orange: List[PhysicsObject] = [PhysicsObject()
                                                for _ in range(orange_count)]
            self.blue_boost: List[float] = [0 for _ in range(blue_count)]
            self.orange_boost: List[float] = [0 for _ in range(orange_count)]
        else:
            self._read_from_gamestate(game_state)

    def _read_from_gamestate(self, game_state: GameState):
        """
        A function to modify the StateWrapper with values read in from a GameState object.
        """
        self.ball: PhysicsObject = game_state.ball
        self.blue: List[PhysicsObject] = []
        self.orange: List[PhysicsObject] = []
        for player in game_state.players:
            if player.team_num == 0:
                self.blue.append(player.car_data)
                self.blue_boost.append(player.boost_amount)
            elif player.team_num == 1:
                self.orange.append(player.car_data)
                self.orange_boost.append(player.boost_amount)

    def format_state(self) -> str:
        """
        A function to format the values stored within a StateWrapper object. 
        These values are sent as a string to be applied to the game engine upon an environment reset.
        """
        # Ball: X, Y, Z, VX, VY, VZ, AVX, AVY, AVX
        # Cars: ID, X, Y, Z, VX, VY, VZ, AVX, AVY, AVZ, RX, RY, RZ, Boost
        state_str = ""

        # create the ball string
        ball_arr = np.concatenate((self.ball.position,
                                   self.ball.linear_velocity, self.ball.angular_velocity), dtype=str)
        ball_str = " ".join(ball_arr)
        state_str += ball_str

        # create strings for all blue team players
        for i in range(len(self.blue)):
            player = self.blue[i]
            player_arr = np.concatenate((player.position, player.linear_velocity,
                                         player.angular_velocity, player.euler_angles()), dtype=str)
            player_str = " ".join(player_arr)
            state_str += " " + str(BLUE_ID1 + i) + " " + \
                player_str + " " + str(self.blue_boost[i])

        # create strings for all orange team players
        for i in range(len(self.orange)):
            player = self.orange[i]
            player_arr = np.concatenate((player.position, player.linear_velocity,
                                         player.angular_velocity, player.euler_angles()), dtype=str)
            player_str = " ".join(player_arr)
            state_str += " " + str(ORANGE_ID1 + i) + " " + \
                player_str + " " + str(self.orange_boost[i])

        return state_str
