import os
import numpy as np
from threading import Thread
from time import sleep

from .communication import CommunicationHandler, Message
from .launch import launch_rocket_league, LaunchPreference, run_injector, page_rocket_league, toggle_rl_process


class GameManager:

    def __init__(self, pipe_id=None, launch_preference=LaunchPreference.EPIC, game_speed=100,
                 use_injector=True, force_paging=False, raise_on_crash=False, auto_minimize=True):
        self.launch_preference = launch_preference
        self.game_speed = game_speed
        self.use_injector = use_injector
        self.force_paging = force_paging
        self.raise_on_crash = raise_on_crash
        self.auto_minimize = auto_minimize

        self.game_process = None
        self.comm_handler = CommunicationHandler()
        self.pipe_name = CommunicationHandler.format_pipe_id(pipe_id)
        self.minimized = False
        self._minimizing_thread = None

    def open_game(self):
        self.minimized = False
        # Game process is only set if epic version is used or launched with path_to_rl
        self.game_process = launch_rocket_league(self.pipe_name, self.launch_preference)

        if self.use_injector:
            sleep(3)
            run_injector()

        self._setup_plugin_connection(self.game_speed)

        if self.force_paging:
            self._page_client()

    def minimize_game(self):
        if self.auto_minimize and not self.minimized:
            if self._minimizing_thread is None:
                # Needs to be run in a separate thread because the window can't be minimized while unresponsive,
                # which calling the toggle_rl_process function directly, or joining too early, will cause
                self._minimizing_thread = Thread(target=toggle_rl_process, args=(self.game_process.pid,))
                self._minimizing_thread.start()
            elif self._minimizing_thread is not None and not self._minimizing_thread.is_alive():
                self._minimizing_thread.join()
                self._minimizing_thread = None
                self.minimized = True

    #TODO update
    def receive_state(self):
        # print("Waiting for state...")
        message, exception = self.comm_handler.receive_message(header=Message.RLGYM_STATE_MESSAGE_HEADER)
        if exception is not None or message is None or message.body is None:
            self._handle_exception()
            # TODO retry here instead of returning
            return None

        return self._match.parse_state(message.body)

    #TODO update
    def send_actions(self, actions):
        assert isinstance(actions, np.ndarray), "Invalid action type, action must be of type np.ndarray(n, 8)."
        assert len(actions.shape) == 2, "Invalid action shape, shape must be of the form (n, 8)."
        assert actions.shape[-1] == 8, "Invalid action shape, last dimension must be 8."

        actions_formatted = self._match.format_actions(actions)
        exception = self.comm_handler.send_message(header=Message.RLGYM_AGENT_ACTION_IMMEDIATE_RESPONSE_MESSAGE_HEADER,
                                                    body=actions_formatted)
        if exception is not None:
            self._handle_exception()
            # TODO retry here instead of returning
            return False
        return True

    def update_config(self, game_speed=None):
        """
        Updates the specified RLGym instance settings

        :param game_speed: The speed the physics will run at, leave it at 100 unless your game can't run at over 240fps
        """
        if game_speed is not None:
            self.game_speed = game_speed

        exception = self.comm_handler.send_message(header=Message.RLGYM_CONFIG_MESSAGE_HEADER, body=[self.game_speed])
        if exception is not None:
            self._handle_exception()

    def close(self):
        """
        Disconnect communication with the Bakkesmod plugin and close the game. This should only be called if you are finished
        with your current RLGym environment instance.
        """
        self.comm_handler.close_pipe()
        if self.game_process is not None:
            self.game_process.terminate()

    def _setup_plugin_connection(self, game_speed):
        self.comm_handler.open_pipe(self.pipe_name)
        exception = self.comm_handler.send_message(header=Message.RLGYM_CONFIG_MESSAGE_HEADER, body=[game_speed])
        if exception is not None:
            self.close()
            raise EnvironmentError("Plugin connection failed")

    def _page_client(self) -> bool:
        if self.game_process is None:
            print("Forced paging is only supported for the epic games version")
            return False
        else:
            print("Forcing Rocket League to page unused memory. PID:", self.game_process.pid)
            return page_rocket_league(rl_pid=self.game_process.pid)

    def _handle_exception(self):
        if self.raise_on_crash:
            raise EnvironmentError("Rocket League has crashed")
        else:
            print("!ROCKET LEAGUE HAS CRASHED!\nATTEMPTING RECOVERY")
            self.close()
            self._wait_for_recovery()
            self.open_game()

    def _wait_for_recovery(self):
        proc_list = os.popen('wmic process get description, processid').read()
        num_instances = proc_list.count("RocketLeague.exe")
        wait_time = 2 * num_instances

        print("Discovered {} existing Rocket League processes. Waiting {} seconds before attempting to open "
              "a new one.".format(num_instances, wait_time))

        sleep(wait_time)
