from rlgym.communication import CommunicationHandler, Message
from rlgym.utils import Math
import subprocess
import numpy as np

class Gym:
    def __init__(self, env, pipe_id=0):
        self._env = env
        self.observation_space = env.observation_space
        self.action_space = env.action_space

        self.comm_handler = CommunicationHandler()
        self.local_pipe_name = self.comm_handler.format_pipe_id(pipe_id)
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
                self.comm_handler.open_pipe()
                break
            except:
                time.sleep(1)

        self.comm_handler.send_message(header=Message.RLGYM_CONFIG_MESSAGE_HEADER, body=self.local_pipe_name)
        self.comm_handler.close_pipe()
        self.comm_handler.open_pipe(self.local_pipe_name)

        self.comm_handler.send_message(header=Message.RLGYM_CONFIG_MESSAGE_HEADER, body=self._env.get_config())

    def reset(self):
        self.comm_handler.send_message(header=Message.RLGYM_RESET_GAME_STATE_MESSAGE_HEADER, body=Message.RLGYM_NULL_MESSAGE_BODY)
        
        # print("Sending reset command")
        self._env.episode_reset()
        state = self._receive_state()

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
        done = self._env.is_done(state)

        return obs, reward, done, state

    def close(self):
        self.comm_handler.close_pipe()
        self.game_process.terminate()

    def _receive_state(self):
        # print("Waiting for state...")
        message = self.comm_handler.receive_message(header=Message.RLGYM_STATE_MESSAGE_HEADER)
        if message is None:
            return None
        # print("GOT MESSAGE\n HEADER: {}\nBODY: {}\n".format(message.header, message.body))
        return self._env.parse_state(message.body)

    def _send_actions(self, actions):
        action_string = self._env.format_actions(actions)
        # print("Transmitting actions",action_string,"...")
        self.comm_handler.send_message(header=Message.RLGYM_AGENT_ACTION_IMMEDIATE_RESPONSE_MESSAGE_HEADER, body=action_string)
        # print("Message sent", action_string, "...")

    def seed(self, seed):
        #TODO: ensure that nothing actually needs to be seeded. I don't think any rng are used here, but need to make sure.
        pass
