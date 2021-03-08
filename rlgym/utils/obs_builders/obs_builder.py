from abc import ABC, abstractmethod
from rlgym.utils.gamestates import PhysicsObject, PlayerData, GameState
import numpy as np
from typing import Any


class ObsBuilder(ABC):
    @staticmethod
    def get_random_physics_state():
        means = [-7.55690032e+00, -7.67272187e+02, 3.99790479e+01, 4.33080865e-01, 3.29746054e-03, 9.68255500e-03,
                 4.10564683e-01, 1.64972058e+01, -9.52952112e+00, 1.21217917e-01, 6.23036234e-03, -1.84941779e-03,
                 -1.82993569e-02, np.pi, np.pi, np.pi]

        stds = [2.22632843e+03, 3.31466701e+03, 7.04738414e+01, 5.49264807e-01, 1.37360694e-01, 1.42669913e-01,
                5.50325801e-01, 6.42938410e+02, 7.39945204e+02, 1.34840452e+02, 7.39983198e-01, 7.07553505e-01,
                1.78035710e+00, np.pi, np.pi, np.pi]

        mu = np.asarray(means)
        sigma = np.asarray(stds)

        obs = (np.random.randn(len(means)) * sigma + mu).tolist()
        obj = PhysicsObject()
        obj.position = obs[:3]
        obj.quaternion = obs[3:7]
        obj.linear_velocity = obs[7:10]
        obj.angular_velocity = obs[10:13]
        obj._euler_angles = obs[13:]  # TODO remove this
        return obj

    def __init__(self):
        pass

    # This method is optional
    @abstractmethod
    def reset(self, optional_data=None):
        raise NotImplementedError

    # This method is optional
    @abstractmethod
    def build_obs(self, state: GameState, optional_data=None) -> np.ndarray:
        raise NotImplementedError

    # This is the function that rlgym calls to make the obs for each agent
    # A List of whatever you return here will be the value of "obs" returned from gym.step
    @abstractmethod
    def build_obs_for_player(self, player: PlayerData, state: GameState, previous_action: np.ndarray, optional_data=None) -> Any:
        raise NotImplementedError
