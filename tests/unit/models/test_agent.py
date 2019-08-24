import random
import json
from pathlib import Path

import numpy as np
from numpy.testing import assert_array_equal

from ttt.models.agent import Agent, CPUAgent, HumanAgent


def deterministic_test(seed):
    """Function wrapper to set a fixed seed.
    Arguments
    ---------
    seed: int

    Returns
    -------
        func: callable
            A function wrapping the input function.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            np.random.seed(np.array(seed, dtype=np.int64))
            random.seed(seed)
            output = func(*args, **kwargs)
            return output

        return wrapper

    return decorator


def test_agent_correct_initialization():
    agent = Agent()

    assert agent.current_state is None
    assert agent.grid is None


def test_agent_updates_grid_correctly():
    agent = Agent()
    new_grid = np.array([1, 2, 1, 2, 1, 2, 1, 0, 0])
    agent.update_grid(new_grid)

    assert_array_equal(new_grid, agent.grid)
    assert_array_equal(new_grid, agent.current_state.grid)

    assert_array_equal(agent.current_state.next_states_values, np.array([0, 0]))
    assert_array_equal(agent.current_state.next_states_transitions, np.array([7, 8]))


def test_cpuagent_correct_initialization():
    agent = CPUAgent()

    assert agent.current_state is None
    assert agent.grid is None
    assert len(agent.mdp.states) == 0


def test_cpuagent_updates_grid_correctly():
    agent = CPUAgent()
    new_grid = np.array([1, 2, 1, 2, 1, 2, 1, 0, 0])
    agent.update_grid(new_grid)

    assert_array_equal(new_grid, agent.grid)
    assert_array_equal(new_grid, agent.current_state.grid)

    assert_array_equal(agent.current_state.next_states_values, np.array([0, 0]))
    assert_array_equal(agent.current_state.next_states_transitions, np.array([7, 8]))

    assert len(agent.mdp.states) == 1

    new_state = agent.mdp.states[0]
    assert_array_equal(new_grid, new_state.grid)
    assert_array_equal(new_state.next_states_values, np.array([0, 0]))
    assert_array_equal(new_state.next_states_transitions, np.array([7, 8]))


@deterministic_test(500)
def test_cpuagent_generates_random_moves():
    agent = CPUAgent()
    new_grid = np.array([1, 2, 1, 2, 1, 2, 1, 0, 0])
    agent.update_grid(new_grid)

    generated_moves = set()
    for _ in range(10):
        generated_moves.add(agent.get_random_move())

    assert len(generated_moves) == 2
    assert 7 in generated_moves
    assert 8 in generated_moves


def test_cpuagent_generates_best_move_correctly():
    agent = CPUAgent()
    new_grid = np.array([1, 2, 1, 2, 1, 2, 1, 0, 0])
    agent.update_grid(new_grid)

    agent.current_state.next_states_values = np.array([-1, 1])

    generated_moves = set()
    for _ in range(10):
        generated_moves.add(agent.get_next_best_move())

    assert len(generated_moves) == 1
    assert 7 not in generated_moves
    assert 8 in generated_moves


def test_cpuagent_serializes_correctly():
    serialized_agent = CPUAgent().serialize()

    assert "mdp" in serialized_agent
    assert "states" in serialized_agent["mdp"]
    assert len(serialized_agent["mdp"]["states"]) == 0


def test_cpuagent_deserializes_correctly():
    agent = CPUAgent()
    serialized_agent = {'mdp': {'states': {}}}
    agent.deserialize(serialized_agent)

    assert len(agent.mdp.states) == 0


def test_cpuagent_saves_correctly(tmpdir):
    root = Path(tmpdir)
    weights_path = root / "agent.json"

    CPUAgent().save(weights_path)

    assert weights_path.exists()
    serialized_agent = json.loads(weights_path.read_text())

    assert "mdp" in serialized_agent
    assert "states" in serialized_agent["mdp"]
    assert len(serialized_agent["mdp"]["states"]) == 0


def test_cpuagent_loads_correctly(tmpdir):
    root = Path(tmpdir)
    weights_path = root / "agent.json"

    agent = CPUAgent()
    weights_path.write_text('{"mdp": {"states": {}}}')
    agent.load(weights_path)

    assert len(agent.mdp.states) == 0


def test_humanagent_correct_initialization():
    agent = HumanAgent()

    assert agent.current_state is None
    assert agent.grid is None


def test_humanagent_updates_grid_correctly():
    agent = HumanAgent()
    new_grid = np.array([1, 2, 1, 2, 1, 2, 1, 0, 0])
    agent.update_grid(new_grid)

    assert_array_equal(new_grid, agent.grid)
    assert_array_equal(new_grid, agent.current_state.grid)

    assert_array_equal(agent.current_state.next_states_values, np.array([0, 0]))
    assert_array_equal(agent.current_state.next_states_transitions, np.array([7, 8]))