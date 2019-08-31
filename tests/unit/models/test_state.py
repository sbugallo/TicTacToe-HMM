import numpy as np
import pytest
from numpy.testing import assert_array_equal

from ttt.models import State, Action


@pytest.mark.unit
def test_state_initializes_correctly():
    grid = np.array([0, 0, 0, 0, 0, 1, 2, 2, 0])
    state = State(grid)

    assert_array_equal(state.grid, grid)
    assert_array_equal(state.next_states_transitions, np.array([Action.top_left, Action.top_center, Action.top_right,
                                                                Action.middle_left, Action.middle_center,
                                                                Action.bottom_right]))
    assert_array_equal(state.next_states_values, np.zeros(6))


@pytest.mark.unit
def test_state_initializes_correctly_when_grid_is_none():
    state = State()

    assert state.grid is None
    assert state.next_states_transitions is None
    assert state.next_states_values is None


@pytest.mark.unit
def test_state_compute_next_states_correctness():
    state = State()
    state.grid = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    state._compute_next_states()
    assert_array_equal(state.next_states_transitions, np.array([Action.top_left, Action.top_center,
                                                                Action.top_right, Action.middle_left,
                                                                Action.middle_center, Action.middle_right,
                                                                Action.bottom_left, Action.bottom_center,
                                                                Action.bottom_right]))
    assert_array_equal(state.next_states_values, np.zeros(9))


@pytest.mark.unit
def test_state_update_transition_weight_correctness():
    grid = np.array([0, 1, 1, 2, 2, 1, 1, 2, 0])
    state = State(grid)
    state.update_transition_weight(Action.bottom_right, -3)
    assert_array_equal(state.next_states_values, np.array([0, -3]))


@pytest.mark.unit
def test_state_get_next_move():
    grid = np.array([0, 1, 1, 2, 2, 1, 1, 2, 0])
    state = State(grid)
    state.update_transition_weight(Action.bottom_right, -3)

    assert state.get_best_move() == Action.top_left


@pytest.mark.unit
def test_state_serialize():
    serialized_state = State(np.array([0, 1, 1, 2, 2, 1, 1, 2, 0])).serialize()

    assert "grid" in serialized_state
    assert "next_states_values" in serialized_state
    assert "next_states_transitions" in serialized_state

    assert serialized_state["grid"] == [0, 1, 1, 2, 2, 1, 1, 2, 0]
    assert serialized_state["next_states_values"] == [0, 0]
    assert serialized_state["next_states_transitions"] == [0, 8]


@pytest.mark.unit
def test_state_deserialize():
    state = State()
    state.deserialize({
        "grid": [0, 1, 1, 2, 2, 1, 1, 2, 0],
        "next_states_values": [0, 0],
        "next_states_transitions": [0, 8]
    })

    assert_array_equal(state.grid, np.array([0, 1, 1, 2, 2, 1, 1, 2, 0]))
    assert_array_equal(state.next_states_transitions, np.array([Action.top_left, Action.bottom_right]))
    assert_array_equal(state.next_states_values, np.array([0, 0]))
