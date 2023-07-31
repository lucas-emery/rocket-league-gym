from abc import ABC
from typing import Optional, Dict, Any

from rlgym.api.config.state_setter import StateSetter
from rlgym.rocket_league.wrappers.state_wrapper import StateWrapper
from rlgym.rocket_league.engine.game_state import GameState


class FixedSizeSetter(StateSetter, ABC):

    def __init__(self, blue_team_size: int, orange_team_size: int):
        super().__init__()
        self.blue_team_size = blue_team_size
        self.orange_team_size = orange_team_size

    def build_wrapper(self, prev_state: Optional[GameState], shared_info: Dict[str, Any]) -> StateWrapper:
        #TODO change this, that constructor doesn't exist
        return StateWrapper(blue_count=self.blue_team_size, orange_count=self.orange_team_size)
