from rlgym.utils.reward_functions import RewardFunction


class SumRewards(RewardFunction):
    """
    For instance, rewarding touch and goal:
    SumRewards(TouchBallReward(), GoalReward())
    """

    def __init__(self, *reward_functions: RewardFunction, coefs=None):
        super().__init__()
        self.reward_funcs = reward_functions
        self.coefs = [1.] * len(reward_functions) if coefs is None else coefs

    def reset(self, *args):
        for rew_fn in self.reward_funcs:
            rew_fn.reset(*args)

    def get_reward(self, *args):
        return sum(c * rew_fn.get_reward(*args) for rew_fn, c in zip(self.reward_funcs, self.coefs))

    def get_final_reward(self, *args):
        return sum(c * rew_fn.get_final_reward(*args) for rew_fn, c in zip(self.reward_funcs, self.coefs))
