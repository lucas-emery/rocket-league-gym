from rlgym.envs.environment import Environment
import numpy as np


class Doubles(Environment):
    def __init__(self, self_play: bool):
        super().__init__()
        print("Initializing doubles env...")
        self.observation_space = 126
        self.action_space = 8
        self.team_size = 2
        self.self_play = self_play
        self.agents = self.team_size * 2 if self.self_play else self.team_size
        self._prev_actions = np.zeros((self.agents, 8), dtype=float)

    def get_config(self):
        return '{} {}'.format(self.team_size, 1 if self.self_play else 0)

    def episode_reset(self):
        self._prev_actions.fill(0)

    def build_observations(self, state):
        print("Building obs...")
        obs = []
        for i in range(self.agents):
            ob = np.zeros(self.observation_space)
            ob[0] = 1  # Game type
            ob[1:9] = self._prev_actions[i]
            if self.self_play:
                if i < self.team_size:
                    ob[9:18] = state[5:14]                  # ball
                    ob[18:33] = state[23+i*31:38+i*31]      # agent
                    ob[33:36] = state[51+i*31:54+i*31]      # agent
                    ob[36:51] = state[54-i*31:69-i*31]      # team
                    ob[51:54] = state[82-i*31:85-i*31]      # team
                    ob[72:87] = state[85:100]                # op1
                    # ob[87:90] = state[104:107]              # op1
                    # ob[90:105] = state[107:122]             # op2
                    ob[87:105] = state[113:131]
                    ob[105:108] = state[144:147]            # op2

                else:
                    j = i - self.team_size
                    ob[9:18] = state[14:23]                 # ball
                    ob[18:20] = state[85+j*31:87+j*31]      # agent
                    ob[20:36] = state[100+j*31:116+j*31]    # agent
                    ob[36:38] = state[116-j*31:118-j*31]    # team
                    ob[38:54] = state[131-j*31:147-j*31]    # team
                    ob[72:74] = state[23:25]                # op1
                    # ob[74:90] = state[29:45]                # op1
                    # ob[90:92] = state[45:47]                # op2
                    ob[74:92] = state[38:56]
                    ob[92:108] = state[69:85]               # op2
            else:
                ob[9:18] = state[3:12]                  # ball
                ob[18:36] = state[12+i*18:30+i*18]      # agent
                ob[36:54] = state[30-i*18:48-i*18]      # team
                # ob[72:90] = state[48:66]                # op1
                # ob[90:108] = state[66:84]               # op2
                ob[72:108] = state[48:84]

            obs.append(ob)
        return obs

    def get_rewards(self, next_state):
        return [next_state[1+i] for i in range(self.agents)]

    def is_done(self, state):
        return bool(state[0])

    def parse_state(self, state_string):
        return np.array([float(x) for x in state_string.split()])

    def format_actions(self, actions):
        self._prev_actions[:] = actions[:]
        return ' '.join([str(x) for x in actions.reshape(-1)])