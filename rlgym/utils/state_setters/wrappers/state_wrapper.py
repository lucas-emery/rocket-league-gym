"""
Data classes to permit the manipulation of environment variables.
"""

from rlgym.utils.gamestates.game_state import GameState
from rlgym.utils.state_setters.wrappers import PhysicsWrapper, CarWrapper
from rlgym.utils.common_values import BLUE_TEAM, ORANGE_TEAM
from typing import List


class StateWrapper(object):
    BLUE_ID1 = 1
    ORANGE_ID1 = 5

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
                self.cars.append(CarWrapper(BLUE_TEAM, StateWrapper.BLUE_ID1 + i))
            for i in range(orange_count):
                self.cars.append(CarWrapper(ORANGE_TEAM, StateWrapper.ORANGE_ID1 + i))
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

    def blue_cars(self) -> List[CarWrapper]:
        return [c for c in self.cars if c.team_num == BLUE_TEAM]

    def orange_cars(self) -> List[CarWrapper]:
        return [c for c in self.cars if c.team_num == ORANGE_TEAM]

    def format_state(self) -> list:
        """
        A function to format the values stored within a StateWrapper object.
        These values are sent as a string to be applied to the game engine upon an environment reset.

        :return: String containing all state values.
        """
        # Ball: X, Y, Z, VX, VY, VZ, AVX, AVY, AVX
        # Cars: ID, X, Y, Z, VX, VY, VZ, AVX, AVY, AVZ, RX, RY, RZ, Boost

        # retrieve the ball string
        ball_state = self.ball._encode()

        # retrieve car strings
        car_states = []
        for c in self.cars:
            car_states += c._encode()

        encoded = ball_state + car_states

        return encoded
