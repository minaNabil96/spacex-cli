"""Unit tests for launch service parsing logic."""

from datetime import datetime

from spacex_cli.services.launch_service import _parse_launch, _parse_launch_details


class TestParseLaunch:
    def test_parse_basic_launch(self, single_launch_data):
        launch = _parse_launch(single_launch_data)
        assert launch.id == "5eb11b6b-199f-449e-9d29-6126600c0106"
        assert launch.name == "Falcon 9 Block 5 | Starlink-1"
        assert launch.flight_number == 123
        assert launch.status_abbrev == "Success"
        assert isinstance(launch.date_utc, datetime)
        assert launch.date_utc.tzinfo is not None

    def test_parse_launch_links(self, single_launch_data):
        launch = _parse_launch(single_launch_data)
        assert launch.links_webcast is not None
        assert "youtube" in launch.links_webcast
        assert launch.links_article is not None

    def test_parse_launch_missing_links(self):
        data = {
            "id": "uuid-test",
            "name": "Test",
            "net": "2024-01-01T00:00:00.000Z",
            "orbital_launch_attempt_count": 1,
            "status": {"name": "Launch Successful", "abbrev": "Success"}
        }
        launch = _parse_launch(data)
        assert launch.links_webcast is None
        assert launch.links_article is None
        assert launch.status_abbrev == "Success"
        assert launch.details is None

    def test_parse_launch_details(self, single_launch_data):
        details = _parse_launch_details(single_launch_data)
        assert details.launch.name == "Falcon 9 Block 5 | Starlink-1"
        assert details.mission_name == "Starlink-1"
        assert details.orbit == "Low Earth Orbit"
        assert details.agency_name == "SpaceX"

    def test_parse_launch_details_no_mission(self):
        data = {
            "id": "test",
            "name": "Test",
            "net": "2024-01-01T00:00:00.000Z",
            "orbital_launch_attempt_count": 1,
            "status": {"name": "Launch Successful", "abbrev": "Success"}
        }
        details = _parse_launch_details(data)
        assert details.mission_name is None
        assert details.orbit is None
        assert details.agency_name == "SpaceX"
