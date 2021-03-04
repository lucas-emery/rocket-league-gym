import rlgym
import time

env = rlgym.make("Duel")
# agent = RandomAgent()
# print(env.action_space.shape, env.observation_space.shape)

while True:
    obs = env.reset()
    done = False
    steps = 0
    ep_reward = 0
    t0 = time.time()
    while not done:
        actions = env.action_space.sample()  # agent.act(obs)
        new_obs, reward, done, state = env.step(actions)
        ep_reward += reward[0]
        obs = new_obs
        steps += 1

    length = time.time() - t0
    print("Step time: {:1.8f} | Episode time: {} | Episode Reward: {}".format(length / steps, length, ep_reward))