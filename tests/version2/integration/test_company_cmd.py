"""Integration tests for company commands (v2)."""

import responses
from typer.testing import CliRunner

from spacex_cli.cli import app

runner = CliRunner()
BASE = "https://lldev.thespacedevs.com/2.2.0"


@responses.activate
def test_company_info_table(company_data):
    responses.add(
        responses.GET, 
        f"{BASE}/agencies/121/", 
        json=company_data
    )
    result = runner.invoke(app, ["company", "info"])
    assert result.exit_code == 0


@responses.activate
def test_company_info_json(company_data):
    responses.add(
        responses.GET, 
        f"{BASE}/agencies/121/", 
        json=company_data
    )
    result = runner.invoke(app, ["-o", "json", "company", "info"])
    assert result.exit_code == 0
    assert "SpaceX" in result.stdout
