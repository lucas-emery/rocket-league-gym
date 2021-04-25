import rlgym
import time
from stable_baselines3 import PPO
from rlgym.utils.reward_functions import distance_to_ball
from rlgym.utils.reward_functions import distance_to_ball2
from rlgym.utils.reward_functions import ShootBallReward
from rlgym.utils.obs_builders import MyObs
from stable_baselines3.common.callbacks import CheckpointCallback


MAX_TIMESTEPS = 60000

env = rlgym.make('Default', obs_builder=MyObs(), reward_fn=distance_to_ball2(), ep_len_minutes=25/60, random_resets=False)
#checkpoints might not work, we will see in morning
#checkpoint_callback = CheckpointCallback(save_freq=40000, save_path='./agents/touchball_agent3_v5/checkpoints/',
#                                         name_prefix='rl_model')

model = PPO('MlpPolicy', env=env, gamma=.99, learning_rate=.001, tensorboard_log="./touchball3_tensorboard/", verbose=1)
model.learn(total_timesteps=MAX_TIMESTEPS)
model.save('./agents/velocity/agents/v_agent_1')
#

for i in range(2,8):
    prev_agent = './agents/velocity/agents/v_agent_' + str(i-1)
    model = PPO.load(prev_agent, env=env, tensorboard_log="./agents/velocity/tensorboards/firstround/", learning_rate=.001, gamma= .99)
    model.learn(total_timesteps=MAX_TIMESTEPS)
    print('done learning')
    new_agent_string = './agents/velocity/agents/v_agent_' + str(i)
    model.save(new_agent_string)

# checkpoint_callback = CheckpointCallback(save_freq=40000, save_path='./agents/touchball_agent3_v6/checkpoints/',
#                                          name_prefix='rl_model')

print('Finished rendering')