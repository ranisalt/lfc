import unittest
from dfa import DFA, load_dfa


class FiniteAutomatonTest(unittest.TestCase):
    def setUp(self):
        self.automaton = DFA(
            alphabet={'0', '1'},
            states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5'},
            initial_state='q0',
            transitions={
                ('q0', '0'): 'q0',
                ('q0', '1'): 'q1',
                ('q1', '0'): 'q2',
                ('q1', '1'): 'q3',
                ('q2', '0'): 'q4',
                ('q2', '1'): 'q5',
                ('q3', '0'): 'q0',
                ('q3', '1'): 'q1',
                ('q4', '0'): 'q2',
                ('q4', '1'): 'q3',
                ('q5', '0'): 'q4',
                ('q5', '1'): 'q5',
                },
            final_states={'q1', 'q2', 'q3'},
            )

    def test_remove_unreachable(self):
        automaton = DFA(
            alphabet={'0', '1'},
            states={'q0', 'q1', 'q2'},
            initial_state='q0',
            transitions={
                ('q0', '0'): 'q1',
                ('q2', '1'): 'q2',
                },
            final_states={'q1', 'q2'},
            )

        cleaned = automaton.remove_unreachable()
        self.assertSetEqual({'0'}, cleaned.alphabet)
        self.assertSetEqual({'q0', 'q1'}, cleaned.states)
        self.assertEqual('q0', cleaned.initial_state)
        self.assertDictEqual({
            ('q0', '0'): 'q1',
            }, cleaned.transitions)
        self.assertSetEqual({'q1'}, cleaned.final_states)

    def test_accept(self):
        self.assertFalse(self.automaton.accept('101'))
        self.assertTrue(self.automaton.accept('111'))

    def test_step(self):
        self.assertEqual(self.automaton.step('q0', '0'), 'q0')

    def test_load(self):
        with open('fixture.json') as fp:
            automaton = load_dfa(fp)

        self.assertSetEqual(self.automaton.alphabet, automaton.alphabet)
        self.assertSetEqual(self.automaton.states, automaton.states)
        self.assertEqual(self.automaton.initial_state, automaton.initial_state)
        self.assertDictEqual(self.automaton.transitions, automaton.transitions)
        self.assertSetEqual(self.automaton.final_states,
                            automaton.final_states)


if __name__ == '__main__':
    unittest.main()
