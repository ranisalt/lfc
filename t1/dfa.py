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

    def remove_unreachable(self):
        reachable = {self.initial_state, }
        new_states = {self.initial_state, }

        while len(new_states) > 0:
            temp = set()
            for q in new_states:
                for c in self.alphabet:
                    state = self.step(q, c)
                    if state:
                        temp.add(state)

            new_states = temp - reachable
            reachable = reachable | new_states

        return self.create(
            initial_state=self.initial_state,
            transitions={
                k: v for k, v in self.transitions.items()
                if k[0] in reachable and v in reachable
                },
            final_states={q for q in self.final_states if q in reachable}
            )

    def accept(self, word) -> bool:
        state = self.initial_state
        for symbol in word:
            state = self.step(state, symbol)
            if not state:
                return False
        return state in self.final_states

    def step(self, state: State, symbol: Symbol) -> Optional[str]:
        return self.transitions.get((state, symbol))

    def to_nfa(self):
        return NFA.create(
            self.initial_state, {
                k: [v] for k, v in self.transitions.items()
                }, self.final_states
            )

    @classmethod
    def create(cls, initial_state, transitions, final_states):
        alphabet = {s for _, s in transitions}

        s = chain.from_iterable((k[0], v) for k, v in transitions.items())
        states = {initial_state, } | set(final_states) | set(s)

        return cls(alphabet, states, initial_state, transitions, final_states)


def load_dfa(fp) -> DFA:
    raw = json.load(fp)

    return DFA.create(
        initial_state=raw['initial_state'],
        transitions={(t[0], t[1]): t[2] for t in raw['transitions']},
        final_states=set(raw['final_states'])
        )
