import fire
from loguru import logger

from ttt.models import CPUAgent
from ttt.play import play_game_player_vs_comp


def play_human_vs_cpu(cpu_weights_path: str, cpu_mode: str) -> None:
    """
    Plays a game between a human player and a CPU agent.

    Parameters
    ----------
    cpu_weights_path: str
        Path to the JSON file with the first player's weights
    cpu_mode: str
        Player 1 policy. Whether best or random.
    """

    assert cpu_mode in {"random", "best"}

    cpu_agent = CPUAgent()
    cpu_agent.load(cpu_weights_path)

    play_game_player_vs_comp(cpu_agent, cpu_mode)


@logger.catch
def main():
    fire.Fire(play_human_vs_cpu)


if __name__ == "__main__":
    main()
