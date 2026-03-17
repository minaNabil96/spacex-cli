import responses
from typer.testing import CliRunner
from spacex_cli.cli import app

runner = CliRunner()


@responses.activate
def test_launches_list_command(launches_data):
    responses.add(
        responses.GET,
        "https://lldev.thespacedevs.com/2.2.0/launch/",
        json=launches_data,
        status=200,
        match_querystring=False
    )
    
    result = runner.invoke(app, ["launches", "list"])
    assert result.exit_code == 0
    # No longer using stderr for tables, so this should work
    assert "\U0001f680 SpaceX Launches" in result.stdout


@responses.activate
def test_company_info_command(company_data):
    responses.add(
        responses.GET,
        "https://lldev.thespacedevs.com/2.2.0/agencies/121/",
        json=company_data,
        status=200
    )
    
    result = runner.invoke(app, ["company", "info"])
    assert result.exit_code == 0
    assert "🏢 SpaceX Company Info" in result.stdout
