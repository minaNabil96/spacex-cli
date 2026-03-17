"""Shared API response helpers for tests."""

import json
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent


def load_fixture(name: str) -> list | dict:
    """Load a JSON fixture by filename."""
    return json.loads((FIXTURES_DIR / name).read_text())


# Pre-loaded fixtures for convenience
LAUNCHES = load_fixture("launches_response.json")
ROCKETS = load_fixture("rockets_response.json")
CAPSULES = load_fixture("capsules_response.json")
COMPANY = load_fixture("company_response.json")
