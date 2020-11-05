from rlgym.utils.gamestates import GameState
from rlgym.utils.gamestates import PlayerData
import numpy as np


class DoubleState(GameState):
    def __init__(self, state_str):
        super().__init__()
        self.players = [PlayerData(), PlayerData()]
        self.opponents = [PlayerData(), PlayerData()]

        self.decode(state_str)

    def _decode(self, state_str):
        p_len = GameState.PLAYER_INFO_LENGTH
        b_len = GameState.BALL_STATE_LENGTH
        packet_len = p_len + b_len
        start = 3

        state_vals = GameState._decode_state_str(state_str)
        num_ball_packets = 2
        num_player_packets = (len(state_vals) - num_ball_packets * b_len) / p_len

        # print("decoding state",state_str)
        ticks = state_vals[0]
        # print(ticks)
        self.blue_score = state_vals[1]
        self.orange_score = state_vals[2]

        # Player data.
        full_player_data = state_vals[start:start + p_len]
        # print("FULL PLAYER DATA:", full_player_data)
        player_state_data = full_player_data[:GameState.PLAYER_CAR_STATE_LENGTH]
        player_tertiary_data = full_player_data[GameState.PLAYER_CAR_STATE_LENGTH:]
        # print(player_tertiary_data,"\n",len(player_tertiary_data))

        self.player.car_data.decode_car_data(player_state_data)

        self.player.match_goals = player_tertiary_data[0]
        self.player.match_saves = player_tertiary_data[1]
        self.player.match_shots = player_tertiary_data[2]
        self.player.match_demolishes = player_tertiary_data[3]
        self.player.boost_pickups = player_tertiary_data[4]
        self.player.is_alive = player_tertiary_data[5]
        self.player.on_ground = player_tertiary_data[6]
        self.player.ball_touched = player_tertiary_data[7]
        self.player.has_flip = player_tertiary_data[8]
        self.player.boost_amount = player_tertiary_data[9]

        start += p_len

        self.player.opponent_car_data.decode_car_data(state_vals[start:start + GameState.PLAYER_CAR_STATE_LENGTH])
        start += p_len

        self.player.ball_data.decode_ball_data(state_vals[start:start + b_len])
        start += b_len

        # Opponent data.
        # We fill the opponent's opponent car data first here instead of its own car data because the inverted state stream
        # is appended to the non-inverted state stream, so this will be the inverted state of the player's car data, not the opponent's
        self.opponent.opponent_car_data.decode_car_data(state_vals[start:start + GameState.PLAYER_CAR_STATE_LENGTH])
        start += p_len

        full_opponent_data = state_vals[start:start + p_len]
        opponent_state_data = full_opponent_data[:GameState.PLAYER_CAR_STATE_LENGTH]
        opponent_tertiary_data = full_opponent_data[GameState.PLAYER_CAR_STATE_LENGTH:]
        # print("FULL OPPONENT DATA:",full_opponent_data)

        self.opponent.car_data.decode_car_data(opponent_state_data)

        self.opponent.match_goals = opponent_tertiary_data[0]
        self.opponent.match_saves = opponent_tertiary_data[1]
        self.opponent.match_shots = opponent_tertiary_data[2]
        self.opponent.match_demolishes = opponent_tertiary_data[3]
        self.opponent.boost_pickups = opponent_tertiary_data[4]
        self.opponent.is_alive = opponent_tertiary_data[5]
        self.opponent.on_ground = opponent_tertiary_data[6]
        self.opponent.ball_touched = opponent_tertiary_data[7]
        self.opponent.has_flip = opponent_tertiary_data[8]
        self.opponent.boost_amount = opponent_tertiary_data[9]

        start += p_len

        self.opponent.ball_data.decode_ball_data(state_vals[start:start + b_len])
        start += b_len

        # print("State decoded!")
        # print(self)


    def __str__(self):
        output = "{}DUELS GAME STATE OBJECT{}\n" \
                 "Game Type: {}\n" \
                 "Orange Score: {}\n" \
                 "Blue Score: {}\n" \
                 "{}\n" \
                 "{}\n" \
                 "".format("*" * 8, "*" * 8,
                           self.game_type,
                           self.orange_score,
                           self.blue_score,
                           self.player,
                           self.opponent)

        return output