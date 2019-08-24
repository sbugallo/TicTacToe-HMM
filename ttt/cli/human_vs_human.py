import fire
from loguru import logger

from ttt.play import play_game_player_vs_player


def play_human_vs_player() -> None:
    """Plays a game between 2 human players"""
    play_game_player_vs_player()


@logger.catch
def main():
    fire.Fire(play_human_vs_player)


if __name__ == "__main__":
    main()
