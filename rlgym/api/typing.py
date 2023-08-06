from typing import TypeVar

AgentID = TypeVar("AgentID", bound=str)
ObsType = TypeVar("ObsType")
ActionType = TypeVar("ActionType")
EngineActionType = TypeVar("EngineActionType")
RewardType = TypeVar("RewardType")
StateType = TypeVar("StateType")
SpaceType = TypeVar("SpaceType")
