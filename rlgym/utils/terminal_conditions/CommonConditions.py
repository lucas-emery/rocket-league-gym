from rlgym.utils.terminal_conditions import TerminalCondition

class TimeoutCondition(TerminalCondition):
    def __init__(self, max_ticks):
        super().__init__()
        self.ticks = 0
        self.max_ticks = max_ticks

    def reset(self, optional_data=None):
        self.ticks = 0

    def is_terminal(self, state, optional_data=None):
        self.ticks += 1
        return self.ticks >= self.max_ticks

    def look_ahead(self, state, optional_data=None):
        return self.ticks + 1 >= self.max_ticks


class GoalScoredCondition(TerminalCondition):
    def __init__(self):
        super().__init__()
        self.blue_score = 0
        self.orange_score = 0

    def reset(self, optional_data=None):
        pass

    def is_terminal(self, state, optional_data=None):
        if state.blue_score != self.blue_score or state.orange_score != self.orange_score:
            self.blue_score = state.blue_score
            self.orange_score = state.orange_score
            return True
        return False

    def look_ahead(self, state, optional_data=None):
        if state.blue_score != self.blue_score or state.orange_score != self.orange_score:
            return True
        return False