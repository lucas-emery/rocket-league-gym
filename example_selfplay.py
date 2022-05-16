import rlgym
import time

env = rlgym.make(spawn_opponents=True)

while True:
    obs = env.reset()
    obs_1 = obs[0]
    obs_2 = obs[1]
    done = False
    steps = 0
    ep_reward = 0
    t0 = time.time()
    while not done:
        actions_1 = env.action_space.sample()
        actions_2 = env.action_space.sample()
        actions = [actions_1, actions_2]
        new_obs, reward, done, state = env.step(actions)
        ep_reward += reward[0]
        obs_1 = new_obs[0]
        obs_2 = new_obs[1]
        steps += 1

    length = time.time() - t0
    print("Step time: {:1.5f} | Episode time: {:.2f} | Episode Reward: {:.2f}".format(length / steps, length, ep_reward))