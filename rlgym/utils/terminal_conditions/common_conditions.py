"""
A module containing implementations of common terminal conditions.
"""

from rlgym.utils.terminal_conditions import TerminalCondition
from rlgym.utils.gamestates import GameState


class TimeoutCondition(TerminalCondition):
    """
    A condition that will terminate an episode after some number of steps.
    """

    def __init__(self, max_steps: int):
        super().__init__()
        self.steps = 0
        self.max_steps = max_steps

    def reset(self, initial_state: GameState):
        """
        Reset the step counter.
        """

        self.steps = 0

    def is_terminal(self, current_state: GameState) -> bool:
        """
        Increment the current step counter and return `True` if `max_steps` have passed.
        """

        self.steps += 1
        return self.steps >= self.max_steps


class NoTouchTimeoutCondition(TimeoutCondition):
    def is_terminal(self, current_state: GameState):
        if any(p.ball_touched for p in current_state.players):
            self.steps = 0
            return False
        else:
            return super(NoTouchTimeoutCondition, self).is_terminal(current_state)


class GoalScoredCondition(TerminalCondition):
    """
    A condition that will terminate an episode as soon as a goal is scored by either side.
    """

    def __init__(self):
        super().__init__()
        self.blue_score = 0
        self.orange_score = 0

    def reset(self, initial_state: GameState):
        pass

    def is_terminal(self, current_state: GameState) -> bool:
        """
        Check to see if the game score for either team has been changed. If either score has changed, update the current
        known scores for both teams and return `True`. Note that the known game scores are never reset for this object
        because the game score is not set to 0 for both teams at the beginning of an episode.
        """

        if current_state.blue_score != self.blue_score or current_state.orange_score != self.orange_score:
            self.blue_score = current_state.blue_score
            self.orange_score = current_state.orange_score
            return True
        return False


class BallTouchedCondition(TerminalCondition):

    def __init__(self):
        super().__init__()
        self.last_touch = None

    def reset(self, initial_state: GameState):
        self.last_touch = initial_state.last_touch

    def is_terminal(self, current_state: GameState) -> bool:
        """
        Return `True` if the last touch does not have the same ID as the last touch from the initial state.
        """
        return current_state.last_touch != self.last_touch
