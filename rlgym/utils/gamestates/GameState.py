from abc import abstractmethod


class GameState(object):
    BALL_STATE_LENGTH = 9
    PLAYER_INFO_LENGTH = 23
    PLAYER_CAR_STATE_LENGTH = 13
    PLAYER_TERTIARY_INFO_LENGTH = 10

    def __init__(self):
        self.game_type = 0
        self.blue_score = None
        self.orange_score = None

    def decode(self, state_str):
        assert type(state_str) == str, "UNABLE TO DECODE STATE OF TYPE {}".format(type(state_str))
        self._decode(state_str)

    @abstractmethod
    def _decode(self, state_str):
        raise NotImplementedError