from rlgym.envs.environment import Environment
from rlgym.utils.gamestates import GameState, PhysicsObject
from rlgym.utils import common_values
import gym.spaces
import numpy as np
from typing import List, Union


class Match(Environment):
    def __init__(self,
                 team_size=1,
                 tick_skip=8,
                 game_speed=100,
                 spawn_opponents=False,
                 random_resets=False,
                 self_play=False,
                 reward_function=None,
                 terminal_conditions=None,
                 obs_builder=None):
        super().__init__()

        self._game_speed = game_speed
        self._team_size = team_size
        self._self_play = self_play
        self._spawn_opponents = spawn_opponents
        self._tick_skip = tick_skip
        self._random_resets = random_resets
        self._reward_fn = reward_function
        self._terminal_conditions = terminal_conditions
        self._obs_builder = obs_builder

        if self._reward_fn is None:
            from rlgym.utils.reward_functions import ShootBallReward
            self._reward_fn = ShootBallReward()

        if obs_builder is None:
            from rlgym.utils.obs_builders import RhobotObs
            self._obs_builder = RhobotObs()

        if terminal_conditions is None:
            from rlgym.utils.terminal_conditions import common_conditions
            ep_len_minutes = 20 / 60
            ticks_per_sec = 120
            ticks_per_min = ticks_per_sec * 60
            max_ticks = int(round(ep_len_minutes * ticks_per_min / self._tick_skip))
            self._terminal_conditions = [common_conditions.TimeoutCondition(max_ticks),
                                         common_conditions.GoalScoredCondition()]

        elif type(terminal_conditions) not in (tuple, list):
            self._terminal_conditions = [terminal_conditions, ]

        self.agents = self._team_size * 2 if self._self_play else self._team_size
        self.observation_space = gym.spaces.Box(-np.inf, np.inf, shape=(self._obs_builder.obs_size,))
        self.action_space = gym.spaces.Box(-1, 1, shape=(8,))

        self._prev_actions = np.zeros((self.agents, self.action_space.shape[0]), dtype=float)

        self._spectator_ids = [i + 1 for i in range(self._team_size)]
        if self._self_play:
            for i in range(self._team_size):
                self._spectator_ids.append(5 + i)

        self.last_touch = None

    def episode_reset(self, initial_state):
        self._prev_actions.fill(0)
        for condition in self._terminal_conditions:
            condition.reset(initial_state)
        self._reward_fn.reset(initial_state)
        self._obs_builder.reset(initial_state)
        self.last_touch = None

    def build_observations(self, state) -> List:
        observations = []

        for i in range(len(state.players)):
            player = state.players[i]

            if not self._self_play and player.team_num == common_values.ORANGE_TEAM:
                continue
            else:
                obs = self._obs_builder.build_obs_for_player(player, state, self._prev_actions[i])

            observations.append(obs)

        if state.last_touch is None:
            state.last_touch = self.last_touch
        else:
            self.last_touch = state.last_touch
        return observations

    def get_rewards(self, state) -> List:
        rewards = []
        for player in state.players:
            if player.team_num == common_values.ORANGE_TEAM and not self._self_play:
                continue

            done = False
            for condition in self._terminal_conditions:
                if condition.look_ahead(state):
                    done = True
                    break

            if done:
                reward = self._reward_fn.get_final_reward(player, state)
            else:
                reward = self._reward_fn.get_reward(player, state)

            rewards.append(reward)
        return rewards

    def is_done(self, state):
        for condition in self._terminal_conditions:
            if condition.is_terminal(state):
                return True
        return False

    def parse_state(self, state_str: str) -> GameState:
        state = GameState(state_str)
        return state

    def format_actions(self, actions: Union[np.ndarray, List[np.ndarray], List[float]]):
        if type(actions) != np.ndarray:
            actions = np.asarray(actions)

        n = len(actions)
        if n != self.agents:
            actions = actions.reshape((1, n))

        self._prev_actions[:] = actions[:]

        action_str = None
        for i in range(len(actions)):
            act_arr = [str(self._spectator_ids[i])]
            for x in actions[i]:
                act_arr.append(str(x))
            act_str = ' '.join(act_arr)

            if action_str is None:
                action_str = act_str
            else:
                action_str = "{} {}".format(action_str, act_str)

        return action_str

    def get_config(self):
        return '{} {} {} {} {} {}'.format(self._team_size,
                                          1 if self._self_play else 0,
                                          1 if self._spawn_opponents else 0,
                                          1 if self._random_resets else 0,
                                          self._tick_skip,
                                          self._game_speed
                                          )