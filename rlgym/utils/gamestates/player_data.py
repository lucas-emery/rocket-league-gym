"""
A class containing all data about a player in the game.
"""

from rlgym.utils.gamestates import PhysicsObject


class PlayerData(object):
    def __init__(self):
        self.car_id: int = -1
        self.team_num: int = -1
        self.match_goals: int = -1
        self.match_saves: int = -1
        self.match_shots: int = -1
        self.match_demolishes: int = -1
        self.boost_pickups: int = -1
        self.is_demoed: bool = False
        self.on_ground: bool = False
        self.ball_touched: bool = False
        self.has_jump: bool = False
        self.has_flip: bool = False
        self.boost_amount: float = -1
        self.car_data: PhysicsObject = PhysicsObject()
        self.inverted_car_data: PhysicsObject = PhysicsObject()

    def __str__(self):
        output = "****PLAYER DATA OBJECT****\n" \
                 "Match Goals: {}\n" \
                 "Match Saves: {}\n" \
                 "Match Shots: {}\n" \
                 "Match Demolishes: {}\n" \
                 "Boost Pickups: {}\n" \
                 "Is Alive: {}\n" \
                 "On Ground: {}\n" \
                 "Ball Touched: {}\n" \
                 "Has Jump: {}\n" \
                 "Has Flip: {}\n" \
                 "Boost Amount: {}\n" \
                 "Car Data: {}\n" \
                 "Inverted Car Data: {}"\
            .format(self.match_goals,
                    self.match_saves,
                    self.match_shots,
                    self.match_demolishes,
                    self.boost_pickups,
                    not self.is_demoed,
                    self.on_ground,
                    self.ball_touched,
                    self.has_jump,
                    self.has_flip,
                    self.boost_amount,
                    self.car_data,
                    self.inverted_car_data)
        return output
