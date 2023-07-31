import numpy as np
from typing import Dict, Any, List

from rlgym.api.engine.transition_engine import TransitionEngine
from rlgym.rocket_league.engine.game_state import GameState
from rlgym.rocket_league.wrappers.state_wrapper import StateWrapper


class GameEngine(TransitionEngine[str, GameState, StateWrapper, np.ndarray]):

    @property
    def agents(self) -> List[str]:
        pass

    @property
    def max_num_agents(self) -> int:
        pass

    @property
    def state(self) -> GameState:
        pass

    @property
    def config(self) -> Dict[str, Any]:
        pass

    def step(self, actions: Dict[str, np.ndarray]) -> GameState:
        pass

    def set_state(self, state_wrapper: StateWrapper) -> GameState:
        pass

    def close(self) -> None:
        pass
