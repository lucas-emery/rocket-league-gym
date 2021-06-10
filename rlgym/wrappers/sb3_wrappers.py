import os
import gym
import csv
import time
import json
import warnings
import numpy as np
import multiprocessing as mp
from typing import List, Optional, Tuple, Union, Sequence, Type, Any, Dict
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.vec_env.subproc_vec_env import _worker
from stable_baselines3.common.vec_env.base_vec_env import VecEnvIndices, CloudpickleWrapper, VecEnvWrapper
from stable_baselines3.common.vec_env.base_vec_env import VecEnv, VecEnvObs, VecEnvStepReturn
from rlgym.gym import Gym
from rlgym.envs import Match


class ResultsWriter:
    """
    A result writer that saves the data from the `Monitor` class, copied from SB3 version 1.1.0a7

    :param filename: the location to save a log file, can be None for no log
    :param header: the header dictionary object of the saved csv
    :param reset_keywords: the extra information to log, typically is composed of
        ``reset_keywords`` and ``info_keywords``
    """

    def __init__(
            self,
            filename: str = "",
            header: Dict[str, Union[float, str]] = None,
            extra_keys: Tuple[str, ...] = (),
    ):
        if header is None:
            header = {}
        if not filename.endswith(Monitor.EXT):
            if os.path.isdir(filename):
                filename = os.path.join(filename, Monitor.EXT)
            else:
                filename = filename + "." + Monitor.EXT
        self.file_handler = open(filename, "wt")
        self.file_handler.write("#%s\n" % json.dumps(header))
        self.logger = csv.DictWriter(self.file_handler, fieldnames=("r", "l", "t") + extra_keys)
        self.logger.writeheader()
        self.file_handler.flush()

    def write_row(self, epinfo: Dict[str, Union[float, int]]) -> None:
        """
        Close the file handler
        :param epinfo: the information on episodic return, length, and time
        """
        if self.logger:
            self.logger.writerow(epinfo)
            self.file_handler.flush()

    def close(self) -> None:
        """
        Close the file handler
        """
        self.file_handler.close()

class SB3VecMonitor(VecEnvWrapper):
    """
    A vectorized monitor wrapper for vectorized Gym environments, copied from the SB3 version 1.1.0a7

    :param venv: The vectorized environment
    :param filename: the location to save a log file, can be None for no log
    :param info_keywords: extra information to log, from the information return of env.step()
    """

    def __init__(
            self,
            venv: VecEnv,
            filename: Optional[str] = None,
            info_keywords: Tuple[str, ...] = (),
    ):
        from stable_baselines3.common.monitor import Monitor as local_monitor_module
        try:
            is_wrapped_with_monitor = venv.env_is_wrapped(local_monitor_module)[0]
        except AttributeError:
            is_wrapped_with_monitor = False

        if is_wrapped_with_monitor:
            warnings.warn(
                "The environment is already wrapped with a `Monitor` wrapper"
                "but you are wrapping it with a `VecMonitor` wrapper, the `Monitor` statistics will be"
                "overwritten by the `VecMonitor` ones.",
                UserWarning,
            )

        VecEnvWrapper.__init__(self, venv)
        self.episode_returns = None
        self.episode_lengths = None
        self.episode_count = 0
        self.t_start = time.time()

        env_id = None
        if hasattr(venv, "spec") and venv.spec is not None:
            env_id = venv.spec.id

        if filename:
            self.results_writer = ResultsWriter(
                filename, header={"t_start": self.t_start, "env_id": env_id}, extra_keys=info_keywords
            )
        else:
            self.results_writer = None
        self.info_keywords = info_keywords

    def reset(self) -> VecEnvObs:
        obs = self.venv.reset()
        self.episode_returns = np.zeros(self.num_envs, dtype=np.float32)
        self.episode_lengths = np.zeros(self.num_envs, dtype=np.int32)
        return obs

    def step_wait(self) -> VecEnvStepReturn:
        obs, rewards, dones, infos = self.venv.step_wait()
        self.episode_returns += rewards
        self.episode_lengths += 1
        new_infos = list(infos[:])
        for i in range(len(dones)):
            if dones[i]:
                info = infos[i].copy()
                episode_return = self.episode_returns[i]
                episode_length = self.episode_lengths[i]
                episode_info = {"r": episode_return, "l": episode_length, "t": round(time.time() - self.t_start, 6)}
                info["episode"] = episode_info
                self.episode_count += 1
                self.episode_returns[i] = 0
                self.episode_lengths[i] = 0
                if self.results_writer:
                    self.results_writer.write_row(episode_info)
                new_infos[i] = info
        return obs, rewards, dones, new_infos

    def close(self) -> None:
        if self.results_writer:
            self.results_writer.close()
        return self.venv.close()

