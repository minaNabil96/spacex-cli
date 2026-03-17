"""Integration tests for launches commands."""

import responses
from typer.testing import CliRunner

from spacex_cli.cli import app

runner = CliRunner()
BASE = "https://lldev.thespacedevs.com/2.2.0"


@responses.activate
def test_list_launches_table(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/", 
        json={"results": launches_data, "count": len(launches_data)}
    )
    result = runner.invoke(app, ["launches", "list", "--limit", "2"])
    assert result.exit_code == 0


@responses.activate
def test_list_launches_json(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/", 
        json={"results": launches_data, "count": len(launches_data)}
    )
    result = runner.invoke(app, ["-o", "json", "launches", "list"])
    assert result.exit_code == 0


@responses.activate
def test_list_launches_json_pretty(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/", 
        json={"results": launches_data, "count": len(launches_data)}
    )
    result = runner.invoke(app, ["-o", "json-pretty", "launches", "list"])
    assert result.exit_code == 0


@responses.activate
def test_list_launches_upcoming(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/upcoming/", 
        json={"results": launches_data, "count": len(launches_data)}
    )
    result = runner.invoke(app, ["launches", "list", "--upcoming"])
    assert result.exit_code == 0


@responses.activate
def test_list_launches_past(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/previous/", 
        json={"results": launches_data, "count": len(launches_data)}
    )
    result = runner.invoke(app, ["launches", "list", "--past"])
    assert result.exit_code == 0


@responses.activate
def test_launch_info(single_launch_data):
    launch_id = single_launch_data["id"]
    responses.add(responses.GET, f"{BASE}/launch/{launch_id}/", json=single_launch_data)
    result = runner.invoke(app, ["launches", "info", launch_id])
    assert result.exit_code == 0


@responses.activate
def test_launch_info_not_found():
    responses.add(responses.GET, f"{BASE}/launch/bad-id/", status=404)
    result = runner.invoke(app, ["launches", "info", "bad-id"])
    assert result.exit_code == 1


@responses.activate
def test_launch_info_json(single_launch_data):
    launch_id = single_launch_data["id"]
    responses.add(responses.GET, f"{BASE}/launch/{launch_id}/", json=single_launch_data)
    result = runner.invoke(app, ["-o", "json", "launches", "info", launch_id])
    assert result.exit_code == 0
