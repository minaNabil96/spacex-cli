from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import CAPSULES
from spacex_cli.models.capsule import Capsule


def get_capsules(client: SpaceXClient, limit: int = 10) -> list[Capsule]:
    # Filter for SpaceX (Agency ID 121)
    return [
        _parse_capsule(item)
        for item in client.get_all(CAPSULES, params={"search": "SpaceX"}, limit=limit)
    ]


def get_capsule_by_id(client: SpaceXClient, capsule_id: str) -> Capsule:
    endpoint = f"{CAPSULES}{capsule_id}/" # CAPSULES already ends with /
    return _parse_capsule(client.get(endpoint).json())


def _parse_capsule(data: dict) -> Capsule:
    return Capsule(
        id=str(data["id"]),
        serial=data["name"],
        status="active", # LL2 has different status structure
        type=data.get("type", {}).get("name", "Unknown"),
        reuse_count=0,
        water_landings=0,
        land_landings=0,
        last_update=None,
        launches=[],
    )
