import numpy as np
from pettingzoo import AECEnv

from rlgym.gym import Gym


class PettingZooWrapper(AECEnv):
    """
    Wrapper for using the RLGym env with PettingZoo,
    """

    def __init__(self, env: Gym):
        """
        :param env: the environment to wrap.
        """
        super().__init__()
        self.env = env
        self.metadata = env.metadata
        self.agents = list(range(self.env._match.agents))
        self.possible_agents = self.agents.copy()

        self.observation_spaces = {agent: self.env.observation_space for agent in self.agents}
        self.action_spaces = {agent: self.env.action_space for agent in self.agents}

        self._reset_values()

    def _reset_values(self):
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.dones = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.state = {agent: None for agent in self.agents}
        self.observations = {agent: None for agent in self.agents}
        self.actions = {}  # For storing until we have enough actions to do an in-game step

        # Somewhat redundant, but would support any type of agent
        self._current_agent_index = 0
        self.agent_selection = self.agents[0]

    def reset(self):
        self._reset_values()

        observations = self.env.reset()
        self.observations = dict(zip(self.agents, observations))
        return self.observations

    def step(self, action):
        agent = self.agent_selection

        self.actions[agent] = action

        if self.agent_selection == self.agents[-1]:  # Only apply once everyone has registered
            action_array = np.stack([self.actions[agent] for agent in self.agents])
            observations, rewards, done, info = self.env.step(action_array)
            assert len(observations) == len(rewards) == self.num_agents
            self.observations = dict(zip(self.agents, observations))
            self.rewards = dict(zip(self.agents, rewards))
            self.dones = {agent: done for agent in self.agents}
            self.infos = {agent: info for agent in self.agents}
        self._current_agent_index = (self.agent_selection + 1) % self.num_agents
        self.agent_selection = self.agents[self._current_agent_index]

    def observe(self, agent):
        return self.observations[agent]

    def render(self, mode='human'):
        self.env.render(mode)

    def state(self):
        raise NotImplementedError

    def seed(self, seed=None):
        self.env.seed(seed)

    def close(self):
        self.env.close()


def parallel_pettingzoo_env(env: Gym):
    # Preliminary solution for making a ParallelEnv
    import supersuit as ss
    return ss.to_parallel(PettingZooWrapper(env))
