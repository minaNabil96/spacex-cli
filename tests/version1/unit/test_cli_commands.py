"""Unit tests for CLI commands (basic invocation via CliRunner)."""

import responses
from typer.testing import CliRunner

from spacex_cli.cli import app

runner = CliRunner()
BASE = "https://api.spacexdata.com/v4"


@responses.activate
def test_help_command():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "SpaceX" in result.output


@responses.activate
def test_launches_help():
    result = runner.invoke(app, ["launches", "--help"])
    assert result.exit_code == 0
    assert "list" in result.output.lower()


@responses.activate
def test_rockets_help():
    result = runner.invoke(app, ["rockets", "--help"])
    assert result.exit_code == 0
    assert "list" in result.output.lower()


@responses.activate
def test_capsules_help():
    result = runner.invoke(app, ["capsules", "--help"])
    assert result.exit_code == 0
    assert "list" in result.output.lower()


@responses.activate
def test_company_help():
    result = runner.invoke(app, ["company", "--help"])
    assert result.exit_code == 0
    assert "info" in result.output.lower()


@responses.activate
def test_export_help():
    result = runner.invoke(app, ["export", "--help"])
    assert result.exit_code == 0
    assert "launches" in result.output.lower()
