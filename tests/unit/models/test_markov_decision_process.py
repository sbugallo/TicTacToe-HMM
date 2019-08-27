import numpy as np
import pytest
from numpy.testing import assert_array_equal

from ttt.models import TicTacToeMDP, State


def test_mdp_initializes_correctly():
    mdp = TicTacToeMDP()
    assert not mdp.states


@pytest.mark.parametrize("states, grid, expected_results", [
    ({}, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), False),
    ({0: State(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))}, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), True),
    ({0: State(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))}, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]), False),
])
def test_mdp_has_state_correctness(states, grid, expected_results):
    mdp = TicTacToeMDP()
    mdp.states = states

    assert mdp.has_state(State(grid)) == expected_results


@pytest.mark.parametrize("states, grid, expected_results", [
    ({}, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 1),
    ({0: State(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))}, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]), 2)
])
def test_mdp_add_state_correctness(states, grid, expected_results):
    mdp = TicTacToeMDP()
    mdp.states = states
    mdp.add_state(State(grid))

    assert len(mdp.states) == expected_results
    assert_array_equal(mdp.states[len(mdp.states) - 1].grid, grid)


def test_mdp_get_state_correctness():
    mdp = TicTacToeMDP()
    mdp.states = {
        0: State(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])),
        1: State(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])),
    }

    result = mdp.get_state(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])).grid
    assert_array_equal(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), result)


def test_mdp_get_state_raises_value_error_if_state_not_found():
    mdp = TicTacToeMDP()
    mdp.states = {}

    with pytest.raises(ValueError, match="could not be found in saved states"):
        mdp.get_state(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))


def test_mdp_update_state_correctness():
    mdp = TicTacToeMDP()
    mdp.states = {
        0: State(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])),
        1: State(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0])),
    }

    new_state = State(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0]))
    new_state.next_states_values *= 2

    mdp.update_state(new_state)

    assert_array_equal(mdp.states[1].next_states_values, new_state.next_states_values)


def test_mdp_serialize_correctness():
    mdp = TicTacToeMDP()
    mdp.states = {
        0: State(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])),
        1: State(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0])),
    }

    serialized_mdp = mdp.serialize()

    assert 'states' in serialized_mdp
    assert len(serialized_mdp["states"]) == 2

    assert_array_equal(serialized_mdp["states"]["0"]["grid"], np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    assert_array_equal(serialized_mdp["states"]["1"]["grid"], np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0]))

    assert_array_equal(serialized_mdp["states"]["0"]["next_states_values"], np.array([0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0]))
    assert_array_equal(serialized_mdp["states"]["1"]["next_states_values"], np.array([0]))

    assert_array_equal(serialized_mdp["states"]["0"]["next_states_transitions"],
                       np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    assert_array_equal(serialized_mdp["states"]["1"]["next_states_transitions"], np.array([9]))


def test_mdp_deserialize_correctness():
    serialized_mdp = {
        'states': {
            '0': {
                'grid': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'next_states_values': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                'next_states_transitions': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            },
            '1': {
                'grid': [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                'next_states_values': [0.0],
                'next_states_transitions': [9]
            }
        }
    }

    mdp = TicTacToeMDP()
    mdp.deserialize(serialized_mdp)

    assert_array_equal(mdp.states[0].grid, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    assert_array_equal(mdp.states[1].grid, np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0]))

    assert_array_equal(mdp.states[0].next_states_values, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    assert_array_equal(mdp.states[1].next_states_values, np.array([0]))

    assert_array_equal(mdp.states[0].next_states_transitions, np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    assert_array_equal(mdp.states[1].next_states_transitions, np.array([9]))
