import fire
from loguru import logger

from ttt.training import train


def train_agent(output_path: str, lr: float = 0.1, exploration_iterations: int = int(25e4),
                exploitation_iterations: int = int(15e4), exploration_exploitation_iterations: int = int(10e4)):
    train(output_path, lr, exploration_iterations, exploitation_iterations, exploration_exploitation_iterations)


@logger.catch
def main():
    fire.Fire(train_agent)


if __name__ == "__main__":
    main()
