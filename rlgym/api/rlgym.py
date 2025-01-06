from typing import Any, List, Dict, Tuple, Generic, Optional
from .config import ActionParser, DoneCondition, ObsBuilder, RewardFunction, StateMutator, Renderer, TransitionEngine, \
    SharedInfoProvider
from .typing import AgentID, ObsType, ActionType, EngineActionType, RewardType, StateType, ObsSpaceType, ActionSpaceType


class RLGym(Generic[AgentID, ObsType, ActionType, EngineActionType, RewardType, StateType, ObsSpaceType, ActionSpaceType]):
    """
    The main RLGym class. This class is responsible for managing the environment and the interactions between
    the different components of the environment. It is the main interface for the user to interact with an environment.
    """

    def __init__(self,
                 state_mutator: StateMutator[StateType],
                 obs_builder: ObsBuilder[AgentID, ObsType, StateType, ObsSpaceType],
                 action_parser: ActionParser[AgentID, ActionType, EngineActionType, StateType, ActionSpaceType],
                 reward_fn: RewardFunction[AgentID, StateType, RewardType],
                 transition_engine: TransitionEngine[AgentID, StateType, EngineActionType],
                 termination_cond: Optional[DoneCondition[AgentID, StateType]] = None,
                 truncation_cond: Optional[DoneCondition[AgentID, StateType]] = None,
                 shared_info_provider: Optional[SharedInfoProvider[AgentID, StateType]] = None,
                 renderer: Optional[Renderer[StateType]] = None):
        """
        The main RLGym class. This class is responsible for managing the environment and the interactions between
        the different components of the environment. It is the main interface for the user to interact with an environment.

        :param state_mutator: The StateMutator used to modify the state of the environment.
        :param obs_builder: The ObsBuilder used to build observations for the agents.
        :param action_parser: The ActionParser used to parse actions from the agents into engine actions.
        :param reward_fn: The RewardFunction used to calculate rewards for the agents.
        :param transition_engine: The TransitionEngine used to transition the environment from one state to another.
        :param termination_cond: The DoneCondition used to determine if the episode is done.
        :param truncation_cond: The DoneCondition used to determine if the episode is truncated.
        :param shared_info_provider: The SharedInfoProvider used to provide shared information across all config objects.
        :param renderer: The Renderer used to render the environment.
        """
        self.state_mutator = state_mutator
        self.obs_builder = obs_builder
        self.action_parser = action_parser
        self.reward_fn = reward_fn
        self.transition_engine = transition_engine
        self.termination_cond = termination_cond
        self.truncation_cond = truncation_cond
        self.renderer = renderer
        self.shared_info_provider = shared_info_provider
        self.shared_info = shared_info_provider.create({}) if shared_info_provider is not None else {}

    @property
    def agents(self) -> List[AgentID]:
        return self.transition_engine.agents

    @property
    def action_spaces(self) -> Dict[AgentID, ActionSpaceType]:
        spaces = {}
        for agent in self.agents:
            spaces[agent] = self.action_space(agent)
        return spaces

    @property
    def observation_spaces(self) -> Dict[AgentID, ObsSpaceType]:
        spaces = {}
        for agent in self.agents:
            spaces[agent] = self.observation_space(agent)
        return spaces

    @property
    def state(self) -> StateType:
        return self.transition_engine.state

    # TODO add snapshot property to all objects, save state and probably shared_info

    def action_space(self, agent: AgentID) -> ActionSpaceType:
        return self.action_parser.get_action_space(agent)

    def observation_space(self, agent: AgentID) -> ObsSpaceType:
        return self.obs_builder.get_obs_space(agent)

    def set_state(self, desired_state: StateType) -> Dict[AgentID, ObsType]:
        if self.shared_info_provider is not None:
            self.shared_info = self.shared_info_provider.create(self.shared_info)
        state = self.transition_engine.set_state(desired_state, self.shared_info)
        agents = self.agents
        if self.shared_info_provider is not None:
            self.shared_info = self.shared_info_provider.set_state(agents, state, self.shared_info)
        return self.obs_builder.build_obs(agents, state, self.shared_info)

    def reset(self) -> Dict[AgentID, ObsType]:
        if self.shared_info_provider is not None:
            self.shared_info = self.shared_info_provider.create(self.shared_info)
        desired_state = self.transition_engine.create_base_state()
        self.state_mutator.apply(desired_state, self.shared_info)
        state = self.transition_engine.set_state(desired_state, self.shared_info)
        agents = self.agents
        if self.shared_info_provider is not None:
            self.shared_info = self.shared_info_provider.set_state(agents, state, self.shared_info)
        self.obs_builder.reset(agents, state, self.shared_info)
        self.action_parser.reset(agents, state, self.shared_info)
        if self.termination_cond is not None:
            self.termination_cond.reset(agents, state, self.shared_info)
        if self.truncation_cond is not None:
            self.truncation_cond.reset(agents, state, self.shared_info)
        self.reward_fn.reset(agents, state, self.shared_info)

        return self.obs_builder.build_obs(agents, state, self.shared_info)

    def step(self, actions: Dict[AgentID, ActionType]) \
            -> Tuple[Dict[AgentID, ObsType], Dict[AgentID, RewardType], Dict[AgentID, bool], Dict[AgentID, bool]]:
        engine_actions = self.action_parser.parse_actions(actions, self.state, self.shared_info)
        new_state = self.transition_engine.step(engine_actions, self.shared_info)
        agents = self.agents
        if self.shared_info_provider is not None:
            self.shared_info = self.shared_info_provider.step(agents, new_state, self.shared_info)
        obs = self.obs_builder.build_obs(agents, new_state, self.shared_info)
        is_terminated = self.termination_cond.is_done(agents, new_state, self.shared_info) \
            if self.termination_cond is not None else {agent: False for agent in agents}
        is_truncated = self.truncation_cond.is_done(agents, new_state, self.shared_info) \
            if self.truncation_cond is not None else {agent: False for agent in agents}
        rewards = self.reward_fn.get_rewards(agents, new_state, is_terminated, is_truncated, self.shared_info)
        return obs, rewards, is_terminated, is_truncated

    def render(self) -> Any:
        self.renderer.render(self.state, self.shared_info)

    def close(self) -> None:
        self.transition_engine.close()
        if self.renderer is not None:
            self.renderer.close()
