import json
import random
from pathlib import Path

import numpy as np
from loguru import logger

from .markov_decision_process import TicTacToeMDP
from .state import State


class Agent:
    """
    Class modeling a player

    Attributes
    ----------
    grid: numpy.ndarray
        Representation of the board as an array of integers.
    current_state: ttt.models.State
        Current game state
    """

    def __init__(self):
        self.grid = None
        self.current_state = None

    def update_grid(self, grid: np.ndarray) -> None:
        """
        Updates `grid` and `current_state` with the given value.

        Parameters
        ----------
        grid: numpy.ndarray
            Representation of the board as an array of integers.
        """
        self.grid: np.ndarray = grid
        self.current_state: State = State(grid)


class CPUAgent(Agent):
    """
    Class modeling a CPU player.

    Attributes
    ----------
    mdp: ttt.models.TicTacToeMDP
        Representation of the game as a Markov Decision Process.
    """

    def __init__(self):
        super().__init__()
        self.mdp = TicTacToeMDP()

    def update_grid(self, grid: np.ndarray) -> None:
        """
        Updates `grid`, `current_state` and `mdp` with the given value.

        Parameters
        ----------
        grid: numpy.ndarray
            Representation of the board as an array of integers.
        """
        super().update_grid(grid)

        if not self.mdp.has_state(self.current_state):
            self.mdp.add_state(self.current_state)
        else:
            self.current_state = self.mdp.get_state(self.grid)

    def get_random_move(self) -> int:
        """
        Generates a random move.

        Returns
        -------
        move: int
        """
        number_of_possible_moves = len(self.current_state.next_states_transitions)
        return self.current_state.next_states_transitions[random.randint(0, number_of_possible_moves - 1)]

    def get_next_best_move(self) -> int:
        """
        Generates a new move using the previous knowledge.

        Returns
        -------
        move: int
        """
        return self.current_state.get_best_move()

    def serialize(self) -> dict:
        """
        Serializes this Agent into a dict.

        Returns
        -------
        serializable_dict: dict
        """

        return {
            "mdp": self.mdp.serialize()
        }

    def deserialize(self, json_data: dict) -> None:
        """
        Dumps specified `json_data` to the agent.

        Parameters
        ----------
        json_data: dict
            Dictionary with the following format: {mdp: dict}
        """

        mdp = TicTacToeMDP()
        mdp.deserialize(json_data["mdp"])
        self.mdp = mdp

        logger.debug(f"Loaded agent")

    def save(self, path: str) -> None:
        """
        Saves model's params as a JSON file.

        Parameters
        ----------
        path: str
            Where to save agent params.
        """

        with open(path, 'w') as fp:
            json.dump(self.serialize(), fp)

    def load(self, path: str) -> None:
        """
        Loads a JSON file containing agent's params.

        Parameters
        ----------
        path: str
            Path of the JSON file.
        """
        data = json.loads(Path(path).read_text())
        self.deserialize(data)


class HumanAgent(Agent):
    """
    Class modeling a human player.

    Attributes
    ----------
    grid: list
        Representation of the board as list of integers.
    """

    def __init__(self):
        super().__init__()

    def get_next_move(self) -> int:
        """
        Gets the user move.

        Returns
        -------
        move: int
        """
        possible_moves = [cell_id + 1 for cell_id in self.current_state.next_states_transitions]
        logger.info(f"Which cell do you want to mark? {possible_moves}: ")
        move = int(input())
        while move not in possible_moves:
            logger.info(f"The cell is already marked. Pleas, select another cell.\n\n"
                        f"Which cell do you want to mark? {possible_moves}: ")
            move = int(input())
        return move - 1
