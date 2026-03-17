import json
from pathlib import Path

import pytest
import responses as resp_lib

from spacex_cli.api.client import SpaceXClient

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def launches_data():
    data = json.loads((FIXTURES / "launches_response.json").read_text())
    return data.get("results", [])


@pytest.fixture
def rockets_data():
    data = json.loads((FIXTURES / "rockets_response.json").read_text())
    return data.get("results", [])


@pytest.fixture
def capsules_data():
    data = json.loads((FIXTURES / "capsules_response.json").read_text())
    return data.get("results", [])


@pytest.fixture
def company_data():
    return json.loads((FIXTURES / "company_response.json").read_text())


@pytest.fixture
def single_launch_data(launches_data):
    return launches_data[0]


@pytest.fixture
def single_rocket_data(rockets_data):
    return rockets_data[0]


@pytest.fixture
def single_capsule_data(capsules_data):
    return capsules_data[0]
