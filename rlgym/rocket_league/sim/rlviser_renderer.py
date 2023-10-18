from typing import Any

import rlviser_py as rlviser
from rlgym.api.config.renderer import Renderer
from rlgym.rocket_league.api.game_state import GameState
from rlgym.rocket_league.common_values import BOOST_LOCATIONS


class RLViserRenderer(Renderer[GameState]):

    def __init__(self, tick_rate=120/8):
        rlviser.set_boost_pad_locations(BOOST_LOCATIONS)
        self.tick_rate = tick_rate
        self.packet_id = 0

    def render(self, state: GameState, _) -> Any:
        self.packet_id += 1
        rlviser.render_rlgym(self.packet_id, self.tick_rate, state)

    def close(self):
        rlviser.quit()
