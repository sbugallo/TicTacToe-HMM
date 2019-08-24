from pathlib import Path

from loguru import logger

from .models import CPUAgent
from .play import play_game_cpu_vs_cpu
from .rewarding import rewarding


def _run_simulation(iterations: int, cpu_agent: CPUAgent, mode_1: str, mode_2: str, lr: float) -> CPUAgent:
    """
    Runs a set of games with the given parameters.

    Parameters
    ----------
    iterations: int
        Number of games to be played.
    cpu_agent: ttt.models.CPUAgent
        Agent to be trained.
    mode_1: str
        Policy of player 1. Possible values: best or random
    mode_2
        Policy of player 2. Possible values: best or random
    lr: float
        Learning rate.

    Returns
    -------
    trained_agent: ttt.models.CPUAgent
        Agent with its weights updated with training results.
    """
    for i in range(iterations):
        logger.info(f"\t\t{i}/{iterations}")
        game = play_game_cpu_vs_cpu(cpu_agent, cpu_agent, mode_1, mode_2, 1, False, False)
        rewarding(game, 1, lr)
        cpu_agent = rewarding(game, 2, lr)

    return cpu_agent


def train(output_path: str, lr: float = 0.1, exploration_iterations: int = 2500, exploitation_iterations: int = 1500,
          exploration_exploitation_iterations: int = 1000) -> CPUAgent:
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

    Returns
    -------
    cpu_agent: ttt.models.CPUAgent
    """

    cpu_agent = CPUAgent()

    logger.info("Starting CPU training")

    logger.info("\tRunning exploration")
    cpu_agent = _run_simulation(exploration_iterations, cpu_agent, "random", "random", lr)

    logger.info("\tRunning exploitation")
    cpu_agent = _run_simulation(exploitation_iterations, cpu_agent, "best", "best", lr)

    logger.info("\tRunning exploration-exploitation")
    cpu_agent = _run_simulation(exploration_exploitation_iterations, cpu_agent, "best", "random", lr)

    output_path = Path(output_path).absolute()
    logger.info(f"\tFinished. Saving agent to {output_path}")
    cpu_agent.save(output_path)

    return cpu_agent
