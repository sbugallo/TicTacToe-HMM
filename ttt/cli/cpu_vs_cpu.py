import fire
from loguru import logger

from ttt.models import CPUAgent
from ttt.play import play_game_cpu_vs_cpu


def play_cpu_vs_cpu(cpu_1_weights_path: str, cpu_1_mode: str, cpu_2_weights_path: str, cpu_2_mode: str, num_rounds: int,
                    display_board: bool = True, display_text: bool = True) -> None:
    """
    Plays a game between two cpu players.

    Parameters
    ----------
    cpu_1_weights_path: str
        Path to the JSON file with the first player's weights
    cpu_1_mode: str
        Player 1 policy. Whether best or random.
    cpu_2_weights_path: str
        Path to the JSON file with the second player's weights
    cpu_2_mode: str
        Player 1 policy. Whether best or random.
    num_rounds: int
        Number or rounds to be played.
    display_board: bool
        Whether to display the board after each move.
    display_text: bool
        Whether to display game information
    """

    cpu_1_agent = CPUAgent()
    cpu_2_agent = CPUAgent()

    cpu_1_agent.load(cpu_1_weights_path)
    cpu_2_agent.load(cpu_2_weights_path)

    play_game_cpu_vs_cpu(cpu_1_agent, cpu_2_agent, cpu_1_mode, cpu_2_mode, num_rounds, display_board, display_text)


@logger.catch
def main():
    fire.Fire(play_game_cpu_vs_cpu)


if __name__ == "__main__":
    main()
