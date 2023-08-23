from typing import Any, Dict

from rlgym.api import StateMutator, StateType


class MutatorSequence(StateMutator[StateType]):

    def __init__(self, *mutators: StateMutator[StateType]):
        self.mutators = tuple(mutators)

    def apply(self, state: StateType, shared_info: Dict[str, Any]) -> None:
        for mutator in self.mutators:
            mutator.apply(state, shared_info)
