import pytest
from pathlib import Path

BASE_PATH = Path(__file__).parent
OUTPUT_PATH = BASE_PATH / "output"

pytest_plugins = "pytester"


@pytest.fixture
def expected_output():
    def _(file_name):
        path = OUTPUT_PATH / file_name
        with path.open() as file:
            return file.read()

    return _
