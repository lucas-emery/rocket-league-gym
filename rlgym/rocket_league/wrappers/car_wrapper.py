import numpy as np


class CarWrapper:
    team_num: int
    position: np.ndarray
    rotation: np.ndarray
    linear_velocity: np.ndarray
    angular_velocity: np.ndarray
    boost: float
