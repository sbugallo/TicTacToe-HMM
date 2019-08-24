import numpy as np


class State:
    """
    Class modelling the states of the game

    Parameters
    ----------
    grid: numpy.ndarray
        Representation of the board.

    Attributes
    ----------
    grid: numpy.ndarray
        Representation of the board.
    next_states_values: numpy.ndarray
        The weight of the transition to a state.
    next_states_transitions: numpy.ndarray
        The next move to move to the next state.
    """

    def __init__(self, grid: np.ndarray = None) -> None:
        if grid is not None:
            self.grid = grid
            self._compute_next_states()

        else:
            self.grid = None
            self.next_states_values = None
            self.next_states_transitions = None

    def _compute_next_states(self) -> None:
        """Computes all possible next states (grids) alongside the related move and weights (equals)"""
        self.next_states_transitions = np.where(self.grid == 0)[0]
        self.next_states_values = np.zeros(self.next_states_transitions.shape)

    def update_transition_weight(self, transition, increase):
        idx = np.where(self.next_states_transitions == transition)[0][0]
        self.next_states_values[idx] += increase

    def serialize(self) -> dict:
        """
        Serializes this State into a dict.

        Returns
        -------
        serializable_dict: dict
        """

        return {
            "grid": self.grid.tolist(),
            "next_states_values": self.next_states_values.tolist(),
            "next_states_transitions": self.next_states_transitions.tolist()
        }

    def deserialize(self, json_data: dict) -> None:
        """
        Dumps specified `json_data` to the state.

        Parameters
        ----------
        json_data: dict
            Dictionary with the following format: {grid: list, next_state_values: list, next_state_transitions: list}
        """
        self.grid = np.array(json_data["grid"])
        self.next_states_values = np.array(json_data["next_states_values"])
        self.next_states_transitions = np.array(json_data["next_states_transitions"])

    def get_best_move(self) -> int:
        """Decides on the best available move based on the transition weights."""
        return self.next_states_transitions[self.next_states_values.argmax()]
