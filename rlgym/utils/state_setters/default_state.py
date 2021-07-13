from rlgym.utils.gamestates.state_wrapper import StateWrapper
from rlgym.utils.state_setters import StateSetter
import random
import numpy as np


class DefaultState(StateSetter):

    SPAWN_BLUE_POS = [[-2048, -2560, 17], [2048, -2560, 17],
                      [-256, -3840, 17], [256, -3840, 17], [0, -4608, 17]]
    SPAWN_BLUE_YAW = [0.25 * np.pi, 0.75 * np.pi,
                      0.5 * np.pi, 0.5 * np.pi, 0.5 * np.pi]
    SPAWN_ORANGE_POS = [[2048, 2560, 17], [-2048, 2560, 17],
                        [256, 3840, 17], [-256, 3840, 17], [0, 4608, 17]]
    SPAWN_ORANGE_YAW = [-0.75 * np.pi, -0.25 *
                        np.pi, -0.5 * np.pi, -0.5 * np.pi, -0.5 * np.pi]

    def __init__(self):
        super().__init__()

    def reset(self, state_wrapper: StateWrapper):
        """
        Modifies the StateWrapper to contain default kickoff values, randomly selected from a list.
        """
        possible_inds = [0, 1, 2, 3, 4]
        random.shuffle(possible_inds)

        for i in range(len(state_wrapper.blue)):
            state_wrapper.blue[i].position = np.array(
                self.SPAWN_BLUE_POS[possible_inds[i]])
            state_wrapper.blue[i]._euler_angles[1] = self.SPAWN_BLUE_YAW[possible_inds[i]]
            state_wrapper.blue[i]._has_computed_euler_angles = True
            state_wrapper.blue_boost[i] = 0.33

        for i in range(len(state_wrapper.orange)):
            state_wrapper.orange[i].position = np.array(
                self.SPAWN_ORANGE_POS[possible_inds[i]])
            state_wrapper.orange[i]._euler_angles[1] = self.SPAWN_ORANGE_YAW[possible_inds[i]]
            state_wrapper.orange[i]._has_computed_euler_angles = True
            state_wrapper.orange_boost[i] = 0.33
