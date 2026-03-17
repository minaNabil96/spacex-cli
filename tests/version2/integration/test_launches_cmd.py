import responses
from typer.testing import CliRunner
from spacex_cli.cli import app

runner = CliRunner()
BASE = "https://lldev.thespacedevs.com/2.2.0"


@responses.activate
def test_list_launches_json(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/", 
        json=launches_data, 
        match_querystring=False
    )
    result = runner.invoke(app, ["-o", "json", "launches", "list"])
    assert result.exit_code == 0
    assert "Falcon 9 Block 5 | Crew-1" in result.stdout


@responses.activate
def test_launch_info_not_found():
    responses.add(responses.GET, f"{BASE}/launch/bad-id/", status=404)
    result = runner.invoke(app, ["launches", "info", "bad-id"])
    assert result.exit_code == 1
    assert "Error:" in result.stdout
