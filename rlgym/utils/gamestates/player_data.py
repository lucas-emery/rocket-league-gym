from rlgym.utils.gamestates import PhysicsObject

class PlayerData(object):
    def __init__(self):
        self.car_id = None
        self.team_num = None
        self.match_goals = None
        self.match_saves = None
        self.match_shots = None
        self.match_demolishes = None
        self.boost_pickups = None
        self.is_alive = None
        self.on_ground = None
        self.ball_touched = None
        self.has_flip = None
        self.boost_amount = None
        self.car_data = PhysicsObject()
        self.inverted_car_data = PhysicsObject()

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
                 "Has Flip: {}\n" \
                 "Boost Amount: {}\n" \
                 "Car Data: {}\n" \
                 "Inverted Car Data: {}"\
            .format(self.match_goals,
                    self.match_saves,
                    self.match_shots,
                    self.match_demolishes,
                    self.boost_pickups,
                    self.is_alive,
                    self.on_ground,
                    self.ball_touched,
                    self.has_flip,
                    self.boost_amount,
                    self.car_data,
                    self.inverted_car_data)
        return output