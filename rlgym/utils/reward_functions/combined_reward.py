from typing import Any, Optional, Tuple, overload, Union

import numpy as np
from rlgym.utils.reward_functions import RewardFunction
from rlgym.utils.gamestates import GameState, PlayerData


class CombinedReward(RewardFunction):
    """
    A reward composed of multiple rewards.
    """

    def __init__(
            self,
            reward_functions: Tuple[RewardFunction, ...],
            reward_weights: Optional[Tuple[float, ...]] = None
    ):
        """
        Creates the combined reward using multiple rewards, and a potential set
        of weights for each reward.

        :param reward_functions: Each individual reward function.
        :param reward_weights: The weights for each reward.
        """
        super().__init__()

        self.reward_functions = reward_functions
        self.reward_weights = reward_weights or np.ones_like(reward_functions)

        if len(self.reward_functions) != len(self.reward_weights):
            raise ValueError(
                ("Reward functions list length ({0}) and reward weights " \
                 "length ({1}) must be equal").format(
                    len(self.reward_functions), len(self.reward_weights)
                )
            )

    @classmethod
    def from_zipped(cls, *rewards_and_weights: Union[RewardFunction, Tuple[RewardFunction, float]]) -> "CombinedReward":
        """
        Alternate constructor which takes any number of either rewards, or (reward, weight) tuples.

        :param rewards_and_weights: a sequence of RewardFunction or (RewardFunction, weight) tuples
        """
        rewards = []
        weights = []
        for value in rewards_and_weights:
            if isinstance(value, tuple):
                r, w = value
            else:
                r, w = value, 1.
            rewards.append(r)
            weights.append(w)
        return cls(tuple(rewards), tuple(weights))

    def reset(self, initial_state: GameState) -> None:
        """
        Resets underlying reward functions.

        :param initial_state: The initial state of the reset environment.
        """
        for func in self.reward_functions:
            func.reset(initial_state)

    def get_reward(
            self,
            player: PlayerData,
            state: GameState,
            previous_action: np.ndarray
    ) -> float:
        """
        Returns the reward for a player on the terminal state.

        :param player: Player to compute the reward for.
        :param state: The current state of the game.
        :param previous_action: The action taken at the previous environment step.

        :return: The combined rewards for the player on the state.
        """
        rewards = [
            func.get_reward(player, state, previous_action)
            for func in self.reward_functions
        ]

        return float(np.dot(self.reward_weights, rewards))

    def get_final_reward(
            self,
            player: PlayerData,
            state: GameState,
            previous_action: np.ndarray
    ) -> float:
        """
        Returns the reward for a player on the terminal state.

        :param player: Player to compute the reward for.
        :param state: The current state of the game.
        :param previous_action: The action taken at the previous environment step.

        :return: The combined rewards for the player on the state.
        """
        rewards = [
            func.get_final_reward(player, state, previous_action)
            for func in self.reward_functions
        ]

        return float(np.dot(self.reward_weights, rewards))
