"""
    Object to contain all relevant information about the game state.
"""

import numpy as np
from typing import List, Optional
from rlgym.utils.gamestates import PlayerData, PhysicsObject


class GameState(object):
    BOOST_PADS_LENGTH = 34
    BALL_STATE_LENGTH = 18
    PLAYER_CAR_STATE_LENGTH = 13
    PLAYER_TERTIARY_INFO_LENGTH = 11
    PLAYER_INFO_LENGTH = 2 + 2 * PLAYER_CAR_STATE_LENGTH + PLAYER_TERTIARY_INFO_LENGTH

    def __init__(self, state_floats: List[float] = None):
        self.game_type: int = 0
        self.blue_score: int = -1
        self.orange_score: int = -1
        self.last_touch: Optional[int] = -1

        self.players: List[PlayerData] = []

        self.ball: PhysicsObject = PhysicsObject()
        self.inverted_ball: PhysicsObject = PhysicsObject()

        # List of "booleans" (1 or 0)
        self.boost_pads: np.ndarray = np.zeros(GameState.BOOST_PADS_LENGTH, dtype=np.float32)
        self.inverted_boost_pads: np.ndarray = np.zeros_like(self.boost_pads, dtype=np.float32)

        if state_floats is not None:
            self.decode(state_floats)

    def decode(self, state_floats: List[float]):
        """
        Decode a string containing the current game state from the Bakkesmod plugin.
        :param state_floats: String containing the game state.
        """
        assert type(state_floats) == list, "UNABLE TO DECODE STATE OF TYPE {}".format(type(state_floats))
        self._decode(state_floats)

    def _decode(self, state_vals: List[float]):
        pads_len = GameState.BOOST_PADS_LENGTH
        p_len = GameState.PLAYER_INFO_LENGTH
        b_len = GameState.BALL_STATE_LENGTH
        start = 3

        num_ball_packets = 1
        # The state will contain the ball, the mirrored ball, every player, every player mirrored, the score for both teams, and the number of ticks since the last packet was sent.
        num_player_packets = int((len(state_vals) - num_ball_packets * b_len - start - pads_len) / p_len)

        ticks = int(state_vals[0])

        self.blue_score = int(state_vals[1])
        self.orange_score = int(state_vals[2])

        self.boost_pads[:] = state_vals[start:start + pads_len]
        self.inverted_boost_pads[:] = self.boost_pads[::-1]
        start += pads_len

        ball_data = state_vals[start:start + b_len]
        self.ball.decode_ball_data(np.asarray(ball_data))
        start += b_len // 2

        inv_ball_data = state_vals[start:start + b_len]
        self.inverted_ball.decode_ball_data(np.asarray(inv_ball_data))
        start += b_len // 2

        for i in range(num_player_packets):
            player = self._decode_player(state_vals[start:start + p_len])
            self.players.append(player)
            start += p_len

            if player.ball_touched:
                self.last_touch = player.car_id
                
        self.players = sorted(self.players, key=lambda p: p.car_id) #YOU'RE WELCOME RANGLER, THIS WAS MY INNOVATION.

    def _decode_player(self, full_player_data):
        player_data = PlayerData()
        c_len = GameState.PLAYER_CAR_STATE_LENGTH
        t_len = GameState.PLAYER_TERTIARY_INFO_LENGTH

        start = 2

        car_data = full_player_data[start:start + c_len]
        player_data.car_data.decode_car_data(np.asarray(car_data))
        start += c_len

        inv_state_data = full_player_data[start:start + c_len]
        player_data.inverted_car_data.decode_car_data(np.asarray(inv_state_data))
        start += c_len

        tertiary_data = full_player_data[start:start + t_len]

        player_data.match_goals = int(tertiary_data[0])
        player_data.match_saves = int(tertiary_data[1])
        player_data.match_shots = int(tertiary_data[2])
        player_data.match_demolishes = int(tertiary_data[3])
        player_data.boost_pickups = int(tertiary_data[4])
        player_data.is_demoed = True if tertiary_data[5] > 0 else False
        player_data.on_ground = True if tertiary_data[6] > 0 else False
        player_data.ball_touched = True if tertiary_data[7] > 0 else False
        player_data.has_jump = True if tertiary_data[8] > 0 else False
        player_data.has_flip = True if tertiary_data[9] > 0 else False
        player_data.boost_amount = float(tertiary_data[10])
        player_data.car_id = int(full_player_data[0])
        player_data.team_num = int(full_player_data[1])

        return player_data

    def __str__(self):
        output = "{}GAME STATE OBJECT{}\n" \
                 "Game Type: {}\n" \
                 "Orange Score: {}\n" \
                 "Blue Score: {}\n" \
                 "PLAYERS: {}\n" \
                 "BALL: {}\n" \
                 "INV_BALL: {}\n" \
                 "".format("*" * 8, "*" * 8,
                           self.game_type,
                           self.orange_score,
                           self.blue_score,
                           self.players,
                           self.ball,
                           self.inverted_ball)

        return output

