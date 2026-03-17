"""Integration tests for export commands."""

import json
import os
import tempfile

import responses
from typer.testing import CliRunner

from spacex_cli.cli import app

runner = CliRunner()
BASE = "https://lldev.thespacedevs.com/2.2.0"


@responses.activate
def test_export_launches_json(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/", 
        json={"results": launches_data, "count": len(launches_data)}
    )
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        dest = f.name
    try:
        result = runner.invoke(app, ["export", "launches", "--dest", dest, "--format", "json"])
        assert result.exit_code == 0
        with open(dest, "r") as f:
            exported = json.load(f)
        assert isinstance(exported, list)
        assert len(exported) == len(launches_data)
    finally:
        os.unlink(dest)


@responses.activate
def test_export_launches_csv(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/", 
        json={"results": launches_data, "count": len(launches_data)}
    )
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        dest = f.name
    try:
        result = runner.invoke(app, ["export", "launches", "--dest", dest, "--format", "csv"])
        assert result.exit_code == 0
        with open(dest, "r") as f:
            content = f.read()
        assert "id" in content  # CSV header
        assert "Starlink-1" in content
    finally:
        os.unlink(dest)


@responses.activate
def test_export_launches_markdown(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/", 
        json={"results": launches_data, "count": len(launches_data)}
    )
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
        dest = f.name
    try:
        result = runner.invoke(
            app, ["export", "launches", "--dest", dest, "--format", "markdown"]
        )
        assert result.exit_code == 0
        with open(dest, "r") as f:
            content = f.read()
        assert "# SpaceX Launches" in content
        assert "```json" in content
    finally:
        os.unlink(dest)


@responses.activate
def test_export_launches_invalid_format(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launch/", 
        json={"results": launches_data, "count": len(launches_data)}
    )
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        dest = f.name
    try:
        result = runner.invoke(app, ["export", "launches", "--dest", dest, "--format", "xml"])
        assert result.exit_code == 2
    finally:
        if os.path.exists(dest):
            os.unlink(dest)
