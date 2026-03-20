"""Integration tests for capsules commands (v2)."""

import responses
from typer.testing import CliRunner

from spacex_cli.cli import app

runner = CliRunner()
BASE = "https://lldev.thespacedevs.com/2.2.0"


@responses.activate
def test_list_capsules_table(capsules_data):
    responses.add(
        responses.GET, 
        f"{BASE}/config/spacecraft/", 
        json={"results": capsules_data, "count": len(capsules_data)}
    )
    result = runner.invoke(app, ["capsules", "list"])
    assert result.exit_code == 0


@responses.activate
def test_capsule_info(single_capsule_data):
    capsule_id = single_capsule_data["id"]
    responses.add(responses.GET, f"{BASE}/config/spacecraft/{capsule_id}/", json=single_capsule_data)
    result = runner.invoke(app, ["capsules", "info", str(capsule_id)])
    assert result.exit_code == 0
