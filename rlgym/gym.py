"""
    The Rocket League gym environment.
"""
from threading import Thread
from time import sleep
from typing import List, Union, Tuple, Dict, Any

import numpy as np
from gym import Env

from rlgym.communication import CommunicationHandler, Message
from rlgym.gamelaunch import launch_rocket_league, run_injector, page_rocket_league, LaunchPreference
from rlgym.gamelaunch.minimize import toggle_rl_process


class Gym(Env):
    def __init__(self, match, pipe_id=0, launch_preference=LaunchPreference.EPIC, use_injector=False,
                 force_paging=False, raise_on_crash=False, auto_minimize=False):
        super().__init__()

        self._match = match
        self.observation_space = match.observation_space
        self.action_space = match.action_space

        self._launch_preference = launch_preference
        self._use_injector = use_injector
        self._force_paging = force_paging

        self._raise_on_crash = raise_on_crash

        self._comm_handler = CommunicationHandler()
        self._local_pipe_name = CommunicationHandler.format_pipe_id(pipe_id)
        self._local_pipe_id = pipe_id

        self._game_process = None

        self._open_game()
        self._setup_plugin_connection()

        if self._force_paging:
            self._page_client()

        self._minimizing_thread = None
        self._minimized = False
        self._auto_minimize = auto_minimize

        self._prev_state = None

    def _open_game(self):
        print("Launching Rocket League, make sure bakkesmod is running.")
        # Game process is only set if epic version is used or launched with path_to_rl
        self._game_process = launch_rocket_league(self._local_pipe_name, self._launch_preference)

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
            print("Forcing Rocket League to page unused memory. PID:", self._game_process.pid)
            return page_rocket_league(rl_pid=self._game_process.pid)

    def _minimize_game(self):
        if not self._minimized:
            if self._minimizing_thread is None:
                # Needs to be run in a separate thread because the window can't be minimized while unresponsive,
                # which calling the toggle_rl_process function directly, or joining too early, will cause
                self._minimizing_thread = Thread(target=toggle_rl_process, args=(self._game_process.pid,))
                self._minimizing_thread.start()
            elif self._minimizing_thread is not None and not self._minimizing_thread.is_alive():
                self._minimizing_thread.join()
                self._minimizing_thread = None
                self._minimized = True

    def reset(self, return_info=False) -> Union[List, Tuple]:
        """
        The environment reset function. When called, this will reset the state of the environment and objects in the game.
        This should be called once when the environment is initialized, then every time the `done` flag from the `step()`
        function is `True`.
        """

        state_str = self._match.get_reset_state()

        exception = self._comm_handler.send_message(header=Message.RLGYM_RESET_GAME_STATE_MESSAGE_HEADER,
                                                    body=state_str)
        if exception is not None:
            self._handle_exception()
            exception = self._comm_handler.send_message(header=Message.RLGYM_RESET_GAME_STATE_MESSAGE_HEADER,
                                                        body=state_str)
            if exception is not None:
                import sys
                print("!UNABLE TO RECOVER ROCKET LEAGUE!\nEXITING")
                sys.exit(-1)

        state = self._receive_state()
        self._match.episode_reset(state)
        self._prev_state = state

        if self._auto_minimize:
            self._minimize_game()  # After a successful episode, try to minimize the game

        obs = self._match.build_observations(state)
        if return_info:
            info = {
                'state': state,
                'result': self._match.get_result(state)
            }
            return obs, info
        return obs

    def step(self, actions: Any) -> Tuple[List, List, bool, Dict]:
        """
        The step function will send the list of provided actions to the game, then advance the game forward by `tick_skip`
        physics ticks using that action. The game is then paused, and the current state is sent back to RLGym. This is
        decoded into a `GameState` object, which gets passed to the configuration objects to determine the rewards,
        next observation, and done signal.

        :param actions: An object containing actions, in the format specified by the `ActionParser`.
        :return: A tuple containing (obs, rewards, done, info)
        """

        actions = self._match.parse_actions(actions, self._prev_state)
        actions_sent = self._send_actions(actions)

        received_state = self._receive_state()

        # If, for any reason, the state is not successfully received, we do not want to just crash the API.
        # This will simply pretend that the state did not change and advance as though nothing went wrong.
        if received_state is None:
            print("FAILED TO RECEIEVE STATE! FALLING TO", self._prev_state)
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

    def update_settings(self, game_speed=None, gravity=None, boost_consumption=None):
        """
        Updates the specified RLGym instance settings

        :param game_speed: The speed the physics will run at, leave it at 100 unless your game can't run at over 240fps
        :param gravity:
        :param boost_consumption:
        """
        self._match.update_settings(game_speed=game_speed, gravity=gravity, boost_consumption=boost_consumption)
        self._comm_handler.send_message(header=Message.RLGYM_CONFIG_MESSAGE_HEADER, body=self._match.get_config())

    def _receive_state(self):
        # print("Waiting for state...")
        message, exception = self._comm_handler.receive_message(header=Message.RLGYM_STATE_MESSAGE_HEADER)
        if exception is not None:
            self._handle_exception()
            return None

        if message is None:
            return None
        # print("GOT MESSAGE\n HEADER: '{}'\nBODY: '{}'\n".format(message.header, message.body))
        if message.body is None:
            return None

        return self._match.parse_state(message.body)

    def _send_actions(self, actions):
        assert isinstance(actions, np.ndarray), "Invalid action type, action must be of type np.ndarray(n, 8)."
        assert len(actions.shape) == 2, "Invalid action shape, shape must be of the form (n, 8)."
        assert actions.shape[-1] == 8, "Invalid action shape, last dimension must be 8."

        actions_formatted = self._match.format_actions(actions)
        exception = self._comm_handler.send_message(header=Message.RLGYM_AGENT_ACTION_IMMEDIATE_RESPONSE_MESSAGE_HEADER,
                                                    body=actions_formatted)
        if exception is not None:
            self._handle_exception()
            return False
        return True

    def _handle_exception(self):
        if self._raise_on_crash:
            raise EnvironmentError("Rocket League has crashed")  # Add exception message?
        else:
            print("!ROCKET LEAGUE HAS CRASHED!\nATTEMPTING RECOVERY")
            self.attempt_recovery()

    def attempt_recovery(self):
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
        self._minimized = False
