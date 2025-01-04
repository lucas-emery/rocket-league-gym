import numpy as np
from typing import Dict, Any, List

from rlgym.api import TransitionEngine, AgentID
from rlgym.rocket_league.api import GameState


class GameEngine(TransitionEngine[AgentID, GameState, np.ndarray]):  # TODO remove for release?
    """
    WIP Don't use yet
    """

    def __init__(self):
        """
        :param game_speed: The speed the physics will run at, leave it at 100 unless your game can't run at over 240fps
        :param launch_preference: Rocket League launch preference (rlgym.gamelaunch.LaunchPreference) or path to RocketLeague executable
        :param use_injector: Whether to use RLGym's bakkesmod injector or not. Enable if launching multiple instances
        :param force_paging: Enable forced paging of each spawned rocket league instance to reduce memory utilization
                                immediately, instead of allowing the OS to slowly page untouched allocations.
                                WARNING: This will require you to potentially expand your Windows Page File [1]
                                and it may substantially increase disk activity, leading to decreased disk lifetime.
                                Use at your own peril.
                                Default is off: OS dictates the behavior.
        :param raise_on_crash: If enabled, raises an exception when Rocket League crashes instead of attempting to recover.
                                You can attempt a recovery manually by calling attempt_recovery()
        :param auto_minimize: Automatically minimize the game window when launching Rocket League
        [1]: https://www.tomshardware.com/news/how-to-manage-virtual-memory-pagefile-windows-10,36929.html
        """
        pass

    @property
    def agents(self) -> List[AgentID]:
        pass

    @property
    def max_num_agents(self) -> int:
        pass

    @property
    def state(self) -> GameState:
        pass

    @property
    def config(self) -> Dict[AgentID, Any]:
        pass

    def step(self, actions: Dict[AgentID, np.ndarray], shared_info: Dict[str, Any]) -> GameState:
        pass

    def create_base_state(self) -> GameState:
        pass

    def set_state(self, desired_state: GameState, shared_info: Dict[str, Any]) -> GameState:
        pass

    def close(self) -> None:
        pass
