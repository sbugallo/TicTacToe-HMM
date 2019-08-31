import math


class Reward:
    """Models all possible rewards."""

    @staticmethod
    def win(i, lr):
        """
        Computes the reward for a given state when the result was a win.

        Parameters
        ----------
        i: int
            Position in which the state was reached
        lr: float
            Learning rate

        Returns
        -------
        reward: float
        """
        return math.exp(-(i + 1)) * lr

    @staticmethod
    def defeat(i, lr):
        """
        Computes the reward for a given state when the result was a defeat.

        Parameters
        ----------
        i: int
            Position in which the state was reached
        lr: float
            Learning rate

        Returns
        -------
        reward: float
        """
        return -(math.exp(-(i + 1))) * lr / 2

    @staticmethod
    def tie(i, lr):
        """
        Computes the reward for a given state when the result was a tie.

        Parameters
        ----------
        i: int
            Position in which the state was reached
        lr: float
            Learning rate

        Returns
        -------
        reward: float
        """
        return -(math.exp(-(i + 1))) * lr / 10
