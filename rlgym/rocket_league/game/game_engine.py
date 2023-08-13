import numpy as np
from typing import Dict, Any, List

from rlgym.api.engine.transition_engine import TransitionEngine
from rlgym.api.typing import AgentID
from rlgym.rocket_league.engine.game_state import GameState


class GameEngine(TransitionEngine[AgentID, GameState, np.ndarray]):
    """
    WIP Don't use yet
    """

    def __init__(self):
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

    def step(self, actions: Dict[AgentID, np.ndarray]) -> GameState:
        pass

    def create_base_state(self) -> GameState:
        pass

    def set_state(self, desired_state: GameState) -> GameState:
        pass

    def close(self) -> None:
        pass
