from typing import Any, Dict, List

from rlgym.api.config.state_mutator import StateMutator
from rlgym.api.typing import StateType


class MutatorSequence(StateMutator[StateType]):

    def __init__(self, mutators: List[StateMutator[StateType]]):
        self.mutators = mutators

    def apply(self, state: StateType, shared_info: Dict[str, Any]) -> None:
        for mutator in self.mutators:
            mutator.apply(state, shared_info)
