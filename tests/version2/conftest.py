import json
from pathlib import Path

import pytest


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def launches_data():
    return json.loads((FIXTURES / "launches_response.json").read_text())


@pytest.fixture
def rockets_data():
    return json.loads((FIXTURES / "rockets_response.json").read_text())


@pytest.fixture
def capsules_data():
    return json.loads((FIXTURES / "capsules_response.json").read_text())


@pytest.fixture
def company_data():
    return json.loads((FIXTURES / "company_response.json").read_text())
