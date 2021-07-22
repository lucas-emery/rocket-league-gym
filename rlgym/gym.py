"""
    The Rocket League gym environment.
"""
from time import sleep
from typing import List, Union, Tuple, Dict

import numpy as np
from gym import Env

from rlgym.gamelaunch import launch_rocket_league, run_injector, page_rocket_league
from rlgym.communication import CommunicationHandler, Message


class Gym(Env):
    def __init__(self, match, pipe_id=0, path_to_rl=None, use_injector=False, force_paging=False):
        super().__init__()

        self._match = match
        self.observation_space = match.observation_space
        self.action_space = match.action_space

        self._path_to_rl = path_to_rl
        self._use_injector = use_injector
        self._force_paging = force_paging

        self._comm_handler = CommunicationHandler()
        self._local_pipe_name = self._comm_handler.format_pipe_id(pipe_id)
        self._local_pipe_id = pipe_id

        self._game_process = None

        self._open_game()
        self._setup_plugin_connection()

        if self._force_paging:
            self._page_client()

        self._prev_state = None

    def _open_game(self):
        print("Launching Rocket League, make sure bakkesmod is running.")
        # Game process is only set if epic version is used or launched with path_to_rl
        self._game_process = launch_rocket_league(self._local_pipe_name, self._path_to_rl)

        if self._use_injector:
            sleep(3)
            run_injector()

    def _setup_plugin_connection(self):
        self._comm_handler.open_pipe(self._local_pipe_name)
        self._comm_handler.send_message(header=Message.RLGYM_CONFIG_MESSAGE_HEADER, body=self._match.get_config())

    def _page_client(self) -> bool:
        if self._game_process is None:
            print("Forced paging is only supported for the epic games version")
            return False
        else:
            print("Forcing rocket league to page unused memory. PID:", self._game_process.pid)
            return page_rocket_league(rl_pid=self._game_process.pid)

    def reset(self) -> List:
        """
        The environment reset function. When called, this will reset the state of the environment and objects in the game.
        This should be called once when the environment is initialized, then every time the `done` flag from the `step()`
        function is `True`.
        """

        exception = self._comm_handler.send_message(header=Message.RLGYM_RESET_GAME_STATE_MESSAGE_HEADER, body=Message.RLGYM_NULL_MESSAGE_BODY)
        if exception is not None:
            self._attempt_recovery()
            exception = self._comm_handler.send_message(header=Message.RLGYM_RESET_GAME_STATE_MESSAGE_HEADER,
                                                        body=Message.RLGYM_NULL_MESSAGE_BODY)
            if exception is not None:
                import sys
                print("!UNABLE TO RECOVER ROCKET LEAGUE!\nEXITING")
                sys.exit(-1)

        state = self._receive_state()
        self._match.episode_reset(state)
        self._prev_state = state

        return self._match.build_observations(state)

    def step(self, actions: Union[np.ndarray, List[np.ndarray], List[float]]) -> Tuple[List, List, bool, Dict]:
        """
        The step function will send the list of provided actions to the game, then advance the game forward by `tick_skip`
        physics ticks using that action. The game is then paused, and the current state is sent back to RLGym. This is
        decoded into a `GameState` object, which gets passed to the configuration objects to determine the rewards,
        next observation, and done signal.

        :param actions: A tuple containing N lists of actions, where N is the number of agents interacting with the game.
        :return: A tuple containing (obs, rewards, done, info)
        """

        #TODO: This is a temporary solution to the action space problems in the current implementation.
        if isinstance(actions, np.ndarray):
            assert actions.shape[-1] == 8, "Invalid action shape, last dimension must be 8."
            actions[..., 5:] = actions[..., 5:] > 0
        elif len(actions) == 8:
            actions[5:] = [0 if x <= 0 else 1 for x in actions[5:]]
        actions_sent = self._send_actions(actions)

        received_state = self._receive_state()

        #If, for any reason, the state is not successfully received, we do not want to just crash the API.
        #This will simply pretend that the state did not change and advance as though nothing went wrong.
        if received_state is None:
            state = self._prev_state
        else:
            state = received_state

        obs = self._match.build_observations(state)
        done = self._match.is_done(state) or received_state is None or not actions_sent
        reward = self._match.get_rewards(state, done)
        self._prev_state = state

        info = {
            'state': state,
            'result': self._match.get_result(state)
        }

        return obs, reward, done, info

    def close(self):
        """
        Disconnect communication with the Bakkesmod plugin and close the game. This should only be called if you are finished
        with your current RLGym environment instance.
        """
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
        # print("GOT MESSAGE\n HEADER: '{}'\nBODY: '{}'\n".format(message.header, message.body))
        if message.body is None:
            return None

        return self._match.parse_state(message.body)

    def _send_actions(self, actions):
        action_string = self._match.format_actions(actions)
        exception = self._comm_handler.send_message(header=Message.RLGYM_AGENT_ACTION_IMMEDIATE_RESPONSE_MESSAGE_HEADER, body=action_string)
        if exception is not None:
            self._attempt_recovery()
            return False
        return True

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
        if self._force_paging:
            self._page_client()
