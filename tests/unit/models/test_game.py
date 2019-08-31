import numpy as np
import pytest
from numpy.testing import assert_array_equal

from ttt.models import Game, CPUAgent, HumanAgent, Actions


@pytest.mark.unit
def test_game_initializes_correctly():
    agent_1 = CPUAgent()
    agent_2 = HumanAgent()
    game = Game(agent_1, agent_2)

    assert game.player_1 == agent_1
    assert game.player_2 == agent_2

    assert_array_equal(game.player_1.grid, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))
    assert_array_equal(game.player_2.grid, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))
    assert_array_equal(game.grid, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))

    assert_array_equal(game.game_sequence, np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]]))


@pytest.mark.unit
@pytest.mark.parametrize("move, player_id, expected_result", [
    (Actions.top_center, 1, np.array([0, 1, 0, 0, 0, 0, 0, 0, 0])),
    (Actions.bottom_right, 2, np.array([0, 0, 0, 0, 0, 0, 0, 0, 2])),
])
def test_game_applies_move_correctly(move, player_id, expected_result):
    game = Game(CPUAgent(), CPUAgent())
    game.apply_move(move, player_id)
    assert_array_equal(game.grid, expected_result)


@pytest.mark.unit
@pytest.mark.parametrize("grid, move, player_id, expected_result", [
    (np.array([1, 1, 0, 0, 0, 0, 0, 0, 0]), Actions.top_right, 1, 1),
    (np.array([2, 2, 0, 0, 0, 0, 0, 0, 0]), Actions.top_right, 2, 2),
    (np.array([1, 1, 0, 0, 0, 0, 0, 0, 0]), Actions.middle_left, 1, -1),
    (np.array([1, 0, 0, 1, 0, 0, 0, 0, 0]), Actions.bottom_left, 1, 1),
    (np.array([2, 0, 0, 2, 0, 0, 0, 0, 0]), Actions.bottom_left, 2, 2),
    (np.array([1, 0, 0, 1, 0, 0, 0, 0, 0]), Actions.bottom_center, 1, -1),
    (np.array([1, 0, 0, 0, 1, 0, 0, 0, 0]), Actions.bottom_right, 1, 1),
    (np.array([2, 0, 0, 0, 2, 0, 0, 0, 0]), Actions.bottom_right, 2, 2),
    (np.array([1, 0, 0, 0, 1, 0, 0, 0, 0]), Actions.bottom_center, 1, -1)
])
def test_game_detects_victory_correctly(grid, move, player_id, expected_result):
    game = Game(CPUAgent(), CPUAgent())
    game.grid = grid
    game.apply_move(move, player_id)
    assert game.result == expected_result


@pytest.mark.unit
@pytest.mark.parametrize("grid, expected_grid_is_full, expected_result, force_win", [
    (np.array([1, 2, 2, 2, 2, 1, 1, 1, 0]), False, -1, False),
    (np.array([1, 2, 2, 2, 2, 1, 1, 1, 0]), False, 1, True),
    (np.array([1, 2, 2, 2, 2, 1, 1, 1, 2]), True, 0, False),
    (np.array([1, 2, 2, 2, 2, 1, 1, 1, 2]), True, 1, True),
])
def test_game_detects_grid_is_full_correctly(grid, expected_grid_is_full, expected_result, force_win):
    game = Game(CPUAgent(), CPUAgent())
    game.grid = grid
    if force_win:
        game.result = 1
    game.check_if_grid_is_full()

    assert game.grid_is_full == expected_grid_is_full
    assert game.result == expected_result


@pytest.mark.unit
def test_game_traces_game_sequence_correctly():
    game = Game(CPUAgent(), CPUAgent())
    game.apply_move(Actions.top_left, 1)
    game.apply_move(Actions.top_center, 2)
    game.apply_move(Actions.top_right, 2)
    game.apply_move(Actions.middle_left, 2)
    game.apply_move(Actions.middle_center, 2)
    game.apply_move(Actions.middle_right, 1)
    game.apply_move(Actions.bottom_left, 1)
    game.apply_move(Actions.bottom_center, 1)
    game.apply_move(Actions.bottom_right, 2)

    expected_game_sequence = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 2, 0, 0, 0, 0, 0, 0],
        [1, 2, 2, 2, 0, 0, 0, 0, 0],
        [1, 2, 2, 2, 2, 0, 0, 0, 0],
        [1, 2, 2, 2, 2, 1, 0, 0, 0],
        [1, 2, 2, 2, 2, 1, 1, 0, 0],
        [1, 2, 2, 2, 2, 1, 1, 1, 0],
        [1, 2, 2, 2, 2, 1, 1, 1, 2],
    ])

    assert_array_equal(game.game_sequence, expected_game_sequence)


