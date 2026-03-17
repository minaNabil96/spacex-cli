"""Unit tests for data models."""

import pytest
from datetime import datetime, timezone

from spacex_cli.models.launch import Launch, LaunchDetails
from spacex_cli.models.rocket import Rocket
from spacex_cli.models.capsule import Capsule
from spacex_cli.models.company import CompanyInfo


class TestLaunchModel:
    def test_create_launch(self):
        launch = Launch(
            id="abc-123",
            name="Test Mission",
            date_utc=datetime(2024, 1, 1, tzinfo=timezone.utc),
            status_name="Launch Successful",
            status_abbrev="Success",
            rocket="Falcon 9",
            launchpad="SLC-40",
            location="Cape Canaveral",
            flight_number=42,
            details="Test details",
            links_webcast="https://example.com/watch",
            links_article="https://example.com/article",
            image="https://example.com/image.jpg"
        )
        assert launch.id == "abc-123"
        assert launch.name == "Test Mission"
        assert launch.flight_number == 42
        assert launch.status_abbrev == "Success"
        assert launch.details == "Test details"

    def test_launch_frozen(self):
        launch = Launch(
            id="abc-123",
            name="Test Mission",
            date_utc=datetime(2024, 1, 1, tzinfo=timezone.utc),
            status_name="Launch Successful",
            status_abbrev="Success",
            rocket="Falcon 9",
            launchpad="SLC-40",
            location="Cape Canaveral",
            flight_number=1,
            details=None,
            links_webcast=None,
            links_article=None,
            image=None
        )
        with pytest.raises(AttributeError):
            launch.name = "Changed"  # type: ignore[misc]

    def test_launch_details_creation(self):
        launch = Launch(
            id="abc-123",
            name="Test Mission",
            date_utc=datetime(2024, 1, 1, tzinfo=timezone.utc),
            status_name="Launch Successful",
            status_abbrev="Success",
            rocket="Falcon 9",
            launchpad="SLC-40",
            location="Cape Canaveral",
            flight_number=42,
            details="Details here",
            links_webcast=None,
            links_article=None,
            image=None
        )
        details = LaunchDetails(
            launch=launch,
            agency_name="SpaceX",
            agency_type="Private",
            mission_name="Starlink",
            mission_type="Commercial",
            orbit="LEO",
            description="Mission description"
        )
        assert details.launch.name == "Test Mission"
        assert details.agency_name == "SpaceX"
        assert details.orbit == "LEO"


class TestRocketModel:
    def test_create_rocket(self):
        rocket = Rocket(
            id=164,
            name="Falcon 9",
            full_name="Falcon 9 Block 5",
            variant="Block 5",
            family="Falcon",
            active=True,
            reusable=True,
            description="Falcon 9 is a two-stage rocket.",
            capacity_leo=22800,
            capacity_gto=8300,
            maiden_flight="2010-06-04",
            height=70.0,
            diameter=3.7,
            info_url="https://example.com/info",
            wiki_url="https://example.com/wiki"
        )
        assert rocket.name == "Falcon 9"
        assert rocket.active is True
        assert rocket.height == 70.0

    def test_rocket_frozen(self):
        rocket = Rocket(
            id=1,
            name="Test",
            full_name="Test Rocket",
            variant="V1",
            family="TestFamily",
            active=True,
            reusable=True,
            description="Desc",
            capacity_leo=None,
            capacity_gto=None,
            maiden_flight=None,
            height=None,
            diameter=None,
            info_url=None,
            wiki_url=None
        )
        with pytest.raises(AttributeError):
            rocket.name = "Changed"  # type: ignore[misc]


class TestCapsuleModel:
    def test_create_capsule(self):
        capsule = Capsule(
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
        assert capsule.name == "Dragon 1.0"
        assert capsule.agency == "SpaceX"
        assert capsule.human_rated is False


class TestCompanyModel:
    def test_create_company_info(self):
        info = CompanyInfo(
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
            info_url=None,
            wiki_url=None,
            logo_url=None
        )
        assert info.name == "SpaceX"
        assert info.total_launch_count == 100
