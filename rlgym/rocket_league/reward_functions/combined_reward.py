from typing import List, Dict, Any, Union, Iterable, Tuple

from rlgym.api.config.reward_function import RewardFunction
from rlgym.api.typing import AgentID
from rlgym.rocket_league.engine.game_state import GameState


class CombinedReward(RewardFunction[AgentID, GameState, float]):

    def __init__(self, rewards_and_weights: Union[Iterable[RewardFunction], Iterable[Tuple[RewardFunction, float]]]):
        reward_fns = []
        weights = []

        for value in rewards_and_weights:
            if isinstance(value, tuple):
                r, w = value
            else:
                r, w = value, 1.
            reward_fns.append(r)
            weights.append(w)

        self.reward_fns = tuple(reward_fns)
        self.weights = tuple(weights)

    def reset(self, initial_state: GameState, shared_info: Dict[str, Any]) -> None:
        for reward_fn in self.reward_fns:
            reward_fn.reset(initial_state, shared_info)

    def get_rewards(self, agents: List[AgentID], state: GameState, is_terminated: Dict[AgentID, bool],
                    is_truncated: Dict[AgentID, bool], shared_info: Dict[str, Any]) -> Dict[AgentID, float]:
        # FIXME optimize this double for loop with a numpy matrix
        combined_rewards = {agent: 0. for agent in agents}
        for reward_fn, weight in zip(self.reward_fns, self.weights):
            rewards = reward_fn.get_rewards(agents, state, is_terminated, is_truncated, shared_info)
            for agent in agents:
                combined_rewards[agent] += rewards[agent] * weight

        return combined_rewards
