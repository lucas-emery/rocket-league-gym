from rlgym.envs.environment import Environment
import numpy as np


class Standard(Environment):
    def __init__(self, self_play: bool):
        super().__init__()
        self.observation_space = 126
        self.action_space = 8
        self.team_size = 3
        self.self_play = self_play
        self.agents = self.team_size * 2 if self.self_play else self.team_size
        self._prev_actions = np.zeros((self.agents, 8), dtype=float)

    def get_config(self):
        return '{} {}'.format(self.team_size, 1 if self.self_play else 0)

    def episode_reset(self):
        self._prev_actions.fill(0)

    def build_observations(self, state):
        obs = []
        for i in range(self.agents):
            ob = np.zeros(self.observation_space)
            ob[0] = 2  # Game type
            ob[1:9] = self._prev_actions[i]
            if self.self_play:
                if i < self.team_size:
                    t1 = 1 if i == 0 else 0
                    t2 = 1 if i == 2 else 2
                    ob[9:18] = state[7:16]                  # ball
                    ob[18:33] = state[25+i*31:40+i*31]      # agent
                    ob[33:36] = state[53+i*31:56+i*31]      # agent
                    ob[36:51] = state[25+t1*31:40+t1*31]    # team1
                    ob[51:54] = state[53+t1*31:56+t1*31]    # team1
                    ob[54:69] = state[25+t2*31:40+t2*31]    # team2
                    ob[69:72] = state[53+t2*31:56+t2*31]    # team2
                    ob[72:87] = state[118:133]              # op1
                    # ob[87:90] = state[137:140]              # op1
                    # ob[90:105] = state[140:155]             # op2
                    ob[87:105] = state[146:164]
                    # ob[105:108] = state[168:171]            # op2
                    # ob[108:123] = state[171:186]            # op3
                    ob[105:123] = state[177:195]
                    ob[123:126] = state[208:211]            # op3

                else:
                    j = i - self.team_size
                    t1 = 1 if j == 0 else 0
                    t2 = 1 if j == 2 else 2
                    ob[9:18] = state[16:25]                  # ball
                    ob[18:20] = state[118+j*31:120+j*31]    # agent
                    ob[20:36] = state[133+j*31:149+j*31]    # agent
                    ob[36:38] = state[118+t1*31:120+t1*31]  # team1
                    ob[38:54] = state[133+t1*31:149+t1*31]  # team1
                    ob[54:56] = state[118+t2*31:120+t2*31]  # team2
                    ob[56:72] = state[133+t2*31:149+t2*31]  # team2
                    ob[72:74] = state[25:27]                # op1
                    # ob[74:90] = state[31:47]                # op1
                    # ob[90:92] = state[47:49]                # op2
                    ob[74:92] = state[40:58]
                    # ob[92:108] = state[62:78]               # op2
                    # ob[108:110] = state[78:80]              # op3
                    ob[92:110] = state[71:89]
                    ob[110:136] = state[102:118]             # op3
            else:
                t1 = 1 if i == 0 else 0
                t2 = 1 if i == 2 else 2
                ob[9:18] = state[4:13]                  # ball
                ob[18:36] = state[13+i*18:31+i*18]      # agent
                ob[36:54] = state[31+t1*18:49+t1*18]    # team1
                ob[54:72] = state[49+t2*18:67+t2*18]    # team2
                # ob[72:90] = state[67:85]                # op1
                # ob[90:108] = state[85:103]              # op2
                # ob[108:126] = state[103:121]            # op3
                ob[72:126] = state[67:121]

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