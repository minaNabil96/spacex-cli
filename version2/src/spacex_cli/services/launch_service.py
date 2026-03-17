from datetime import datetime
from typing import Optional

from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import LAUNCH_DETAIL, LAUNCHES, LAUNCH_UPCOMING, LAUNCH_PREVIOUS
from spacex_cli.models.launch import Launch, LaunchDetails


def get_launches(
    client: SpaceXClient,
    limit: int = 10,
    upcoming: bool = False,
    past: bool = False,
) -> list[Launch]:
    # For LL2 API, we choose the appropriate endpoint
    endpoint = LAUNCHES
    if upcoming:
        endpoint = LAUNCH_UPCOMING
    elif past:
        endpoint = LAUNCH_PREVIOUS
        
    # Filter for SpaceX (Agency ID 121) using Launch Service Provider ID
    params = {"lsp__id": 121}
    data = client.get_all(endpoint, params=params, limit=limit)
    return [_parse_launch(item) for item in data]


def get_launch_by_id(client: SpaceXClient, launch_id: str) -> LaunchDetails:
    response = client.get(LAUNCH_DETAIL.format(id=launch_id)).json()
    return _parse_launch_details(response)


def get_next_launch(client: SpaceXClient) -> Launch:
    # Get the first upcoming SpaceX launch
    data = client.get_all(LAUNCH_UPCOMING, params={"lsp__id": 121}, limit=1)
    if not data:
        raise Exception("No upcoming launches found")
    return _parse_launch(data[0])


def _parse_launch(data: dict) -> Launch:
    # LL2 API mapping to Launch model
    # Date: 'net' field in ISO format
    date_str = data.get("net", "")
    try:
        date_utc = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        date_utc = datetime.now() # Fallback

    # Success: status object
    # Status ID 3 is success, 4 is failure
    status_id = data.get("status", {}).get("id")
    success = None
    if status_id == 3:
        success = True
    elif status_id == 4:
        success = False

    # Rocket: rocket -> configuration -> full_name
    rocket_name = data.get("rocket", {}).get("configuration", {}).get("full_name", "Unknown Rocket")
    
    # Launchpad: pad -> name
    launchpad_name = data.get("pad", {}).get("name", "Unknown Pad")

    # Details: mission -> description
    details = data.get("mission", {}).get("description") if data.get("mission") else "No mission details."

    # Links: webcast and article
    # LL2 has video_url or lives streams in vidURLs
    vid_urls = data.get("vidURLs", [])
    webcast = vid_urls[0].get("url") if vid_urls else None
    
    # Article: not always present in a direct field, maybe in 'infoURLs'
    info_urls = data.get("infoURLs", [])
    article = info_urls[0].get("url") if info_urls else None

    return Launch(
        id=data["id"],
        name=data["name"],
        date_utc=date_utc,
        success=success,
        rocket=rocket_name,
        launchpad=launchpad_name,
        flight_number=0, # Flight number not directly in LL2 top-level for all agencies
        details=details,
        links_webcast=webcast,
        links_article=article,
    )


def _parse_launch_details(data: dict) -> LaunchDetails:
    launch = _parse_launch(data)
    
    # Payloads in LL2 are nested in mission -> orbit or separate rocket -> configuration -> payloads?
    # Actually LL2 has mission -> orbit -> name
    mission = data.get("mission") or {}
    orbit = mission.get("orbit", {}).get("name") if mission.get("orbit") else "Unknown"
    
    # Customers: not as easy in LL2 2.2.0, usually in agency or mission
    customers = []
    if mission.get("type"):
         customers.append(mission["type"]) # Just a placeholder since LL2 varies

    return LaunchDetails(
        launch=launch,
        payload_mass_kg=mission.get("payload_mass") if mission else None,
        payload_mass_lbs=None,
        orbit=orbit,
        customers=customers,
    )
