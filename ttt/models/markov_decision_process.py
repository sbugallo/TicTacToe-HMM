from typing import Dict

import numpy as np
from loguru import logger

from .state import State


class TicTacToeMDP:
    """
    Class modeling a Markov Decision Process

    Attributes
    ----------
    states: dict
        Dict of states
    """

    def __init__(self):
        self.states: Dict[int, State] = {}

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

        for entry in self.states.values():
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
        self.states[len(self.states)] = State(state.grid)

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
        for state in self.states.values():
            if np.array_equal(grid, state.grid):
                return state

        raise ValueError(f"Grid {grid} could not be found in saved states "
                         f"{[state.grid for state in self.states.values()]}")

    def update_state(self, state: State) -> None:
        """
        Updates the MDPs state with the given one.

        Parameters
        ----------
        state: ttt.models.State
            State to update MDPs with.
        """

        for key, entry in self.states.items():
            if np.array_equal(state.grid, entry.grid):
                entry.next_states_values = state.next_states_values.copy()
                self.states[key] = entry

    def serialize(self) -> dict:
        """
        Serializes this MDP into a dict.

        Returns
        -------
        serializable_dict: dict
        """

        return {
            "states": {str(key): state.serialize() for key, state in self.states.items()}
        }

    def deserialize(self, json_data: dict) -> None:
        """
        Dumps specified `json_data` to the MDP.

        Parameters
        ----------
        json_data: dict
            Dictionary with the following format: {state_id (str): state (ttt.models.State)}
        """

        for key, serialized_state in json_data["states"].items():
            state = State()
            state.deserialize(serialized_state)
            self.states[int(key)] = state

        logger.debug(f"Loaded MDP: \n\tstates: {self.states}")
