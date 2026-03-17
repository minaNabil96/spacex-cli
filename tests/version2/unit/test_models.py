from datetime import datetime
import pytest
from spacex_cli.models.launch import Launch, LaunchDetails


def test_launch_creation():
    now = datetime.now()
    launch = Launch(
        id="1",
        name="Test Launch",
        date_utc=now,
        success=True,
        rocket="Falcon 9",
        launchpad="KSC",
        flight_number=1,
        details="Test details",
        links_webcast="http://webcast",
        links_article="http://article"
    )
    assert launch.id == "1"
    assert launch.name == "Test Launch"
    assert launch.date_utc == now
    assert launch.success is True


def test_launch_details_creation():
    now = datetime.now()
    launch = Launch(
        id="1",
        name="Test Launch",
        date_utc=now,
        success=True,
        rocket="Falcon 9",
        launchpad="KSC",
        flight_number=1,
        details="Test details",
        links_webcast="http://webcast",
        links_article="http://article"
    )
    details = LaunchDetails(
        launch=launch,
        payload_mass_kg=1000.0,
        payload_mass_lbs=2204.6,
        orbit="LEO",
        customers=["NASA"]
    )
    assert details.launch == launch
    assert details.payload_mass_kg == 1000.0
    assert details.customers == ["NASA"]


def test_frozen_behaviour():
    launch = Launch(
        id="1",
        name="Test Launch",
        date_utc=datetime.now(),
        success=True,
        rocket="Falcon 9",
        launchpad="KSC",
        flight_number=1,
        details=None,
        links_webcast=None,
        links_article=None
    )
    with pytest.raises(AttributeError):
        launch.name = "New Name"
