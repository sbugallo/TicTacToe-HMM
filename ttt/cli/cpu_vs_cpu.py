import fire
from loguru import logger

from ttt.models import CPUAgent
from ttt.play import play_game_cpu_vs_cpu


def play_cpu_vs_cpu(cpu_1_weights_path, cpu_1_mode, cpu_2_weights_path, cpu_2_mode, num_rounds, display_board=True,
                    display_text=True) -> None:
    """

    Parameters
    ----------
    cpu_1_weights_path
    cpu_1_mode
    cpu_2_weights_path
    cpu_2_mode
    num_rounds
    display_board
    display_text
    """

    cpu_1_agent = CPUAgent()
    cpu_2_agent = CPUAgent()

    cpu_1_agent.load(cpu_1_weights_path)
    cpu_2_agent.load(cpu_2_weights_path)

    play_game_cpu_vs_cpu(cpu_1_agent, cpu_2_agent, cpu_1_mode, cpu_2_mode, num_rounds, display_board)


@logger.catch
def main():
    fire.Fire(play_game_cpu_vs_cpu)


if __name__ == "__main__":
    main()
