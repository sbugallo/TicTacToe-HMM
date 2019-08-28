import json
import random
from pathlib import Path
from typing import List

import numpy as np
from loguru import logger

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
    states: list
        List of states. Representation of the game as a Markov Decision Process.
    """

    def __init__(self):
        super().__init__()
        self.states: List[State] = []

    def update_grid(self, grid: np.ndarray) -> None:
        """
        Updates `grid`, `current_state` and `mdp` with the given value.

        Parameters
        ----------
        grid: numpy.ndarray
            Representation of the board as an array of integers.
        """
        super().update_grid(grid)

        if not self.has_state(self.current_state):
            self.add_state(self.current_state)
        else:
            # Overwrite new State with the saved one
            self.current_state = self.get_state(self.grid)

    def get_random_move(self) -> int:
        """
        Generates a random move.

        Returns
        -------
        move: int
        """
        number_of_possible_moves = len(self.current_state.next_states_transitions)
        return self.current_state.next_states_transitions[random.randint(0, number_of_possible_moves - 1)]

    def get_best_move(self) -> int:
        """
        Generates a new move using the previous knowledge.

        Returns
        -------
        move: int
        """
        return self.current_state.get_best_move()

    def has_state(self, state: State) -> bool:
        """
        Checks if MDP has registered the given state
        Parameters
        ----------
        state: ttt.models.State
            State to be checked

        Returns
        -------
        is_registered: bool
        """

        for entry in self.states:
            if np.array_equal(state.grid, entry.grid):
                return True

        return False

    def add_state(self, state: State) -> None:
        """
        Adds the given state to the MDP.

        Parameters
        ----------
        state: ttt.models.State
            State to be added.
        """
        self.states.append(State(state.grid))

    def get_state(self, grid: np.ndarray) -> State:
        """
        Gets the state with the given grid.

        Parameters
        ----------
        grid: numpy.ndarray
            Representation of the board.

        Returns
        -------
        state: ttt.models.State
            State containing the given grid.
        """
        for state in self.states:
            if np.array_equal(grid, state.grid):
                return state

        raise ValueError(f"Grid {grid} could not be found in saved states "
                         f"{[state.grid for state in self.states]}")

    def update_state(self, state: State) -> None:
        """
        Updates the MDPs state with the given one.

        Parameters
        ----------
        state: ttt.models.State
            State to update MDPs with.
        """

        for index, entry in enumerate(self.states):
            if np.array_equal(state.grid, entry.grid):
                entry.next_states_values = state.next_states_values.copy()
                self.states[index] = entry

    def serialize(self) -> dict:
        """
        Serializes this Agent into a dict.

        Returns
        -------
        serializable_dict: dict
        """

        return {
            "states": [state.serialize() for state in self.states]
        }

    def deserialize(self, json_data: dict) -> None:
        """
        Dumps specified `json_data` to the agent.

        Parameters
        ----------
        json_data: dict
            Dictionary with the following format: {mdp: dict}
        """

        for serialized_state in json_data["states"]:
            state = State()
            state.deserialize(serialized_state)
            self.states.append(state)

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
