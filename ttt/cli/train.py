import fire
from loguru import logger

from ttt.training import train


def train_agent(output_path: str, lr: float = 0.1, exploration_iterations: int = 2500,
                exploitation_iterations: int = 1500, exploration_exploitation_iterations: int = 1000):
    train(output_path, lr, exploration_iterations, exploitation_iterations, exploration_exploitation_iterations)


@logger.catch
def main():
    fire.Fire(train_agent)


if __name__ == "__main__":
    main()
