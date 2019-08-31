import numpy as np
import pytest
from numpy.testing import assert_array_equal

from ttt.models import CPUAgent, State, Actions
from ttt.play import play_game_cpu_vs_cpu
from ttt.rewarding import rewarding, get_move


@pytest.fixture
def sample_game():
    cpu_agent = CPUAgent()
    return play_game_cpu_vs_cpu(cpu_agent, cpu_agent, "random", "random", 1, False, False)


@pytest.mark.unit
@pytest.mark.parametrize("state_1, state_2, expected_move", [
    (State(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])), State(np.array([0, 0, 0, 0, 0, 0, 0, 0, 1])), Actions.bottom_right),
    (State(np.array([0, 2, 1, 2, 1, 2, 1, 2, 1])), State(np.array([1, 2, 1, 2, 1, 2, 1, 2, 1])), Actions.top_left),
])
def test_get_move_correctness(state_1, state_2, expected_move):
    assert expected_move == get_move(state_1, state_2)

@pytest.mark.unit
def test_get_move_raises_value_error_if_cannot_go_from_state1_to_state2():
    with pytest.raises(ValueError, match="Cannot go from state_1"):
        get_move(State(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])), State(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])))


@pytest.mark.unit
def test_rewarding_raises_assertion_error_if_player_number_is_not_valid():
    with pytest.raises(AssertionError):
        rewarding(None, 3, None)


@pytest.mark.unit
def test_rewarding_do_not_update_values_if_lr_is_0(sample_game):
    cpu_agent = rewarding(sample_game, 1, 0)
    for state in cpu_agent.states:
        values = state.next_states_values
        assert_array_equal(np.zeros(len(values)), values)


@pytest.mark.unit
def test_rewarding_only_computes_player_moves(sample_game):
    winner = sample_game.game_sequence[1].max()
    loser = 1 if winner == 2 else 2

    sample_game.game_sequence = [sample_game.game_sequence[0], sample_game.game_sequence[1]]
    sample_game.result = winner

    cpu_agent = rewarding(sample_game, loser, 0.1)
    for state in cpu_agent.states:
        values = state.next_states_values
        assert_array_equal(np.zeros(len(values)), values)

    cpu_agent = rewarding(sample_game, winner, 0.1)
    with pytest.raises(AssertionError):
        for state in cpu_agent.states:
            values = state.next_states_values
            assert_array_equal(np.zeros(len(values)), values)
