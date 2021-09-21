from rlgym.gym import Gym
from rlgym.utils import StateSetter
from typing import Dict


class BaseTest:

    def get_config(self) -> Dict:
        raise NotImplementedError()

    def get_state_setter(self) -> StateSetter:
        raise NotImplementedError()

    def run(self, env: Gym):
        raise NotImplementedError()
