import rlgym
import time

env = rlgym.make()

while True:
    obs = env.reset()
    done = False
    steps = 0
    ep_reward = 0
    t0 = time.time()
    while not done:
        actions = env.action_space.sample()  # agent.act(obs) | Your agent should go here
        new_obs, reward, done, state = env.step(actions)
        ep_reward += reward
        obs = new_obs
        steps += 1

    length = time.time() - t0
    print("Step time: {:1.5f} | Episode time: {:.2f} | Episode Reward: {:.2f}".format(length / steps, length, ep_reward))