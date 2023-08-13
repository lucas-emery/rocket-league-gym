"""
    The Rocket League gym environment.
"""
from typing import Any, List, Dict, Tuple, Generic, Optional

from rlgym.api.config.action_parser import ActionParser
from rlgym.api.config.done_condition import DoneCondition
from rlgym.api.config.obs_builder import ObsBuilder
from rlgym.api.config.reward_function import RewardFunction
from rlgym.api.config.state_mutator import StateMutator
from rlgym.api.engine.renderer import Renderer
from rlgym.api.engine.transition_engine import TransitionEngine
from rlgym.api.typing import AgentID, ObsType, ActionType, EngineActionType, RewardType, StateType, SpaceType


class RLGym(Generic[AgentID, ObsType, ActionType, EngineActionType, RewardType, StateType, SpaceType]):
    #TODO docs

    def __init__(self,
                 state_mutator: StateMutator[StateType],
                 obs_builder: ObsBuilder[AgentID, ObsType, StateType, SpaceType],
                 action_parser: ActionParser[AgentID, ActionType, EngineActionType, SpaceType],
                 reward_fn: RewardFunction[AgentID, StateType, RewardType],
                 termination_cond: DoneCondition[AgentID, StateType],
                 truncation_cond: DoneCondition[AgentID, StateType],
                 transition_engine: TransitionEngine[AgentID, StateType, EngineActionType],
                 renderer: Optional[Renderer[StateType]]):
        self.state_mutator = state_mutator
        self.obs_builder = obs_builder
        self.action_parser = action_parser
        self.reward_fn = reward_fn
        self.termination_cond = termination_cond
        self.truncation_cond = truncation_cond
        self.transition_engine = transition_engine
        self.renderer = renderer
        self.shared_info = {}

    @property
    def agents(self) -> List[AgentID]:
        return self.transition_engine.agents

    @property
    def action_spaces(self) -> Dict[AgentID, SpaceType]:
        spaces = {}
        for agent in self.agents:
            spaces[agent] = self.action_space(agent)
        return spaces

    @property
    def observation_spaces(self) -> Dict[AgentID, SpaceType]:
        spaces = {}
        for agent in self.agents:
            spaces[agent] = self.observation_space(agent)
        return spaces

    @property
    def state(self) -> StateType:
        return self.transition_engine.state

    #TODO add snapshot property to all objects, save state and probably shared_info

    def action_space(self, agent: AgentID) -> SpaceType:
        return self.action_parser.get_action_space(agent)

    def observation_space(self, agent: AgentID) -> SpaceType:
        return self.obs_builder.get_obs_space(agent)

    def set_state(self, desired_state: StateType) -> Dict[AgentID, ObsType]:
        state = self.transition_engine.set_state(desired_state)

        return self.obs_builder.build_obs(self.agents, state, self.shared_info)

    def reset(self) -> Dict[AgentID, ObsType]:
        desired_state = self.transition_engine.create_base_state()
        self.state_mutator.apply(desired_state, self.shared_info)
        state = self.transition_engine.set_state(desired_state)

        self.obs_builder.reset(state, self.shared_info)
        self.action_parser.reset(state, self.shared_info)
        self.termination_cond.reset(state, self.shared_info)
        self.truncation_cond.reset(state, self.shared_info)
        self.reward_fn.reset(state, self.shared_info)

        return self.obs_builder.build_obs(self.agents, state, self.shared_info)

    def step(self, actions: Dict[AgentID, ActionType]) -> Tuple[Dict[AgentID, ObsType], Dict[AgentID, RewardType], Dict[AgentID, bool], Dict[AgentID, bool]]:
        engine_actions = self.action_parser.parse_actions(actions, self.state, self.shared_info)
        new_state = self.transition_engine.step(engine_actions)
        agents = self.agents
        obs = self.obs_builder.build_obs(agents, new_state, self.shared_info)
        is_terminated = self.termination_cond.is_done(agents, new_state, self.shared_info)
        is_truncated = self.truncation_cond.is_done(agents, new_state, self.shared_info)
        rewards = self.reward_fn.get_rewards(agents, new_state, is_terminated, is_truncated, self.shared_info)
        return obs, rewards, is_terminated, is_truncated

    def render(self) -> Any:
        self.renderer.render(self.state)

    def close(self) -> None:
        self.transition_engine.close()
        if self.renderer is not None:
            self.renderer.close()
