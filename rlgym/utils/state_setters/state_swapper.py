from rlgym.utils.state_setters.state_setter import StateSetter
from rlgym.utils.state_setters.state_wrapper import (BLUE_ID1, ORANGE_ID1,
                                                     CarWrapper,
                                                     PhysicsWrapper)
from rlgym.utils.state_setters.wrappers.state_wrapper import StateWrapper

from copy import deepcopy
from random import getrandbits, shuffle
from typing import List

PI = 3.1415926535897932

class StateSwapper(StateSetter):
    MASK_SHUFFLE= 0b01
    MASK_SWAP_FRONT_BACK = 0b10
    MASK_SWAP_LEFT_RIGHT = 0b100

    BLUE_TEAM = 0
    ORANGE_TEAM = 1

    BLUE_CARS = [BLUE_ID1 + n for n in range(4)]
    ORANGE_CARS = [ORANGE_ID1 + n for n in range(4)]

    X_DIM = 0
    Y_DIM = 1
    Z_DIM = 2


    def __init__(self, state_setter: StateSetter, shuffle_teams=False, swap_front_back=False, swap_left_right=False) -> None:
        self.state_setter = state_setter
        self.opt_shuffle_teams = shuffle_teams
        self.opt_swap_front_back = swap_front_back
        self.opt_swap_left_right = swap_left_right


    def reset(self, state_wrapper: StateWrapper):
        self.state_setter.reset(state_wrapper)
        self._debug(state_wrapper)
        bits = getrandbits(3)
        if self.opt_shuffle_teams and (bits & StateSwapper.MASK_SHUFFLE):
            self.shuffle_teams(state_wrapper)

        if self.opt_swap_front_back and (bits & StateSwapper.MASK_SWAP_FRONT_BACK):
            self.swap_front_back(state_wrapper)

        if self.opt_swap_left_right and (bits & StateSwapper.MASK_SWAP_LEFT_RIGHT):
            self.swap_left_right(state_wrapper)

        self._debug(state_wrapper)


    def _debug(self, state_wrapper: StateWrapper):
        print("\n".join(f"Car {car.id}, team: {car.team_num}, pos: {car.position}" for car in state_wrapper.cars))
        ball = state_wrapper.ball
        print(f"Ball pos: {ball.position}")


    @staticmethod
    def _normalize_cars(cars: List[CarWrapper]):
        sorted_cars = list(sorted(cars, key = lambda car: car.id))
        for car in sorted_cars:
            car.team_num = StateSwapper.BLUE_TEAM if car.id in StateSwapper.BLUE_CARS else StateSwapper.ORANGE_TEAM
        return sorted_cars


    @staticmethod
    def _map_cars(cars: List[CarWrapper], from_ids: List[int], to_ids: List[int]):
        car_ids = [ car.id for car in cars ]
        assert len(from_ids) == len(to_ids), "from_ids and to_ids must be of equal length"
        assert len(set(from_ids)) == len(set(to_ids)), "from_ids and to_ids must not contain duplicates"
        assert len(from_ids) <= len(car_ids), "length of from_ids must not be larger than the cars list"
        transformation = [ to_ids[from_ids.index(car_id)] if car_id in from_ids else car_id for car_id in car_ids ]
        source_car_copies = [ deepcopy(car) for car in cars ]
        def produce_swapped_cars():
            for (idx, car) in enumerate(source_car_copies):
                car.id = transformation[idx]
                yield car
        return StateSwapper._normalize_cars(list(produce_swapped_cars()))


    @staticmethod
    def _mirror_car_rotation(car_object: CarWrapper, dimension: int):
        if StateSwapper.X_DIM == dimension:
            car_object.set_rot(
                1 * car_object.rotation[0], # pitch
                PI - car_object.rotation[1], # yaw
                -1 * car_object.rotation[2], # roll
            )
        if StateSwapper.Y_DIM == dimension:
            car_object.set_rot(
                1 * car_object.rotation[0], # pitch
                -1 * car_object.rotation[1], # yaw
                -1 * car_object.rotation[2], # roll
            )


    @staticmethod
    def _flip_physics_dimension(physics_object: PhysicsWrapper, dimension: int):
        physics_object.position[dimension] *= -1
        physics_object.linear_velocity[dimension] *= -1
        if isinstance(physics_object, CarWrapper):
            StateSwapper._mirror_car_rotation(physics_object, dimension)


    def shuffle_teams(self, state_wrapper: StateWrapper):
        """ The cars within a team are randomly swapped with each other """
        team_size = len(state_wrapper.cars) // 2
        gamemode_blue_cars = StateSwapper.BLUE_CARS[:team_size]
        gamemode_orange_cars = StateSwapper.ORANGE_CARS[:team_size]
        blue = list(gamemode_blue_cars)
        orange = list(gamemode_orange_cars)
        shuffle(blue)
        shuffle(orange)

        state_wrapper.cars[:] = StateSwapper._map_cars(
            state_wrapper.cars, gamemode_blue_cars + gamemode_orange_cars,
            blue + orange
        )


    def swap_teams(self, state_wrapper):
        """ Blue cars move to Orange positions, orange to blue """
        team_size = len(state_wrapper.cars) // 2
        gamemode_blue_cars = StateSwapper.BLUE_CARS[:team_size]
        gamemode_orange_cars = StateSwapper.ORANGE_CARS[:team_size]
        state_wrapper.cars[:] = StateSwapper._map_cars(
            state_wrapper.cars,
            gamemode_blue_cars + gamemode_orange_cars,
            gamemode_orange_cars + gamemode_blue_cars
        )


    def swap_front_back(self, state_wrapper: StateWrapper):
        self.swap_teams(state_wrapper)
        for car in state_wrapper.cars:
            StateSwapper._flip_physics_dimension(car, StateSwapper.X_DIM)
        StateSwapper._flip_physics_dimension(state_wrapper.ball, StateSwapper.X_DIM)


    def swap_left_right(self, state_wrapper: StateWrapper):
        for car in state_wrapper.cars:
            StateSwapper._flip_physics_dimension(car, StateSwapper.Y_DIM)
        StateSwapper._flip_physics_dimension(state_wrapper.ball, StateSwapper.Y_DIM)
