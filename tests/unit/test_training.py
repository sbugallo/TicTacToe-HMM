from pathlib import Path

import pytest

import ttt.training
from ttt.models import CPUAgent
from ttt.training import train, _run_simulation


@pytest.mark.unit
@pytest.mark.parametrize("num_iterations", [1, 10, 100])
def test_run_simulation_runs_correct_number_of_iterations(mocker, num_iterations):
    cpu_agent = CPUAgent()

    mocker.spy(ttt.training, "rewarding")
    mocker.spy(ttt.training, "play_game_cpu_vs_cpu")
    _run_simulation(num_iterations, cpu_agent, "best", "random", 0.1)

    assert ttt.training.rewarding.call_count == num_iterations * 2
    assert ttt.training.play_game_cpu_vs_cpu.call_count == num_iterations


@pytest.mark.unit
def test_train_runs_3_training_phases(mocker, tmpdir):
    output_path = Path(tmpdir) / "output.json"

    mocker.spy(ttt.training, "_run_simulation")
    with mocker.patch('ttt.training._run_simulation'):
        train(str(output_path.absolute()))

        assert ttt.training._run_simulation.call_count == 3


@pytest.mark.unit
def test_train_saves_agent(tmpdir):
    output_path = Path(tmpdir) / "output.json"
    train(str(output_path.absolute()), exploration_iterations=1, exploitation_iterations=1,
          exploration_exploitation_iterations=1)
    assert output_path.exists()


@pytest.mark.unit
def test_train_returns_agent(tmpdir):
    output_path = Path(tmpdir) / "output.json"
    agent = train(str(output_path.absolute()), exploration_iterations=1, exploitation_iterations=1,
                  exploration_exploitation_iterations=1)
    assert isinstance(agent, CPUAgent)
