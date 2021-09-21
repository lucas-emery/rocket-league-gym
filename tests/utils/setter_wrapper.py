from rlgym.utils import StateSetter
from rlgym.utils.state_setters import DefaultState, StateWrapper


class SetterWrapper(StateSetter):
    def __init__(self):
        super().__init__()
        self.state_setter = DefaultState()

    def set(self, state_setter: StateSetter):
        self.state_setter = state_setter

    def reset(self, state_wrapper: StateWrapper):
        return self.state_setter.reset(state_wrapper)