@pytest.mark.unit
@pytest.mark.parametrize("grid, expected_result", [
    (np.array([1, 1, 1, 0, 0, 0, 0, 0, 0]), 1),
    (np.array([2, 2, 2, 0, 0, 0, 0, 0, 0]), 2),
    (np.array([0, 0, 0, 1, 1, 1, 0, 0, 0]), 1),
    (np.array([0, 0, 0, 2, 2, 2, 0, 0, 0]), 2),
    (np.array([0, 0, 0, 0, 0, 0, 1, 1, 1]), 1),
    (np.array([0, 0, 0, 0, 0, 0, 2, 2, 2]), 2),
    (np.array([1, 0, 0, 1, 0, 0, 1, 0, 0]), -1)
])
def test_game_checks_horizontal_win_correctly(grid, expected_result):
    game = Game(CPUAgent(), CPUAgent())
    game.grid = grid
    game.check_horizontal_win()

    assert game.result == expected_result


@pytest.mark.unit
@pytest.mark.parametrize("grid, expected_result", [
    (np.array([1, 0, 0, 1, 0, 0, 1, 0, 0]), 1),
    (np.array([2, 0, 0, 2, 0, 0, 2, 0, 0]), 2),
    (np.array([0, 1, 0, 0, 1, 0, 0, 1, 0]), 1),
    (np.array([0, 2, 0, 0, 2, 0, 0, 2, 0]), 2),
    (np.array([0, 0, 1, 0, 0, 1, 0, 0, 1]), 1),
    (np.array([0, 0, 2, 0, 0, 2, 0, 0, 2]), 2),
    (np.array([1, 1, 1, 0, 0, 0, 0, 0, 0]), -1)
])
def test_game_checks_vertical_win_correctly(grid, expected_result):
    game = Game(CPUAgent(), CPUAgent())
    game.grid = grid
    game.check_vertical_win()

    assert game.result == expected_result


@pytest.mark.unit
@pytest.mark.parametrize("grid, expected_result", [
    (np.array([1, 0, 0, 0, 1, 0, 0, 0, 1]), 1),
    (np.array([2, 0, 0, 0, 2, 0, 0, 0, 2]), 2),
    (np.array([0, 0, 1, 0, 1, 0, 1, 0, 0]), 1),
    (np.array([0, 0, 2, 0, 2, 0, 2, 0, 0]), 2),
    (np.array([1, 1, 1, 0, 0, 0, 0, 0, 0]), -1)
])
def test_game_checks_diagonal_win_correctly(grid, expected_result):
    game = Game(CPUAgent(), CPUAgent())
    game.grid = grid
    game.check_diagonal_win()

    assert game.result == expected_result


@pytest.mark.unit
@pytest.mark.parametrize("grid, expected_result", [
    (np.array([1, 0, 0, 0, 1, 0, 0, 0, 1]),
     {"p0": "X", "p1": "2", "p2": "3", "p3": "4", "p4": "X", "p5": "6", "p6": "7", "p7": "8", "p8": "X"}),
    (np.array([2, 0, 0, 0, 2, 0, 0, 0, 2]),
     {"p0": "O", "p1": "2", "p2": "3", "p3": "4", "p4": "O", "p5": "6", "p6": "7", "p7": "8", "p8": "O"}),
    (np.array([1, 2, 1, 2, 1, 2, 1, 2, 1]),
     {"p0": "X", "p1": "O", "p2": "X", "p3": "O", "p4": "X", "p5": "O", "p6": "X", "p7": "O", "p8": "X"})
])
def test_game_prints_correct_board(grid, expected_result):
    game = Game(CPUAgent(), CPUAgent())
    game.grid = grid

    printed_board = game.print_board()
    wrappers = {"X": "\x1b[31m", "O": "\x1b[36m"}

    for pos in printed_board.keys():
        wrapper_ascii = wrappers[expected_result[pos]]if expected_result[pos] in wrappers else "\x1b[32m"
        assert printed_board[pos] == f"{wrapper_ascii}{expected_result[pos]}\x1b[39m"
