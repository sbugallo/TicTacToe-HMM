import numpy as np

from .models import Game, CPUAgent, State, Action, Reward


def get_move(state_1: State, state_2: State) -> Action:
    """
    Returns the move applied to go from `state_1` to `state_2`.

    Parameters
    ----------
    state_1: ttt.models.State
        Grid representation.
    state_2: ttt.models.State
        Grid representation.

    Returns
    -------
    move: ttt.models.Action
        Move applied to go from `state_1` to `state_2`.
    """

    diff = state_1.grid - state_2.grid

    diff_idx = np.nonzero(diff)[0]
    if len(diff_idx) != 1:
        raise ValueError(f"Cannot go from state_1 {state_1.grid} to state_2 {state_2.grid}")

    return Action(diff_idx[0])


def rewarding(game: Game, player_number: int, lr: float) -> CPUAgent:
    """
    Reads the sequence of states the completed game has.

    Parameters
    ----------
    game: ttt.models.Game
        Game that was played.
    player_number: int
        Player to be rewarded.
    lr: float
        Learning rate.

    Returns
    -------
    cpu_agent: ttt.models.CPUAgent
        Agent with its weights updated with games' results.
    """

    assert player_number in {1, 2}

    cpu_agent = game.player_1 if player_number == 1 else game.player_2

    for i, current_state in enumerate(game.game_sequence):

        if i == len(game.game_sequence) - 1:
            break

        agent_current_state = cpu_agent.get_state(current_state)
        agent_next_state = cpu_agent.get_state(game.game_sequence[i + 1])
        move = get_move(agent_current_state, agent_next_state)

        if agent_next_state.grid[move.value] != player_number:
            continue

        if game.result > 0:

            # Win -> positive reward
            if game.result == player_number:
                agent_current_state.update_transition_weight(move, Reward.win(i, lr))

            # Lose -> negative reward
            else:
                agent_current_state.update_transition_weight(move, Reward.defeat(i, lr))

        # Tie -> small positive reward
        else:
            agent_current_state.update_transition_weight(move, Reward.tie(i, lr))

        cpu_agent.update_state(agent_current_state)

    return cpu_agent
