"""
A module containing implementations of common terminal conditions.
"""

from rlgym.utils.terminal_conditions import TerminalCondition

class TimeoutCondition(TerminalCondition):
    """
    A condition that will terminate an episode after some number of steps.
    """

    def __init__(self, max_steps):
        super().__init__()
        self.steps = 0
        self.max_steps = max_steps

    def reset(self, initial_state):
        """
        Reset the step counter.
        """

        self.steps = 0

    def is_terminal(self, current_state):
        """
        Increment the current step counter and return `True` if `max_steps` have passed.
        """

        self.steps += 1
        return self.steps >= self.max_steps

    def look_ahead(self, current_state):
        """
        Check if incrementing the step counter will result in `max_steps` having passed. This is a good example usage of
        the `look_ahead` function, as it does not simply call `is_terminal`, but checks to see if a call to `is_terminal`
        would result in a `True` condition.
        """

        return self.steps + 1 >= self.max_steps


class GoalScoredCondition(TerminalCondition):
    """
    A condition that will terminate an episode as soon as a goal is scored by either side.
    """

    def __init__(self):
        super().__init__()
        self.blue_score = 0
        self.orange_score = 0

    def reset(self, initial_state):
        pass

    def is_terminal(self, current_state):
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

    def look_ahead(self, current_state):
        """
        Check to see if the game score for either team is different from the current known game score for both teams.
        Note that here, because we are looking ahead at the current state, we do not update the current known game scores.
        """

        if current_state.blue_score != self.blue_score or current_state.orange_score != self.orange_score:
            return True
        return False

class BallTouchedCondition(TerminalCondition):
    def __init__(self):
        super().__init__()
        self.last_touch = None

    def reset(self, initial_state):
        self.last_touch = initial_state.last_touch

    def is_terminal(self, current_state):
        """
        Return `True` if the last touch does not have the same ID as the last touch from the initial state.
        """
        return current_state.last_touch != self.last_touch

    def look_ahead(self, current_state):
        """
        Since this terminal condition is not updated when `is_terminal` gets called, we can simply wrap that function
        here.
        """
        return self.is_terminal(current_state)