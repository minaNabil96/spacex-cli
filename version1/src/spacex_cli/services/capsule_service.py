from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import CAPSULE_DETAIL, CAPSULES
from spacex_cli.models.capsule import Capsule


def get_capsules(client: SpaceXClient, limit: int = 10) -> list[Capsule]:
    # Filter by SpaceX (Agency 121) if possible, or just parse and handle in UI
    # LL2 /config/spacecraft/ doesn't always have a direct agency filter like launcher
    params = {} 
    data = client.get_all(CAPSULES, params=params, limit=limit)
    return [_parse_capsule(item) for item in data]


def get_capsule_by_id(client: SpaceXClient, capsule_id: str) -> Capsule:
    return _parse_capsule(client.get(CAPSULE_DETAIL.format(id=capsule_id)).json())


def _parse_capsule(data: dict) -> Capsule:
    agency_list = data.get("agency", [])
    if isinstance(agency_list, dict): # Handle inconsistent API response types
        agency_name = agency_list.get("name", "SpaceX")
    else:
        agency_name = agency_list[0].get("name", "SpaceX") if agency_list else "SpaceX"

    return Capsule(
        id=data["id"],
        name=data["name"],
        type=data.get("type", {}).get("name", "Unknown"),
        agency=agency_name,
        in_use=data.get("in_use", False),
        capability=data.get("capability", "N/A"),
        maiden_flight=data.get("maiden_flight"),
        height=data.get("height"),
        diameter=data.get("diameter"),
        human_rated=data.get("human_rated", False),
        crew_capacity=data.get("crew_capacity"),
        image_url=data.get("image_url"),
        wiki_url=data.get("wiki_url"),
    )
