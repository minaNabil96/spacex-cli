"""Integration tests for export commands (v2)."""

import responses
from typer.testing import CliRunner
import os

from spacex_cli.cli import app

runner = CliRunner()
BASE = "https://lldev.thespacedevs.com/2.2.0"


@responses.activate
def test_export_launches_json(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/", 
        json=launches_data
    )
    dest = "test_export.json"
    try:
        result = runner.invoke(app, ["export", "launches", "--dest", dest, "--format", "json"])
        assert result.exit_code == 0
        assert os.path.exists(dest)
    finally:
        if os.path.exists(dest):
            os.remove(dest)


@responses.activate
def test_export_launches_csv(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/", 
        json=launches_data
    )
    dest = "test_export.csv"
    try:
        result = runner.invoke(app, ["export", "launches", "--dest", dest, "--format", "csv"])
        assert result.exit_code == 0
        assert os.path.exists(dest)
    finally:
        if os.path.exists(dest):
            os.remove(dest)
