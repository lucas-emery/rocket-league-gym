import rlgym
import time
from stable_baselines3 import PPO
from rlgym.utils.reward_functions import distance_to_ball
from rlgym.utils.reward_functions import distance_to_ball2
from rlgym.utils.reward_functions import ShootBallReward
from rlgym.utils.obs_builders import MyObs
from stable_baselines3.common.callbacks import CheckpointCallback


MAX_TIMESTEPS = 40000

env = rlgym.make('Default', obs_builder=MyObs(), reward_fn=distance_to_ball2(), ep_len_minutes=45/60, random_resets=False)
                                     name_prefix='rl_model')

print(49)
model = PPO.load(r"D:\randy\Documents\Rocket League\RLgym\Version 4 cloned repo\rocket-league-gym\agents\touchball agents\touchball_agent3_v5\agents\touch_ball_agent_v5_14.zip", env=env, learning_rate=.001, gamma= .99)
model.learn(total_timesteps=MAX_TIMESTEPS)

print(14)
model = PPO.load(r"D:\randy\Documents\Rocket League\RLgym\Version 4 cloned repo\rocket-league-gym\agents\touchball agents\touchball_agent3_v5\agents\touch_ball_agent_v5_49.zip", env=env, learning_rate=.001, gamma= .99)
model.learn(total_timesteps=MAX_TIMESTEPS)

# env = rlgym.make('Default')

# for i in range(10):
#     obs = env.reset()
#     done = False
#     steps = 0
#     ep_reward = 0
#     t0 = time.time()
#     while True:
#         actions, _states = model.predict(obs)  # agent.act(obs) | Your agent should go here
#         obs, reward, done, state = env.step(actions)
#         ep_reward += reward[0]
#         obs = new_obs
#         steps += 1
#         if done:
#             break

#     length = time.time() - t0
#     print("Step time: {:1.5f} | Episode time: {:.2f} | Episode Reward: {:.2f}".format(length / steps, length, ep_reward))
print('Finished rendering')