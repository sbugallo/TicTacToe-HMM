import fire
from loguru import logger

from ttt.training import train


def train_agent(output_path: str, lr: float = 0.1, exploration_iterations: int = 2500,
                exploitation_iterations: int = 1500, exploration_exploitation_iterations: int = 1000):
    """
    Trains a new agent.

    Parameters
    ----------
    output_path: str
        Where to save agent's weights. E.g., weights.json.
    lr: float
        Learning rate.
    exploration_iterations: int
        Number of iterations during exploration phase.
    exploitation_iterations: int
        Number of iterations during exploitation phase.
    exploration_exploitation_iterations: int
        Number of iterations during exploration-exploitation phase.
    """
    train(output_path, lr, exploration_iterations, exploitation_iterations, exploration_exploitation_iterations)


@logger.catch
def main():
    fire.Fire(train_agent)


if __name__ == "__main__":
    main()
