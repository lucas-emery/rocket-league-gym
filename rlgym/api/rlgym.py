"""
    The Rocket League gym environment.
"""
from typing import Any, List, Dict, Tuple, TypeVar, Generic

from rlgym.api.config.action_parser import ActionParser
from rlgym.api.config.done_condition import DoneCondition
from rlgym.api.config.obs_builder import ObsBuilder
from rlgym.api.config.reward_function import RewardFunction
from rlgym.api.config.state_setter import StateSetter
from rlgym.api.engine.renderer import Renderer
from rlgym.api.engine.transition_engine import TransitionEngine

AgentID = TypeVar("AgentID", bound=str)
ObsType = TypeVar("ObsType")
ActionType = TypeVar("ActionType")
EngineActionType = TypeVar("EngineActionType")
RewardType = TypeVar("RewardType")
StateType = TypeVar("StateType")
StateWrapperType = TypeVar("StateWrapperType")
SpaceType = TypeVar("SpaceType")


class RLGym(Generic[AgentID, ObsType, ActionType, EngineActionType, RewardType, StateType, StateWrapperType, SpaceType]):
    #TODO docs

    def __init__(self,
                 state_setter: StateSetter[StateType, StateWrapperType],
                 obs_builder: ObsBuilder[AgentID, ObsType, StateType, SpaceType],
                 action_parser: ActionParser[AgentID, ActionType, EngineActionType, SpaceType],
                 reward_fn: RewardFunction[AgentID, StateType, RewardType],
                 termination_cond: DoneCondition[AgentID, StateType],
                 truncation_cond: DoneCondition[AgentID, StateType],
                 transition_engine: TransitionEngine[AgentID, StateType, StateWrapperType, EngineActionType],
                 renderer: Renderer[StateType]):
        self.state_setter = state_setter
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

    def action_space(self, agent: AgentID) -> SpaceType:
        return self.action_parser.get_action_space(agent)

    def observation_space(self, agent: AgentID) -> SpaceType:
        return self.obs_builder.get_obs_space(agent)

    def reset(self) -> Dict[AgentID, ObsType]:
        state_wrapper = self.state_setter.build_wrapper(self.state, self.shared_info)
        self.state_setter.reset(state_wrapper, self.shared_info)
        state = self.transition_engine.set_state(state_wrapper)

        self.obs_builder.reset(state, self.shared_info)
        self.action_parser.reset(state, self.shared_info)
        self.reward_fn.reset(state, self.shared_info)
        self.termination_cond.reset(state, self.shared_info)
        self.truncation_cond.reset(state, self.shared_info)

        obs = self.obs_builder.build_obs(state, self.shared_info)
        return obs

    def step(self, actions: Dict[AgentID, ActionType]) -> Tuple[Dict[AgentID, ObsType], Dict[AgentID, RewardType], Dict[AgentID, bool], Dict[AgentID, bool]]:
        engine_actions = self.action_parser.parse_actions(actions, self.state, self.shared_info)
        new_state = self.transition_engine.step(engine_actions)
        obs = self.obs_builder.build_obs(new_state, self.shared_info)
        is_terminated = self.termination_cond.is_done(new_state, self.shared_info)
        is_truncated = self.truncation_cond.is_done(new_state, self.shared_info)
        rewards = self.reward_fn.get_rewards(new_state, is_terminated, is_truncated, self.shared_info)
        return obs, rewards, is_terminated, is_truncated

    def render(self) -> Any:
        self.renderer.render(self.state)

    def close(self) -> None:
        self.transition_engine.close()
