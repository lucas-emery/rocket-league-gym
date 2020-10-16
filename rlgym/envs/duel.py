from rlgym.envs.environment import Environment
from rlgym.utils.gamestates import DuelState
from rlgym.utils import Math
from rlgym.utils.reward_functions import ShootBallReward
import gym.spaces
import numpy as np

class Duel(Environment):
    def __init__(self, self_play: bool):
        super().__init__()
        #TODO: Sort out where all these variables should go. More than one class will need many of these.
        self.observation_space = gym.spaces.Box(-np.inf,np.inf,shape=(47,))
        self.action_space = gym.spaces.Box(-1,1,shape=(8,))
        self.team_size = 1
        self.self_play = self_play
        self.agents = self.team_size * 2 if self.self_play else self.team_size
        self._prev_actions = np.zeros((self.agents, self.action_space.shape[0]), dtype=float)

        self.spawn_opponents = False
        self._tick_skip = 6
        ep_len_minutes = 1
        ticks_per_sec = 120
        ticks_per_min = ticks_per_sec * 60
        self._max_ticks = int(round(ep_len_minutes * ticks_per_min / self._tick_skip))
        self._tick = 0
        self._random_resets = 1

        self._blue_score = 0
        self._orange_score = 0
        self._done = False
        self._match_shots = [0,0]
        self._match_saves = [0,0]

        self._start_ball_dist = None
        self._best_ball_dist = None
        self._reward_fn = ShootBallReward()


    def episode_reset(self):
        self._done = False
        self._prev_actions.fill(0)
        self._reward_fn.reset()
        self._tick = 0

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
                #ob += state.player.opponent_car_data
                ob += self.get_random_opponent_state()

            obs.append(ob)

        self._tick+=1
        return np.asarray(obs)

    def get_rewards(self, state):
        # TODO: change the reward function to take a player data packet as input so it can compute the rewards for self-play
        if state.blue_score != self._blue_score or state.orange_score != self._orange_score:
            self._orange_score = state.orange_score
            self._blue_score = state.blue_score
            self._done = True

        if self.is_done(state):
            reward = self._reward_fn.get_final_reward(state)
        else:
            reward = self._reward_fn.get_reward(state)

        return [reward,0]

    def is_done(self, state):
        if self._tick >= self._max_ticks:
            self._done = True
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

    def get_random_opponent_state(self):
        means = [-7.55690032e+00, -7.67272187e+02, 3.99790479e+01, 4.33080865e-01, 3.29746054e-03, 9.68255500e-03,
                 4.10564683e-01, 1.64972058e+01, -9.52952112e+00, 1.21217917e-01, 6.23036234e-03, -1.84941779e-03,
                 -1.82993569e-02]

        stds = [2.22632843e+03, 3.31466701e+03, 7.04738414e+01, 5.49264807e-01, 1.37360694e-01, 1.42669913e-01,
                5.50325801e-01, 6.42938410e+02, 7.39945204e+02, 1.34840452e+02, 7.39983198e-01, 7.07553505e-01,
                1.78035710e+00]

        mu = np.asarray(means)
        sigma = np.asarray(stds)

        obs = np.random.randn(len(means)) * sigma + mu
        return obs.tolist()

    def get_config(self):
        return '{} {} {} {} {} {}'.format(self.team_size,
                                 1 if self.self_play else 0,
                                 1 if self.spawn_opponents else 0,
                                 self._random_resets,
                                 self._max_ticks * self._tick_skip,
                                 self._tick_skip
                                 )