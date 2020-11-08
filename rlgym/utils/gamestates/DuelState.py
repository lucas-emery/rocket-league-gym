from rlgym.utils.gamestates import GameState
from rlgym.utils.gamestates import PlayerData, PhysicsObject
import numpy as np


class DuelState(GameState):
    def __init__(self, state_str):
        super().__init__()
        self.players = []

        self.ball = PhysicsObject()
        self.inv_ball = PhysicsObject()

        self.decode(state_str)

    def _decode(self, state_str):
        p_len = GameState.PLAYER_INFO_LENGTH
        b_len = GameState.BALL_STATE_LENGTH
        start = 3

        state_vals = GameState._decode_state_str(state_str)
        num_ball_packets = 1
        #The state will contain the ball, the mirrored ball, every player, every player mirrored, the score for both teams, and the number of ticks since the last packet was sent.
        num_player_packets = int((len(state_vals) - num_ball_packets * b_len - start) / p_len)
        #print(len(state_vals), " | ", num_ball_packets, " | ", num_player_packets)

        #print(state_str)

        ticks = state_vals[0]
        # print(ticks)
        self.blue_score = state_vals[1]
        self.orange_score = state_vals[2]

        ball_data = state_vals[start:start+b_len]
        #print("BALL:",ball_data)
        self.ball.decode_ball_data(ball_data)
        start += b_len//2

        inv_ball_data = state_vals[start:start+b_len]
        #print("INV_BALL:",inv_ball_data)
        self.inv_ball.decode_ball_data(inv_ball_data)
        start += b_len//2

        for i in range(num_player_packets):
            player = self.decode_player(state_vals[start:start+p_len])
            self.players.append(player)
            start += p_len

            if player.ball_touched:
                self.last_touch = player.car_id


        #print("State decoded!")
        #print(self)

    def decode_player(self, full_player_data):
        #print("DECODING PLAYER ",full_player_data)
        player_data = PlayerData()
        c_len = GameState.PLAYER_CAR_STATE_LENGTH
        t_len = GameState.PLAYER_TERTIARY_INFO_LENGTH

        start = 2

        car_data = full_player_data[start:start+c_len]
        player_data.car_data.decode_car_data(car_data)
        start += c_len

        inv_state_data = full_player_data[start:start+c_len]
        player_data.inverted_car_data.decode_car_data(inv_state_data)
        start += c_len

        tertiary_data = full_player_data[start:start+t_len]

        player_data.match_goals = int(tertiary_data[0])
        player_data.match_saves = int(tertiary_data[1])
        player_data.match_shots = int(tertiary_data[2])
        player_data.match_demolishes = int(tertiary_data[3])
        player_data.boost_pickups = int(tertiary_data[4])
        player_data.is_alive = True if tertiary_data[5] > 0 else False
        player_data.on_ground = True if tertiary_data[6] > 0 else False
        player_data.ball_touched = True if tertiary_data[7] > 0 else False
        player_data.has_flip = True if tertiary_data[8] > 0 else False
        player_data.boost_amount = float(tertiary_data[9])
        player_data.car_id = int(full_player_data[0])
        player_data.team_num = int(full_player_data[1])

        return player_data


    def __str__(self):
        output = "{}DUELS GAME STATE OBJECT{}\n" \
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
                           self.inv_ball)

        return output

