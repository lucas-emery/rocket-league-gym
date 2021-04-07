from abc import abstractmethod


class Environment:
    def __init__(self):
        self.observation_space = None
        self.action_space = None
        self.agents = None
        self.bots = None
        self._team_size = None

    @abstractmethod
    def get_config(self):
        raise NotImplementedError

    @abstractmethod
    def episode_reset(self, initial_state):
        raise NotImplementedError

    @abstractmethod
    def build_observations(self, state):
        raise NotImplementedError

    @abstractmethod
    def get_rewards(self, next_state, done):
        raise NotImplementedError

    @abstractmethod
    def is_done(self, state):
        raise NotImplementedError

    @abstractmethod
    def parse_state(self, state_string):
        raise NotImplementedError

    @abstractmethod
    def format_actions(self, actions):
        raise NotImplementedError

