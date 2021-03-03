from rlgym.communication import CommunicationHandler, Message
import subprocess
import winreg
import os
import numpy as np
from rlgym.utils import BotRecorder
from rlgym.gamelaunch import launch_rocket_league

class Gym:
    def __init__(self, match, pipe_id=0, path_to_rl=None, use_injector=False):
        self._match = match
        self.observation_space = match.observation_space
        self.action_space = match.action_space

        self._path_to_rl = path_to_rl
        self._use_injector = use_injector

        self._comm_handler = CommunicationHandler()
        self._local_pipe_name = self._comm_handler.format_pipe_id(pipe_id)
        self._local_pipe_id = pipe_id

        self._game_process = None

        self._open_game()
        self._setup_plugin_connection()

        self._recorder = BotRecorder(self._comm_handler)
        self._prev_state = None

    def _open_game(self):
        # Game process is only set if launched with path_to_rl
        self._game_process = launch_rocket_league(self._local_pipe_name, self._path_to_rl, self._local_pipe_name)

    def _setup_plugin_connection(self):
        self._comm_handler.open_pipe(self._local_pipe_name)
        self._comm_handler.send_message(header=Message.RLGYM_CONFIG_MESSAGE_HEADER, body=self._match.get_config())

    def reset(self):
        exception = self._comm_handler.send_message(header=Message.RLGYM_RESET_GAME_STATE_MESSAGE_HEADER, body=Message.RLGYM_NULL_MESSAGE_BODY)
        if exception is not None:
            self._attempt_recovery()
            exception = self._comm_handler.send_message(header=Message.RLGYM_RESET_GAME_STATE_MESSAGE_HEADER,
                                                        body=Message.RLGYM_NULL_MESSAGE_BODY)
            if exception is not None:
                import sys
                print("!UNABLE TO RECOVER ROCKET LEAGUE!\nEXITING")
                sys.exit(-1)

        # print("Sending reset command")
        self._match.episode_reset()
        state = self._receive_state()
        self._prev_state = state

        #self.recorder.reset()

        return self._match.build_observations(state)

    def step(self, actions):
        # print("Stepping")
        #self._parse_tanh_actions(actions)
        actions_sent = self._send_actions(actions)
        # print("Requesting state")

        received_state = self._receive_state()
        if received_state is None:  # TODO ask matt why?
            state = self._prev_state
        else:
            state = received_state

        #self.recorder.step(state)
        # print("Building obs")
        obs = self._match.build_observations(state)
        # print("Getting rewards")
        reward = self._match.get_rewards(state)
        # print("Checking done")
        done = self._match.is_done(state) or received_state is None or not actions_sent
        self._prev_state = state

        return obs, reward, done, state

    def close(self):
        self._comm_handler.close_pipe()
        if self._game_process is not None:
            self._game_process.terminate()

    def _receive_state(self):
        # print("Waiting for state...")
        message, exception = self._comm_handler.receive_message(header=Message.RLGYM_STATE_MESSAGE_HEADER)
        if exception is not None:
            self._attempt_recovery()
            return None

        if message is None:
            return None
        # print("GOT MESSAGE\n HEADER: {}\nBODY: {}\n".format(message.header, message.body))
        return self._match.parse_state(message.body)

    def _send_actions(self, actions):
        action_string = self._match.format_actions(actions)
        #print("Transmitting actions",action_string,"...")
        exception = self._comm_handler.send_message(header=Message.RLGYM_AGENT_ACTION_IMMEDIATE_RESPONSE_MESSAGE_HEADER, body=action_string)
        if exception is not None:
            self._attempt_recovery()
            return False
        return True
        # print("Message sent", action_string, "...")

    def seed(self, seed):
        #TODO: ensure that nothing actually needs to be seeded. I don't think any rng are used here, but need to make sure.
        pass

    def _parse_tanh_actions(self, actions):
        choices = [1, 0]

        prob = (1.0 + actions[-1]) / 2.0
        if prob is None or np.isnan(prob):
            prob = 0
        prob = min(max(prob, 0), 1)
        choice = np.random.choice(choices, p=[prob, 1 - prob])
        actions[-1] = choice

        prob = (1.0 + actions[-2]) / 2.0
        if prob is None or np.isnan(prob):
            prob = 0
        prob = min(max(prob, 0), 1)
        choice = np.random.choice(choices, p=[prob, 1 - prob])
        actions[-2] = choice

        prob = (1.0 + actions[-3]) / 2.0
        if prob is None or np.isnan(prob):
            prob = 0
        prob = min(max(prob, 0), 1)
        choice = np.random.choice(choices, p=[prob, 1 - prob])
        actions[-3] = choice

    def _attempt_recovery(self):
        print("!ROCKET LEAGUE HAS CRASHED!\nATTEMPTING RECOVERY")
        import os
        import time
        self.close()
        proc_list = os.popen('wmic process get description, processid').read()
        num_instances = proc_list.count("RocketLeague.exe")
        wait_time = 2 * num_instances

        print("Discovered {} existing Rocket League processes. Waiting {} seconds before attempting to open "
              "a new one.".format(num_instances, wait_time))

        time.sleep(wait_time)
        self._open_game()
        self._setup_plugin_connection()
