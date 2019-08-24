from loguru import logger

from .models import Game, HumanAgent
from .rewarding import rewarding


def play_game_cpu_vs_cpu(player_1, player_2, player_1_mode, player_2_mode, num_rounds, display_board=True,
                         display_text=True) -> Game:
    """

    Parameters
    ----------
    player_1
    player_2
    player_1_mode
    player_2_mode
    num_rounds
    display_board
    display_text

    Returns
    -------

    Raises
    ------
    AssertionError:

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
        else:
            player_2_victories += 1

    if display_text:
        if game.result > 0:
            logger.info("Player " + str(game.result) + " wins!")
        else:
            logger.info("It's a tie!")

        logger.info(f"\n\nScores: CPU1 {player_1_victories} - {player_2_victories} CPU2")

    return game


def play_game_player_vs_comp(cpu_player, cpu_player_mode) -> Game:
    """

    Parameters
    ----------
    cpu_player
    cpu_player_mode

    Returns
    -------

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
        else:
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
    """
    """

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
        else:
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


def play_game(game, player_1_move, player_2_move, start, display_board=True) -> Game:
    """

    Parameters
    ----------
    game
    player_1_move
    player_2_move
    start
    display_board

    Returns
    -------

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
