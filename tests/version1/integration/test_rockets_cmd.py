"""Integration tests for rockets commands."""

import responses
from typer.testing import CliRunner

from spacex_cli.cli import app

runner = CliRunner()
BASE = "https://lldev.thespacedevs.com/2.2.0"


@responses.activate
def test_list_rockets_table(rockets_data):
    responses.add(
        responses.GET, 
        f"{BASE}/config/launcher/", 
        json={"results": rockets_data, "count": len(rockets_data)}
    )
    result = runner.invoke(app, ["rockets", "list"])
    assert result.exit_code == 0


@responses.activate
def test_list_rockets_json(rockets_data):
    responses.add(
        responses.GET, 
        f"{BASE}/config/launcher/", 
        json={"results": rockets_data, "count": len(rockets_data)}
    )
    result = runner.invoke(app, ["-o", "json", "rockets", "list"])
    assert result.exit_code == 0


@responses.activate
def test_rocket_info(single_rocket_data):
    rocket_id = single_rocket_data["id"]
    responses.add(responses.GET, f"{BASE}/config/launcher/{rocket_id}/", json=single_rocket_data)
    result = runner.invoke(app, ["rockets", "info", str(rocket_id)])
    assert result.exit_code == 0


@responses.activate
def test_rocket_info_not_found():
    responses.add(responses.GET, f"{BASE}/config/launcher/bad-id/", status=404)
    result = runner.invoke(app, ["rockets", "info", "bad-id"])
    assert result.exit_code == 1


@responses.activate
def test_rocket_info_json(single_rocket_data):
    rocket_id = single_rocket_data["id"]
    responses.add(responses.GET, f"{BASE}/config/launcher/{rocket_id}/", json=single_rocket_data)
    result = runner.invoke(app, ["-o", "json-pretty", "rockets", "info", str(rocket_id)])
    assert result.exit_code == 0
