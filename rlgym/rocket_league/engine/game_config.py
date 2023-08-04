

class GameConfig:
    gravity: float
    boost_consumption: float

    __slots__ = tuple(__annotations__)

    def __str__(self):
        output = "****GAME CONFIG****\n" \
                 "Gravity: {}\n" \
                 "Boost Consumption: {}\n" \
                 "".format(self.gravity,
                           self.boost_consumption)

        return output
