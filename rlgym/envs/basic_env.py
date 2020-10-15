from rlgym.envs.environment import Environment


class BasicEnv(Environment):
    def __init__(self):
        super().__init__()
        self.observation_space = 41
        self.action_space = 8
        self.agents = 1
        self.team_size = 1
        self.self_play = False

    def get_config(self):
        return '%d %d'.format(self.team_size, 1 if self.self_play else 0)

    def episode_reset(self):
        pass

    def build_observations(self, state):
        return [state[2:]]

    def get_rewards(self, next_state):
        return [next_state[1]]

    def is_done(self, state):
        return bool(state[0])

    def parse_state(self, state_string):
        return [float(x) for x in state_string.split()]

    def format_actions(self, actions):
        return ' '.join([str(x) for x in actions[0]])
