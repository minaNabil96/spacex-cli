from datetime import datetime
from typing import Optional

from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import (
    LAUNCH_DETAIL,
    LAUNCH_PREVIOUS,
    LAUNCH_UPCOMING,
    LAUNCHES,
)
from spacex_cli.models.launch import Launch, LaunchDetails


def get_launches(
    client: SpaceXClient,
    limit: int = 10,
    upcoming: bool = False,
    past: bool = False,
) -> list[Launch]:
    endpoint = LAUNCHES
    if upcoming:
        endpoint = LAUNCH_UPCOMING
    elif past:
        endpoint = LAUNCH_PREVIOUS

    # Agency ID 121 is SpaceX
    params = {"lsp__id": 121}
    data = client.get_all(endpoint, params=params, limit=limit)
    return [_parse_launch(item) for item in data]


def get_launch_by_id(client: SpaceXClient, launch_id: str) -> LaunchDetails:
    data = client.get(LAUNCH_DETAIL.format(id=launch_id)).json()
    return _parse_launch_details(data)


def get_next_launch(client: SpaceXClient) -> Launch:
    # Use upcoming with limit 1 to get the next launch
    data = client.get_all(LAUNCH_UPCOMING, params={"lsp__id": 121}, limit=1)
    if not data:
        raise Exception("No upcoming launches found")
    return _parse_launch(data[0])


def _parse_launch(data: dict) -> Launch:
    # LL2 date is in 'net' field
    net_str = data.get("net", data.get("window_start", ""))
    date_utc = datetime.fromisoformat(net_str.replace("Z", "+00:00"))

    status = data.get("status", {})
    rocket = data.get("rocket", {}).get("configuration", {})
    pad = data.get("pad", {})
    location = pad.get("location", {})

    vids = data.get("vidURLs", [])
    articles = data.get("infoURLs", [])

    return Launch(
        id=data["id"],
        name=data["name"],
        date_utc=date_utc,
        status_name=status.get("name", "Unknown"),
        status_abbrev=status.get("abbrev", "N/A"),
        rocket=rocket.get("full_name", rocket.get("name", "Unknown")),
        launchpad=pad.get("name", "Unknown"),
        location=location.get("name", "Unknown"),
        flight_number=data.get("orbital_launch_attempt_count"),
        details=data.get("mission", {}).get("description") or status.get("description"),
        links_webcast=vids[0]["url"] if vids else None,
        links_article=articles[0]["url"] if articles else None,
        image=data.get("image"),
    )


def _parse_launch_details(data: dict) -> LaunchDetails:
    launch = _parse_launch(data)
    agency = data.get("launch_service_provider", {})
    mission = data.get("mission", {}) or {}

    return LaunchDetails(
        launch=launch,
        agency_name=agency.get("name", "SpaceX"),
        agency_type=agency.get("type"),
        mission_name=mission.get("name"),
        mission_type=mission.get("type"),
        orbit=mission.get("orbit", {}).get("name"),
        description=mission.get("description"),
    )
