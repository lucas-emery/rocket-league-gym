from typing import Dict, Any

from rlgym.api.config.state_mutator import StateMutator
from rlgym.rocket_league.common_values import BLUE_TEAM, OCTANE, ORANGE_TEAM
from rlgym.rocket_league.engine.car import Car
from rlgym.rocket_league.engine.game_state import GameState
from rlgym.rocket_league.engine.physics_object import PhysicsObject


class FixedTeamSizeMutator(StateMutator[GameState]):

    def __init__(self, blue_size=1, orange_size=1):
        self.blue_size = blue_size
        self.orange_size = orange_size

    def apply(self, state: GameState, shared_info: Dict[str, Any]) -> None:
        assert len(state.cars) == 0  # This mutator doesn't support other team size mutators

        for idx in range(self.blue_size):
            car = self._new_car()
            car.team_num = BLUE_TEAM
            state.cars['blue-{}'.format(idx)] = car

        for idx in range(self.orange_size):
            car = self._new_car()
            car.team_num = ORANGE_TEAM
            state.cars['orange-{}'.format(idx)] = car

    def _new_car(self) -> Car:
        car = Car()
        car.hitbox_type = OCTANE
        car.physics = PhysicsObject()
        return car
