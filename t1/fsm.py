import json
from itertools import chain
from typing import Dict, NamedTuple, Optional, Set, Tuple

Symbol = str
State = str


class DFA(NamedTuple):
    alphabet: Set[Symbol]
    states: Set[State]
    initial_state: State
    transitions: Dict[Tuple[Symbol, State], State]
    final_states: Set[State]

    def accept(self, word) -> bool:
        state = self.initial_state
        for symbol in word:
            state = self.step(state, symbol)
            if state is None:
                return False
        return state in self.final_states

    def step(self, state: State, symbol: Symbol) -> Optional[str]:
        tpl = (state, symbol)
        if tpl in self.transitions:
            return self.transitions[tpl]
        return None

    @classmethod
    def create(cls, initial_state, transitions, final_states):
        alphabet = {s for _, s in transitions}

        s = chain.from_iterable((k[0], v) for k, v in transitions.items())
        states = {initial_state, } | set(final_states) | set(s)

        return cls(alphabet, states, initial_state, transitions, final_states)

    @classmethod
    def load(cls, fp):
        raw = json.load(fp)

        return cls.create(
            initial_state=raw['initial_state'],
            transitions={(t[0], t[1]): t[2] for t in raw['transitions']},
            final_states=set(raw['final_states'])
            )
