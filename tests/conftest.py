from pathlib import Path

import pytest

tests_path = Path(__file__).parent.absolute()


@pytest.fixture
def data_path():
    return tests_path / "data"
