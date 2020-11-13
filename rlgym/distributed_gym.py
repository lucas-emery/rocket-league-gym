import win32api
import win32event
import win32file
import win32pipe
import winerror
import pywintypes
from enum import Enum
import numpy as np
import sys


class State(Enum):
    IDLE = 0
    CONNECTING = 1
    SETTING_UP = 2
    RECEIVING = 3
    SENDING = 4
    AWAITING_ACTION = 5
    DIED = 6


class DistributedGym:
    def __init__(self, matches: list, wait_count=sys.maxsize, wait_ratio=1.0):
        self._matches = matches
        self._next_match = 0
        self.wait_count = wait_count
        self.wait_ratio = wait_ratio

        self._PIPE_SIZE = 4096
        self._PIPE_NAME = r'\\.\pipe\RLGym'

        self.events = []
        self.runners = []
        self.runners_by_id = {}
        self.next_id = 0

        self.notify_reset = []
        self.ids = []
        self.obs = []
        self.rewards = []
        self.t_ids = []
        self.t_obs = []
        self.t_rewards = []

        # All envs must have the same dimensions
        first_env = matches[0]
        self.observation_space = first_env.observation_space
        self.action_space = first_env.action_space

        self.idle_runners = 0
        self.waiting_runners = 0
        self._create_runner()

    def _create_runner(self):
        env = self._get_next_env()
        if env.observation_space != self.observation_space:
            raise RuntimeError('Invalid env obs space. Expected:', self.observation_space, 'Got:', env.observation_space)
        if env.action_space != self.action_space:
            raise RuntimeError('Invalid env action space. Expected:', self.action_space, 'Got:', env.action_space)

        print("Building win32 pipe...")
        event = win32event.CreateEvent(None, True, True, None)
        pipe = win32pipe.CreateNamedPipe(self._PIPE_NAME, win32pipe.PIPE_ACCESS_DUPLEX | win32file.FILE_FLAG_OVERLAPPED,
                                         win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                                         win32pipe.PIPE_UNLIMITED_INSTANCES, self._PIPE_SIZE, self._PIPE_SIZE, 0, None)
        overlap = pywintypes.OVERLAPPED()
        overlap.hEvent = event
        r_id = self._get_new_id()
        print("Pipe built, initializing runner...")
        runner = Runner(r_id, env, pipe, overlap, self._PIPE_SIZE)

        self.events.append(event)
        self.runners.append(runner)
        self.runners_by_id[r_id] = runner
        self.idle_runners += 1

    def _get_next_env(self):
        env_name = self._envs[self._next_env]
        self._next_env += 1
        if self._next_env == len(self._envs):
            self._next_env = 0
        return self._get_env(env_name)

    def _get_new_id(self):
        r_id = self.next_id
        self.next_id += 1
        return r_id

    def reset(self):
        print("Resetting distributed environment...")
        # Notify reset to env objects
        for r_id in self.notify_reset:
            self.runners_by_id[r_id].env.episode_reset()
        self.notify_reset.clear()
        # Wait for N observations
        ids, obs, rewards, done = self._get_next_batch(is_reset=True)
        assert not done
        return ids, obs, rewards

    def step(self, ids, actions):
        # Add actions to runners
        for i in range(len(ids)):
            r_id, agent = ids[i]
            action = actions[i]
            runner = self.runners_by_id[r_id]
            if runner:
                runner.add_action(agent, action)

        # Send actions of ready runners
        for r in self.runners:
            if r.send_actions():
                self.waiting_runners -= 1

        # Get N obs if not terminal, only t_obs otherwise
        ids, obs, rewards, done = self._get_next_batch()

        return ids, obs, rewards, done

    def close(self):
        for runner in self.runners:
            runner.close()
        for event in self.events:
            win32file.CloseHandle(event)

    def _get_next_batch(self, is_reset=False):
        # If done send only terminal obs and get next full batch on "reset"
        while self.waiting_runners < min(self.wait_count, len(self.runners) - self.idle_runners) \
                or self.waiting_runners < int(self.wait_ratio * (len(self.runners) - self.idle_runners)) \
                or len(self.runners) - self.idle_runners == 0:
            # Wait for signal
            code = win32event.WaitForMultipleObjects(self.events, False, win32event.INFINITE)
            index = code - win32event.WAIT_OBJECT_0

            # Check index out of bounds? Server crashed anyways
            runner = self.runners[index]
            if runner.pending_op:
                try:
                    result = win32file.GetOverlappedResult(runner.pipe, runner.overlap, 0)

                    if runner.state == State.CONNECTING:
                        # if result == 0: # GetOverlappedResult throws an exception in python
                        #     raise RuntimeError('Connection failed', win32api.GetLastError())
                        runner.state = State.SETTING_UP
                    elif runner.state == State.SENDING:
                        if result == 0:
                            runner.state = State.DIED
                        else:
                            runner.state = State.RECEIVING
                    elif runner.state == State.RECEIVING:
                        if result == 0:
                            runner.state = State.DIED
                        else:
                            runner.b_read = result
                            runner.state = State.SENDING
                    else:
                        print('Invalid runner state', runner.state, runner.pending_op)
                        runner.state = State.DIED
                except:
                    print('GetOverlappedResult failed. Error code:', win32api.GetLastError(), 'Resetting runner', runner.id)
                    runner.state = State.DIED

                runner.pending_op = False

            if runner.state == State.SETTING_UP:
                # Send setup, state changes internally to sending
                print('Setting up runner ', runner.id)
                runner.setup()
                self.idle_runners -= 1
                if self.idle_runners == 0:
                    self._create_runner()
            elif runner.state == State.SENDING:
                # get state from buffer and build obs
                obs, rewards, terminal = runner.get_obs()
                # if terminal then read first state else wait action
                if terminal:
                    self.t_ids.extend([(runner.id, agent) for agent in range(len(obs))])
                    self.t_obs.extend(obs)
                    self.t_rewards.extend(rewards)
                    self.notify_reset.append(runner.id)
                    runner.state = State.RECEIVING
                else:
                    self.ids.extend([(runner.id, agent) for agent in range(len(obs))])
                    self.obs.extend(obs)
                    self.rewards.extend(rewards)
                    # can't send action instantly, have to wait for action to be ready.
                    runner.state = State.AWAITING_ACTION
                    self.waiting_runners += 1
                    # unset event manually?
                    win32event.ResetEvent(self.events[index])
            elif runner.state == State.RECEIVING:
                # queue read operation on pipe. All contained in receive_state method
                runner.receive_state()
            elif runner.state == State.DIED:
                print('Runner', runner.id, 'died.')
                self.idle_runners += 1
                if runner.id in self.notify_reset:
                    self.notify_reset.remove(runner.id)
                new_id = self._get_new_id()
                self.runners_by_id[runner.id] = None
                self.runners_by_id[new_id] = runner
                runner.reset(new_id)
            else:
                print('Invalid runner state', runner.state, runner.pending_op)
                runner.state = State.DIED

        if not is_reset and len(self.notify_reset) > 0:
            terminal = True
            ids = self.t_ids
            obs = self.t_obs
            rewards = self.t_rewards
            self.t_ids = []
            self.t_obs = []
            self.t_rewards = []
        else:
            terminal = False
            ids = self.ids
            obs = self.obs
            rewards = self.rewards
            self.ids = []
            self.obs = []
            self.rewards = []

        return ids, obs, rewards, terminal


