import numpy as np
from numpy.testing import assert_array_equal

from ttt.models import State


def test_state_initializes_correctly():
    grid = np.array([0, 0, 0, 0, 0, 1, 2, 2, 0])
    state = State(grid)

    assert_array_equal(state.grid, grid)
    assert_array_equal(state.next_states_transitions, np.array([0, 1, 2, 3, 4, 8]))
    assert_array_equal(state.next_states_values, np.zeros(6))


def test_state_initializes_correctly_when_grid_is_none():
    state = State()

    assert state.grid is None
    assert state.next_states_transitions is None
    assert state.next_states_values is None


def test_state_compute_next_states_correctness():
    state = State()
    state.grid = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    state._compute_next_states()
    assert_array_equal(state.next_states_transitions, np.array([0, 1, 2, 3, 4, 5, 6, 7, 8]))
    assert_array_equal(state.next_states_values, np.zeros(9))


def test_state_update_transition_weight_correctness():
    grid = np.array([0, 1, 1, 2, 2, 1, 1, 2, 0])
    state = State(grid)
    state.update_transition_weight(8, -3)
    assert_array_equal(state.next_states_values, np.array([0, -3]))


def test_state_get_next_move():
    grid = np.array([0, 1, 1, 2, 2, 1, 1, 2, 0])
    state = State(grid)
    state.update_transition_weight(8, -3)

    assert state.get_best_move() == 0


def test_state_serialize():
    serialized_state = State(np.array([0, 1, 1, 2, 2, 1, 1, 2, 0])).serialize()

    assert "grid" in serialized_state
    assert "next_states_values" in serialized_state
    assert "next_states_transitions" in serialized_state

    assert serialized_state["grid"] == [0, 1, 1, 2, 2, 1, 1, 2, 0]
    assert serialized_state["next_states_values"] == [0, 0]
    assert serialized_state["next_states_transitions"] == [0, 8]


def test_state_deserialize():
    state = State()
    state.deserialize({
        "grid": [0, 1, 1, 2, 2, 1, 1, 2, 0],
        "next_states_values": [0, 0],
        "next_states_transitions": [0, 8]
    })

    assert_array_equal(state.grid, np.array([0, 1, 1, 2, 2, 1, 1, 2, 0]))
    assert_array_equal(state.next_states_transitions, np.array([0, 8]))
    assert_array_equal(state.next_states_values, np.array([0, 0]))