class SB3SingleInstanceWrapper(VecEnv):
    """
    Class for wrapping a single env into a VecEnv (each car is treated as its own environment).
    """
    def __init__(self, env: Gym):
        """
        :param env: the environment to wrap.
        """
        super().__init__(env._match.agents, env.observation_space, env.action_space)
        self.env = env
        self.step_result = None

    def reset(self) -> VecEnvObs:
        return tuple(self.env.reset())

    def step_async(self, actions: np.ndarray) -> None:
        self.step_result = self.env.step(actions)

    def step_wait(self) -> VecEnvStepReturn:
        observations, rewards, done, info = self.step_result
        return tuple(observations), np.array(rewards), np.full(len(rewards), done), [info] * len(rewards)

    def close(self) -> None:
        self.env.close()

    def seed(self, seed: Optional[int] = None) -> List[Union[None, int]]:
        return [self.env.seed(seed)] * self.num_envs

    # Now a bunch of functions that need to be overridden to work, might have to implement later
    def get_attr(self, attr_name: str, indices: VecEnvIndices = None) -> List[Any]: pass
    def set_attr(self, attr_name: str, value: Any, indices: VecEnvIndices = None) -> None: pass
    def env_method(self, method_name: str, *method_args, indices: VecEnvIndices = None, **method_kwargs) -> List[Any]: pass
    def env_is_wrapped(self, wrapper_class: Type[gym.Wrapper], indices: VecEnvIndices = None) -> List[bool]: pass
    def get_images(self) -> Sequence[np.ndarray]: pass


class SB3MultipleInstanceWrapper(SubprocVecEnv):
    """
    Class for launching several Rocket League instances into a single SubprocVecEnv for use with Stable Baselines.
    """
    def __init__(self, path_to_epic_rl, num_instances, match_args_func, wait_time=60):
        """
        :param path_to_epic_rl: Path to the Rocket League executable of the Epic version.
        :param num_instances: the number of Rocket League instances to start up.
        :param match_args_func: a function which produces the arguments for the Match object.
                                Needs to be a function so that each subprocess can call it and get their own objects.
        :param wait_time: the time to wait between launching each instance. Default one minute.
        """
        def spawn_process():
            match = Match(**match_args_func())
            env = Gym(match, pipe_id=os.getpid(), path_to_rl=path_to_epic_rl, use_injector=True)
            return env

        match_args = match_args_func()

        # super().__init__([])  Super init intentionally left out since we need to launch processes with delay

        env_fns = [spawn_process for _ in range(num_instances)]

        # START - Code from SubprocVecEnv class
        self.waiting = False
        self.closed = False
        n_envs = len(env_fns)

        # Fork is not a thread safe method (see issue #217)
        # but is more user friendly (does not require to wrap the code in
        # a `if __name__ == "__main__":`)
        forkserver_available = "forkserver" in mp.get_all_start_methods()
        start_method = "forkserver" if forkserver_available else "spawn"
        ctx = mp.get_context(start_method)

        self.remotes, self.work_remotes = zip(*[ctx.Pipe() for _ in range(n_envs)])
        self.processes = []
        for work_remote, remote, env_fn in zip(self.work_remotes, self.remotes, env_fns):
            args = (work_remote, remote, CloudpickleWrapper(env_fn))
            # daemon=True: if the main process crashes, we should not cause things to hang
            process = ctx.Process(target=_worker, args=args, daemon=True)  # pytype:disable=attribute-error
            process.start()
            self.processes.append(process)
            work_remote.close()
            time.sleep(wait_time)  # ADDED - Waits between starting Rocket League instances

        self.remotes[0].send(("get_spaces", None))
        observation_space, action_space = self.remotes[0].recv()
        # END - Code from SubprocVecEnv class

        self.n_agents_per_env = match_args.get("team_size") * (1 + match_args.get("self_play", False))
        self.num_envs = num_instances * self.n_agents_per_env
        VecEnv.__init__(self, self.num_envs, observation_space, action_space)

    def reset(self) -> VecEnvObs:
        for remote in self.remotes:
            remote.send(("reset", None))
        obs = sum((remote.recv() for remote in self.remotes), [])
        return tuple(obs)

    def step_async(self, actions: np.ndarray) -> None:
        i = 0
        for remote in self.remotes:
            remote.send(("step", actions[i: i + self.n_agents_per_env, :]))
            i += self.n_agents_per_env
        self.waiting = True

    def step_wait(self) -> VecEnvStepReturn:
        results = [remote.recv() for remote in self.remotes]
        self.waiting = False
        obs, rews, dones, infos = zip(*results)

        obs = sum(obs, [])
        rews = sum(rews, [])
        dones = [d for d in dones for _ in range(self.n_agents_per_env)]
        infos = [i for i in infos for _ in range(self.n_agents_per_env)]
        return tuple(obs), np.array(rews), np.array(dones), infos

    def seed(self, seed: Optional[int] = None) -> List[Union[None, int]]:
        res = super(SB3MultipleInstanceWrapper, self).seed(seed)
        return [r for r in res for _ in range(self.n_agents_per_env)]

    def _get_target_remotes(self, indices: VecEnvIndices) -> List[Any]:
        # Override to prevent out of bounds
        indices = self._get_indices(indices)
        return [self.remotes[i // self.n_agents_per_env] for i in indices]