class Runner:
    def __init__(self, r_id, env, pipe, overlap, buffer_size):
        self.id = r_id
        self.env = env
        self.pipe = pipe
        self.overlap = overlap
        self.state = State.IDLE
        self.pending_op = False
        self.b_read = 0
        self.r_buffer = win32file.AllocateReadBuffer(buffer_size)
        self.w_buffer = None
        self.action_count = 0
        self.actions = np.empty((env.agents, env.action_space), dtype=float)

        self.connect()

    def connect(self):
        print("Connecting pipe to DLL...")
        code = win32pipe.ConnectNamedPipe(self.pipe, self.overlap)
        if code == winerror.ERROR_IO_PENDING:
            self.state = State.CONNECTING
            self.pending_op = True
            print("Unable to connect...")
        else:
            self.state = State.SETTING_UP
            # is this necessary? It was like this on msoft's docs
            win32event.SetEvent(self.overlap.hEvent)
            print("Pipe connected!")

    def setup(self):
        self.w_buffer = str.encode(self.env.get_config())
        self._send_data()

    def _send_data(self):
        try:
            code, _ = win32file.WriteFile(self.pipe, self.w_buffer, self.overlap)
            # signal set automatically after write?
            if code == 0:
                self.state = State.RECEIVING
            else:
                self.state = State.SENDING
                self.pending_op = True
        except:
            print('WriteFile failed. Error code:', win32api.GetLastError(), 'Resetting runner', self.id)
            self.state = State.DIED
            win32event.SetEvent(self.overlap.hEvent)

    def receive_state(self):
        try:
            print("Receiving state...")
            code, _ = win32file.ReadFile(self.pipe, self.r_buffer, self.overlap)
            # signaled if read returns instantly?
            # if code == 0: Pywin expects you to get readable bytes from GetOverlappedResult
            #     self.state = State.SENDING
            if code == 0 or code == winerror.ERROR_IO_PENDING:
                self.state = State.RECEIVING
                self.pending_op = True
                print("State received!")
            else:
                print('ReadFile failed. Error code:', win32api.GetLastError(), 'Resetting runner', self.id)
                self.state = State.DIED
                win32event.SetEvent(self.overlap.hEvent)
        except:
            print('ReadFile failed. Error code:', win32api.GetLastError(), 'Resetting runner', self.id)
            self.state = State.DIED
            win32event.SetEvent(self.overlap.hEvent)

    def get_obs(self):
        state = self.env.parse_state(bytes(self.r_buffer[:self.b_read]).decode())
        obs = self.env.build_observations(state)
        rewards = self.env.get_rewards(state)
        done = self.env.is_done(state)
        return obs, rewards, done

    def add_action(self, agent, action):
        self.actions[agent] = action
        self.action_count += 1

    def send_actions(self):
        if self.state == State.AWAITING_ACTION and self.action_count == self.env.agents:
            self.w_buffer = str.encode(self.env.format_actions(self.actions))
            self._clear_actions()
            self._send_data()
            return True
        return False

    def _clear_actions(self):
        self.action_count = 0

    def reset(self, new_id):
        win32pipe.DisconnectNamedPipe(self.pipe)
        self.id = new_id
        self._clear_actions()
        self.connect()

    def close(self):
        win32file.CloseHandle(self.pipe)