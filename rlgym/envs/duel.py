from rlgym.envs.environment import Environment
from rlgym.utils.gamestates import DuelState
import gym.spaces
import numpy as np


class Duel(Environment):
    def __init__(self, self_play: bool):
        super().__init__()
        self.GOAL_REWARD = 10
        self.GOAL_PUNISHMENT = -10
        self.BALL_TOUCH_REWARD = 0.1

        self.SAVE_REWARD = 1
        self.SAVE_PUNISHMENT = -1
        self.SHOT_REWARD = 1
        self.SHOT_PUNISHMENT = -1

        self.observation_space = gym.spaces.Box(-np.inf, np.inf, shape=(47,))
        self.action_space = gym.spaces.Box(-1, 1, shape=(8,))
        self.team_size = 1
        self.self_play = self_play
        self.agents = self.team_size * 2 if self.self_play else self.team_size
        self._prev_actions = np.zeros((self.agents, self.action_space.shape[0]), dtype=float)

        #TODO: send max_ticks and other configurable data to DLL as part of cvars
        self._ticks = 0
        self._max_ticks = 5*36000//6
        self._blue_score = 0
        self._orange_score = 0
        self._done = False
        self._match_shots = [0,0]
        self._match_saves = [0,0]

    def get_config(self):
        return '{} {}'.format(self.team_size, 1 if self.self_play else 0)

    def episode_reset(self):
        self._done = False
        self._ticks = 0
        self._prev_actions.fill(0)

    def build_observations(self, state):
        #print("STATE:", state)
        obs = []
        for i in range(self.agents):
            ob = [state.game_type]  # np.zeros(self.observation_space)
            ob += self._prev_actions[i].tolist()
            ob[0] = state.game_type   # Game type
            ob[1:9] = self._prev_actions[i]

            if self.self_play:
                if i < self.team_size:
                    ob.append(state.player.has_flip)
                    ob.append(state.player.boost_amount)
                    ob.append(state.player.on_ground)
                    ob += state.player.ball_data
                    ob += state.player.car_data
                    ob += state.player.opponent_car_data
                else:
                    ob.append(state.opponent.has_flip)
                    ob.append(state.opponent.boost_amount)
                    ob.append(state.opponent.on_ground)
                    ob += state.opponent.ball_data
                    ob += state.opponent.car_data
                    ob += state.opponent.opponent_car_data
            else:
                ob.append(state.player.has_flip)
                ob.append(state.player.boost_amount)
                ob.append(state.player.on_ground)
                ob += state.player.ball_data
                ob += state.player.car_data
                ob += state.player.opponent_car_data

            obs.append(ob)
        self._ticks += 1

        #print("BUILT OBS:\n",obs)
        return np.asarray(obs)

    def get_rewards(self, state):
        rewards = [0,0]
        if state.blue_score != self._blue_score:
            self._blue_score = state.blue_score
            self._done = True

            if state.player.ball_touched >= 1:
                rewards[0] += self.GOAL_REWARD

            rewards[1] += self.GOAL_PUNISHMENT

        if state.orange_score != self._orange_score:
            self._orange_score = state.orange_score
            self._done = True

            if state.opponent.ball_touched >= 1:
                rewards[1] += self.GOAL_REWARD

            rewards[0] += self.GOAL_PUNISHMENT

        if state.player.ball_touched:
            rewards[0] += self.BALL_TOUCH_REWARD

        if state.opponent.ball_touched:
            rewards[1] += self.BALL_TOUCH_REWARD

        if state.player.match_shots > self._match_shots[0]:
            self._match_shots[0] = state.player.match_shots
            rewards[0] += self.SHOT_REWARD
            rewards[1] += self.SHOT_PUNISHMENT

        if state.player.match_saves > self._match_saves[0]:
            self._match_saves[0] = state.player.match_saves
            rewards[0] += self.SAVE_REWARD
            rewards[1] += self.SAVE_PUNISHMENT

        if state.opponent.match_shots > self._match_shots[1]:
            self._match_shots[1] = state.opponent.match_shots
            rewards[1] += self.SHOT_REWARD
            rewards[0] += self.SHOT_PUNISHMENT

        if state.opponent.match_saves > self._match_saves[1]:
            self._match_saves[1] = state.opponent.match_saves
            rewards[1] += self.SAVE_REWARD
            rewards[0] += self.SAVE_PUNISHMENT

        #print(state)

        #print("COMPUTED REWARDS",rewards)
        return rewards

    def is_done(self, state):
        self._done = self._done or self._ticks >= self._max_ticks

        return self._done

    def parse_state(self, state_str):
        if state_str is None:
            return None

        state = DuelState(state_str)
        return state

    def format_actions(self, actions: np.ndarray):
        self._prev_actions[:] = actions[:]
        action_str = ''.join(["{} ".format(str(x)) for x in actions.ravel()])
        return action_str
