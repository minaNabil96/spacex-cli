from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import ROCKET_DETAIL, ROCKETS
from spacex_cli.models.rocket import Rocket


def get_rockets(client: SpaceXClient, limit: int = 10) -> list[Rocket]:
    # Agency 121 is SpaceX
    params = {"manufacturer__id": 121}
    return [_parse_rocket(item) for item in client.get_all(ROCKETS, params=params, limit=limit)]


def get_rocket_by_id(client: SpaceXClient, rocket_id: str) -> Rocket:
    return _parse_rocket(client.get(ROCKET_DETAIL.format(id=rocket_id)).json())


def _parse_rocket(data: dict) -> Rocket:
    config = data  # In ROCKETS list, each item is a launcher_config
    return Rocket(
        id=config["id"],
        name=config.get("name", config.get("full_name", "Unknown")),
        full_name=config.get("full_name", config["name"]),
        variant=config.get("variant", "N/A"),
        family=config.get("family", "N/A"),
        active=config.get("active", False),
        reusable=config.get("reusable", False),
        description=config.get("description", "No description available."),
        capacity_leo=config.get("leo_capacity"),
        capacity_gto=config.get("gto_capacity"),
        maiden_flight=config.get("maiden_flight"),
        height=config.get("height"),
        diameter=config.get("diameter"),
        info_url=config.get("info_url"),
        wiki_url=config.get("wiki_url"),
    )
