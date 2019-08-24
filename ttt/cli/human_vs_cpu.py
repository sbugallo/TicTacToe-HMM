import fire
from loguru import logger

from ttt.models import CPUAgent
from ttt.play import play_game_player_vs_comp


def play_human_vs_cpu(cpu_weights_path, cpu_mode) -> None:
    """

    Parameters
    ----------
    cpu_weights_path
    cpu_mode
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
