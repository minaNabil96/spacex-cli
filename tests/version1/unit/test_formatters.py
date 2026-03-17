"""Unit tests for formatters."""

import json
from datetime import datetime, timezone

from spacex_cli.formatters.json_fmt import format_json
from spacex_cli.formatters.csv_fmt import format_to_csv
from spacex_cli.formatters.table_fmt import (
    format_launches_table,
    format_rockets_table,
    format_capsules_table,
)
from spacex_cli.formatters.panel_fmt import (
    format_launch_panel,
    format_rocket_panel,
    format_capsule_panel,
    format_company_panel,
)
from spacex_cli.models.launch import Launch, LaunchDetails
from spacex_cli.models.rocket import Rocket
from spacex_cli.models.capsule import Capsule
from spacex_cli.models.company import CompanyInfo


def _make_launch(**kwargs) -> Launch:
    defaults = dict(
        id="test1",
        name="Test Mission",
        date_utc=datetime(2024, 1, 1, tzinfo=timezone.utc),
        status_name="Launch Successful",
        status_abbrev="Success",
        rocket="Falcon 9",
        launchpad="SLC-40",
        location="Cape Canaveral",
        flight_number=1,
        details="Test details",
        links_webcast="https://example.com",
        links_article="https://example.com/article",
        image="https://example.com/img"
    )
    defaults.update(kwargs)
    return Launch(**defaults)


def _make_rocket(**kwargs) -> Rocket:
    defaults = dict(
        id=164,
        name="Falcon 9",
        full_name="Falcon 9 Block 5",
        variant="Block 5",
        family="Falcon",
        active=True,
        reusable=True,
        description="Two-stage rocket.",
        capacity_leo=22800,
        capacity_gto=8300,
        maiden_flight="2010-06-04",
        height=70.0,
        diameter=3.7,
        info_url="https://example.com",
        wiki_url="https://example.com/wiki"
    )
    defaults.update(kwargs)
    return Rocket(**defaults)


def _make_capsule(**kwargs) -> Capsule:
    defaults = dict(
        id=3,
        name="Dragon 1.0",
        type="Capsule",
        agency="SpaceX",
        in_use=False,
        capability="Cargo",
        maiden_flight="2010-12-08",
        height=6.1,
        diameter=3.7,
        human_rated=False,
        crew_capacity=0,
        image_url=None,
        wiki_url=None
    )
    defaults.update(kwargs)
    return Capsule(**defaults)


def _make_company(**kwargs) -> CompanyInfo:
    defaults = dict(
        id=121,
        name="SpaceX",
        abbrev="SX",
        type="Private",
        country_code="USA",
        description="Space company",
        administrator="Elon Musk",
        founding_year="2002",
        launchers="Falcon",
        spacecraft="Dragon",
        total_launch_count=100,
        successful_launches=95,
        consecutive_successful_launches=10,
        failed_launches=5,
        pending_launches=2,
        info_url="https://example.com",
        wiki_url="https://example.com/wiki",
        logo_url=None
    )
    defaults.update(kwargs)
    return CompanyInfo(**defaults)


# ── JSON Formatter ────────────────────────────────────────────────────────────


class TestJsonFormatter:
    def test_compact_json(self):
        data = {"key": "value", "num": 42}
        result = format_json(data, pretty=False)
        parsed = json.loads(result)
        assert parsed == data
        assert "\n" not in result  # compact — no newlines

    def test_pretty_json(self):
        data = {"key": "value"}
        result = format_json(data, pretty=True)
        parsed = json.loads(result)
        assert parsed == data
        assert "\n" in result  # pretty — has newlines

    def test_json_with_datetime(self):
        data = {"ts": datetime(2024, 1, 1, tzinfo=timezone.utc)}
        result = format_json(data, pretty=False)
        parsed = json.loads(result)
        assert "2024" in parsed["ts"]

    def test_json_list(self):
        data = [{"a": 1}, {"b": 2}]
        result = format_json(data, pretty=False)
        parsed = json.loads(result)
        assert len(parsed) == 2


# ── CSV Formatter ─────────────────────────────────────────────────────────────


class TestCsvFormatter:
    def test_csv_basic(self):
        data = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
        result = format_to_csv(data)
        assert "name,age" in result
        assert "Alice,30" in result
        assert "Bob,25" in result

    def test_csv_empty(self):
        result = format_to_csv([])
        assert result == ""


# ── Table Formatters ──────────────────────────────────────────────────────────


class TestTableFormatters:
    def test_launches_table_columns(self):
        launches = [_make_launch(), _make_launch(name="Second", flight_number=2)]
        table = format_launches_table(launches)
        assert table.title == "🚀 SpaceX Launches"
        assert len(table.columns) == 4
        assert table.row_count == 2

    def test_rockets_table_columns(self):
        rockets = [_make_rocket()]
        table = format_rockets_table(rockets)
        assert table.title == "🛰️ SpaceX Rockets"
        assert len(table.columns) == 5
        assert table.row_count == 1

    def test_capsules_table_columns(self):
        capsules = [_make_capsule()]
        table = format_capsules_table(capsules)
        assert table.title == "🐉 Spacecraft Versions"
        assert len(table.columns) == 5
        assert table.row_count == 1


# ── Panel Formatters ──────────────────────────────────────────────────────────


class TestPanelFormatters:
    def test_launch_panel(self):
        launch = _make_launch()
        details = LaunchDetails(
            launch=launch,
            agency_name="SpaceX",
            agency_type="Private",
            mission_name="Starlink",
            mission_type="Commercial",
            orbit="LEO",
            description="Mission description"
        )
        panel = format_launch_panel(details)
        assert panel.title is not None
        assert "Launch Details" in str(panel.title)

    def test_rocket_panel(self):
        rocket = _make_rocket()
        panel = format_rocket_panel(rocket)
        assert panel.title is not None
        assert "Launcher Specs" in str(panel.title)

    def test_capsule_panel(self):
        capsule = _make_capsule()
        panel = format_capsule_panel(capsule)
        assert panel.title is not None
        assert "Spacecraft Details" in str(panel.title)

    def test_company_panel(self):
        company = _make_company()
        panel = format_company_panel(company)
        assert panel.title is not None
        assert "Agency Info" in str(panel.title)
