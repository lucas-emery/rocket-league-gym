from rlgym.communication import CommunicationHandler, Message
from rlgym.utils import Math
import subprocess
import numpy as np

class Gym:
    def __init__(self, env, pipe_id=0):
        self._env = env
        self.observation_space = env.observation_space
        self.action_space = env.action_space

        self._tick_skip = 6
        self._ep_len_minutes = 1
        ticks_per_sec = 120
        ticks_per_min = ticks_per_sec * 60
        self._max_ticks = self._ep_len_minutes * ticks_per_min // self._tick_skip
        self._tick = 0
        self._random_resets = 1

        self.commHandler = CommunicationHandler()
        self.local_pipe_name = self.commHandler.format_pipe_id(pipe_id)
        self.local_pipe_id = pipe_id

        self.game_process = None

        self.open_game()
        self.setup_plugin_connection()

    def open_game(self):
        path_to_rl = "H:\\SteamLibrary\\steamapps\\common\\rocketleague\\Binaries\\Win64"
        full_command = "{}\\{}".format(path_to_rl, "RocketLeague.exe")
        self.game_process = subprocess.Popen(full_command)
        print("Executing injector...")
        full_command = "{}\\{}".format(path_to_rl, "RLMultiInjector.exe")
        subprocess.Popen(full_command)

    def setup_plugin_connection(self):
        import time
        #TODO: Come up with a better way to deal with multiple processes simultaneously attempting to open the global pipe.
        for i in range(120):
            try:
                self.commHandler.open_pipe()
                break
            except:
                time.sleep(1)

        self.commHandler.send_message(header=Message.RLGYM_CONFIG_MESSAGE_HEADER, body=self.local_pipe_name)
        self.commHandler.close_pipe()
        self.commHandler.open_pipe(self.local_pipe_name)

        #Build config for plugin match
        env_config = self._env.get_config()
        cfg = "{} {} {} {}".format(env_config, self._random_resets, self._max_ticks * self._tick_skip, self._tick_skip)

        self.commHandler.send_message(header=Message.RLGYM_CONFIG_MESSAGE_HEADER, body=cfg)

    def reset(self):
        self.commHandler.send_message(header=Message.RLGYM_RESET_GAME_STATE_MESSAGE_HEADER, body=Message.RLGYM_NULL_MESSAGE_BODY)
        
        # print("Sending reset command")
        self._env.episode_reset()
        state = self._receive_state()

        self._tick = 0
        return self._env.build_observations(state)

    def step(self, actions):
        # print("Stepping")
        self._send_actions(actions)
        # print("Requesting state")
        state = self._receive_state()
        # print("Building obs")
        obs = self._env.build_observations(state)
        # print("Getting rewards")
        reward = self._env.get_rewards(state)
        # print("Checking done")
        done = self._env.is_done(state) or self._tick >= self._max_ticks


        self._tick += 1
        return obs, reward, done, state

    def close(self):
        self.commHandler.close_pipe()
        self.game_process.terminate()

    def _receive_state(self):
        # print("Waiting for state...")
        message = self.commHandler.receive_message(header=Message.RLGYM_STATE_MESSAGE_HEADER)
        if message is None:
            return None
        # print("GOT MESSAGE\n HEADER: {}\nBODY: {}\n".format(message.header, message.body))
        return self._env.parse_state(message.body)

    def _send_actions(self, actions):
        action_string = self._env.format_actions(actions)
        # print("Transmitting actions",action_string,"...")
        self.commHandler.send_message(header=Message.RLGYM_AGENT_ACTION_IMMEDIATE_RESPONSE_MESSAGE_HEADER, body=action_string)
        # print("Message sent", action_string, "...")

    def seed(self, seed):
        #TODO: ensure that nothing actually needs to be seeded. I don't think any rng are used here, but need to make sure.
        pass
