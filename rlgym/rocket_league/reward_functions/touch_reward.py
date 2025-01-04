from typing import List, Dict, Any

from rlgym.api import RewardFunction, AgentID
from rlgym.rocket_league.api import GameState


class TouchReward(RewardFunction[AgentID, GameState, float]):
    """
    A RewardFunction that gives a reward of 1 if the agent touches the ball, 0 otherwise.
    """

    def reset(self, agents: List[AgentID], initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        pass

    def get_rewards(self, agents: List[AgentID], state: GameState, is_terminated: Dict[AgentID, bool],
                    is_truncated: Dict[AgentID, bool], shared_info: Dict[str, Any]) -> Dict[AgentID, float]:
        return {agent: self._get_reward(agent, state) for agent in agents}

    def _get_reward(self, agent: AgentID, state: GameState) -> float:
        return 1. if state.cars[agent].ball_touches > 0 else 0.
