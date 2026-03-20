import json
from pathlib import Path

import pytest
from rich.console import Console
import spacex_cli.utils.console


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def launches_data():
    return json.loads((FIXTURES / "launches_response.json").read_text())


@pytest.fixture
def rockets_data():
    data = json.loads((FIXTURES / "rockets_response.json").read_text())
    return data["results"]


@pytest.fixture
def single_rocket_data(rockets_data):
    return rockets_data[0]


@pytest.fixture
def capsules_data():
    data = json.loads((FIXTURES / "capsules_response.json").read_text())
    return data["results"]


@pytest.fixture
def single_capsule_data(capsules_data):
    return capsules_data[0]


@pytest.fixture
def company_data():
    return json.loads((FIXTURES / "company_response.json").read_text())


@pytest.fixture(autouse=True)
def reset_consoles():
    # Force rich consoles to use current sys.stdout/stderr during tests
    spacex_cli.utils.console.console = Console()
    spacex_cli.utils.console.out_console = Console()
    spacex_cli.utils.console.error_console = Console(stderr=True)


@pytest.fixture
def launches_data():
    return json.loads((FIXTURES / "launches_response.json").read_text())
