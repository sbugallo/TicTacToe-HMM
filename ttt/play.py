from loguru import logger
from typing import Callable
from .models import Game, HumanAgent, CPUAgent
from .rewarding import rewarding


def play_game_cpu_vs_cpu(player_1: CPUAgent, player_2: CPUAgent, player_1_mode: str, player_2_mode: str,
                         num_rounds: int, display_board: bool = True, display_text: bool = True) -> Game:
    """
    Plays a game between two cpu players.

    Parameters
    ----------
    player_1: ttt.models.CPUAgent
    player_2: ttt.models.CPUAgent
    player_1_mode: str
        Whether best or random.
    player_2_mode: str
        Whether best or random.
    num_rounds: int
        Number or rounds to be played.
    display_board: bool
        Whether to display the board after each move.
    display_text: bool
        Whether to display game information

    Returns
    -------
    played_game: ttt.models.Game

    Raises
    ------
    AssertionError: if `num_rounds` < 1
    """

    assert num_rounds > 0

    player_1_move = player_1.get_random_move if player_1_mode == 'random' else player_1.get_next_best_move
    player_2_move = player_2.get_random_move if player_2_mode == 'random' else player_2.get_next_best_move

    player_1_victories = 0
    player_2_victories = 0

    start = -1

    for _ in range(num_rounds):
        start = (start + 1) % 2
        game = play_game(Game(player_1, player_2), player_1_move, player_2_move, start, display_board)

        if game.result == 1:
            player_1_victories += 1
        elif game.result == 2:
            player_2_victories += 1

        if display_text:
            if game.result > 0:
                logger.info("Player " + str(game.result) + " wins!")
            else:
                logger.info("It's a tie!")

    if display_text:
        logger.info(f"\n\nScores: CPU1 {player_1_victories} - {player_2_victories} CPU2")

    return game


def play_game_player_vs_comp(cpu_player: CPUAgent, cpu_player_mode: str) -> Game:
    """
    Plays a game between a human player and a CPU agent.

    Parameters
    ----------
    cpu_player: ttt.models.CPUAgent
    cpu_player_mode: str
        Whether best or random.

    Returns
    -------
    played_game: ttt.models.Game
    """

    human_player = HumanAgent()
    cpu_player_move = cpu_player.get_random_move if cpu_player_mode == 'random' else cpu_player.get_next_best_move

    human_player_victories = 0
    cpu_player_victories = 0

    start = -1

    while True:
        start = (start + 1) % 2
        game = play_game(Game(human_player, cpu_player), human_player.get_next_move, cpu_player_move, start)

        if game.result == 1:
            human_player_victories += 1
        elif game.result == 2:
            cpu_player_victories += 1

        if game.result == 1:
            logger.info("Player wins!")
        elif game.result == 2:
            logger.info("CPU wins!")
        else:
            logger.info("It's a tie!")

        next_round = -1
        while next_round not in {1, 2}:
            logger.info("Do you want to play another round?\n\t1. Yes\n\t2. No\n")
            next_round = int(input())

        if next_round == 2:
            break

        cpu_player = rewarding(game, 2, 0.6)

    logger.info(f"Scores: PLAYER {human_player_victories} - {cpu_player_victories} CPU")

    return game


def play_game_player_vs_player() -> None:
    """Plays a game between 2 human players"""

    player_1 = HumanAgent()
    player_2 = HumanAgent()

    player_1_victories = 0
    player_2_victories = 0

    start = -1

    while True:
        start = (start + 1) % 2
        game = play_game(Game(player_1, player_2), player_1.get_next_move, player_2.get_next_move(), start)

        if game.result == 1:
            player_1_victories += 1
        elif game.result == 2:
            player_2_victories += 1

        if game.result == 1:
            logger.info("Player 1 wins!")
        elif game.result == 2:
            logger.info("Player 2 wins!")
        else:
            logger.info("It's a tie!")

        next_round = -1
        while next_round not in {1, 2}:
            logger.info("Do you want to play another round?\n\t1. Yes\n\t2. No\n")
            next_round = int(input())

        if next_round == 2:
            break

    logger.info(f"Scores: PLAYER1 {player_1_victories} - {player_2_victories} PLAYER2")
    return


def play_game(game: Game, player_1_move: Callable, player_2_move: Callable, start: int,
              display_board: bool = True) -> Game:
    """
    Runs 1 round of a game.

    Parameters
    ----------
    game: ttt.models.Game
        Game to be played.
    player_1_move: method
        Player's method that computes the next move.
    player_2_move: method
        Player's method that computes the next move.
    start: int
        Which player will start.
    display_board: bool
        Whether to display the board after each move or not.

    Returns
    -------
    played_game: ttt.models.Game
    """

    if start == 0:
        order = {
            'first': {"player_id": 1, "move": player_1_move},
            'second': {"player_id": 2, "move": player_2_move}
        }
    else:
        order = {
            'first': {"player_id": 2, "move": player_2_move},
            'second': {"player_id": 1, "move": player_1_move}
        }

    while game.result < 0:  # continue till outcome of game is not decided
        if display_board:
            game.print_board()

        move1 = order["first"]["move"]()
        game.apply_move(move1, order["first"]["player_id"])

        if display_board:
            game.print_board()

        if game.result >= 0:
            break

        move2 = order["second"]["move"]()
        game.apply_move(move2, order["second"]["player_id"])

    if display_board:
        game.print_board()

    return game
