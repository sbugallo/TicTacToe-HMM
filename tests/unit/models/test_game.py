from ttt.models import Game, CPUAgent, HumanAgent
from numpy.testing import assert_array_equal
import numpy as np
import pytest


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


@pytest.mark.parametrize("move, player_id, expected_result", [
    (1, 1, np.array([0, 1, 0, 0, 0, 0, 0, 0, 0])),
    (8, 2, np.array([0, 0, 0, 0, 0, 0, 0, 0, 2])),
])
def test_game_applies_move_correctly(move, player_id, expected_result):
    game = Game(CPUAgent(), CPUAgent())
    game.apply_move(move, player_id)
    assert_array_equal(game.grid, expected_result)


@pytest.mark.parametrize("grid, move, player_id, expected_result", [
    (np.array([1, 1, 0, 0, 0, 0, 0, 0, 0]), 2, 1, 1),
    (np.array([2, 2, 0, 0, 0, 0, 0, 0, 0]), 2, 2, 2),
    (np.array([1, 1, 0, 0, 0, 0, 0, 0, 0]), 3, 1, -1),
    (np.array([1, 0, 0, 1, 0, 0, 0, 0, 0]), 6, 1, 1),
    (np.array([2, 0, 0, 2, 0, 0, 0, 0, 0]), 6, 2, 2),
    (np.array([1, 0, 0, 1, 0, 0, 0, 0, 0]), 7, 1, -1),
    (np.array([1, 0, 0, 0, 1, 0, 0, 0, 0]), 8, 1, 1),
    (np.array([2, 0, 0, 0, 2, 0, 0, 0, 0]), 8, 2, 2),
    (np.array([1, 0, 0, 0, 1, 0, 0, 0, 0]), 7, 1, -1)
])
def test_game_detects_victory_correctly(grid, move, player_id, expected_result):
    game = Game(CPUAgent(), CPUAgent())
    game.grid = grid
    game.apply_move(move, player_id)
    assert game.result == expected_result


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


def test_game_traces_game_sequence_correctly():
    game = Game(CPUAgent(), CPUAgent())
    game.apply_move(0, 1)
    game.apply_move(1, 2)
    game.apply_move(2, 2)
    game.apply_move(3, 2)
    game.apply_move(4, 2)
    game.apply_move(5, 1)
    game.apply_move(6, 1)
    game.apply_move(7, 1)
    game.apply_move(8, 2)

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