from rlgym.utils.reward_functions import RewardFunction
from rlgym.utils import math

class DefaultReward(RewardFunction):
    def __init__(self):
        super().__init__()
        self.last_touch = None

    def reset(self, initial_state):
        self.last_touch = initial_state.last_touch

    def get_reward(self, player, state, previous_action):
        return -math.vecmag(player.car_data.angular_velocity)

    def get_final_reward(self, player, state, previous_action):
        return self.get_reward(player, state, previous_action)