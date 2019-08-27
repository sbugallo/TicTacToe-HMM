import numpy as np
from loguru import logger

from .agent import Agent


class Game:
    """
    Class modeling.

    Attributes
    ----------
    grid: numpy.ndarray
    player_1: ttt.models.Agent
    player_2: ttt.models.Agent
    result: int
    grid_is_full: bool
    game_sequence: list

    Parameters
    ----------
    player_1: ttt.models.Agent
    player_2: ttt.models.Agent
    """

    def __init__(self, player_1: Agent, player_2: Agent) -> None:
        self.grid = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])

        self.result = -1
        self.grid_is_full = False

        self.player_1 = player_1
        self.player_2 = player_2

        self.player_1.update_grid(self.grid.copy())
        self.player_2.update_grid(self.grid.copy())

        self.game_sequence = [self.grid.copy()]

    def apply_move(self, move: int, player_id: int) -> None:
        """
        Commits the move over the board.

        Parameters
        ----------
        move: int
            Cell to mark.
        player_id: int
            Value to apply.
        """

        self.grid[move] = int(player_id)

        self.player_1.update_grid(self.grid.copy())
        self.player_2.update_grid(self.grid.copy())

        self.check_victory()
        self.check_if_grid_is_full()

        self.game_sequence.append(self.grid.copy())

    def check_horizontal_win(self) -> None:
        """Checks if there is 3 consecutives marks of the same player horizontally."""

        if self.grid[0] == self.grid[1] == self.grid[2] and self.grid[2] != 0:
            self.result = self.grid[0]
        if self.grid[3] == self.grid[4] == self.grid[5] and self.grid[5] != 0:
            self.result = self.grid[3]
        if self.grid[6] == self.grid[7] == self.grid[8] and self.grid[8] != 0:
            self.result = self.grid[6]

    def check_vertical_win(self) -> None:
        """Checks if there is 3 consecutives marks of the same player vertically."""

        if self.grid[0] == self.grid[3] == self.grid[6] and self.grid[6] != 0:
            self.result = self.grid[0]
        if self.grid[1] == self.grid[4] == self.grid[7] and self.grid[7] != 0:
            self.result = self.grid[1]
        if self.grid[2] == self.grid[5] == self.grid[8] and self.grid[8] != 0:
            self.result = self.grid[2]

    def check_diagonal_win(self) -> None:
        """Checks if there is 3 consecutives marks of the same player diagonally"""

        if self.grid[0] == self.grid[4] == self.grid[8] and self.grid[8] != 0:
            self.result = self.grid[0]
        if self.grid[2] == self.grid[4] == self.grid[6] and self.grid[6] != 0:
            self.result = self.grid[2]

    def check_if_grid_is_full(self) -> None:
        """Checks if there is no more possible move."""

        count = 9 - np.count_nonzero(self.grid)

        if count == 0:
            self.grid_is_full = True
            if self.result < 0:
                self.result = 0

    def check_victory(self) -> None:
        """Checks if there is 3 consecutives marks of the same player."""

        self.check_horizontal_win()
        self.check_vertical_win()
        self.check_diagonal_win()

    def print_board(self) -> dict:
        """Displays the current grid."""

        positions = {}
        for index, value in enumerate(self.grid):
            if value == 1:
                mark = "X"
            elif value == 2:
                mark = "O"
            else:
                mark = f"{index + 1}"

            positions[f"p{index}"] = mark

        logger.info("""
                      {p0} | {p1} | {p2}
                     -----------
                      {p3} | {p4} | {p5}
                     -----------
                      {p6} | {p7} | {p8}
                    """.format(**positions))

        return positions
