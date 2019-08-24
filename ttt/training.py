from pathlib import Path

from loguru import logger

from .models import CPUAgent
from .play import play_game_cpu_vs_cpu
from .rewarding import rewarding


def _run_simulation(iterations: int, cpu_agent: CPUAgent, mode_1: str, mode_2: str, lr: float) -> CPUAgent:
    for i in range(iterations):
        logger.info(f"\t\t{i}/{iterations}")
        game = play_game_cpu_vs_cpu(cpu_agent, cpu_agent, mode_1, mode_2, 1, False, False)
        rewarding(game, 1, lr)
        cpu_agent = rewarding(game, 2, lr)

    return cpu_agent


def train(output_path: str, lr: float = 0.1, exploration_iterations: int = 2500, exploitation_iterations: int = 1500,
          exploration_exploitation_iterations: int = 1000) -> CPUAgent:
    """

    Parameters
    ----------
    output_path
    lr
    exploration_iterations
    exploitation_iterations
    exploration_exploitation_iterations

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
