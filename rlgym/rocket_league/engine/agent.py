from rlgym.rocket_league.engine.physics_object import PhysicsObject


class Agent:

    team_num: int
    match_goals: int
    match_saves: int
    match_shots: int
    match_demolishes: int
    boost_pickups: int
    is_demoed: bool
    on_ground: bool
    ball_touched: bool
    has_jump: bool
    has_flip: bool
    boost_amount: float
    car: PhysicsObject
    inverted_car: PhysicsObject

    __slots__ = tuple(__annotations__)

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
                 "Car: {}\n" \
                 "Inverted Car: {}"\
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
                    self.car,
                    self.inverted_car)
        return output
