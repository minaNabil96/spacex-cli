from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import ROCKETS
from spacex_cli.models.rocket import Rocket


def get_rockets(client: SpaceXClient, limit: int = 10) -> list[Rocket]:
    # Filter for SpaceX (Agency ID 121)
    return [
        _parse_rocket(item)
        for item in client.get_all(ROCKETS, params={"search": "SpaceX"}, limit=limit)
    ]


def get_rocket_by_id(client: SpaceXClient, rocket_id: str) -> Rocket:
    # Rocket ID in LL2 corresponds to config/launcher/{id}
    endpoint = f"{ROCKETS}/{rocket_id}/"
    return _parse_rocket(client.get(endpoint).json())


def _parse_rocket(data: dict) -> Rocket:
    return Rocket(
        id=str(data["id"]),
        name=data["full_name"],
        type=data.get("variant", "Unknown"),
        active=True, # Active field not exactly same in LL2 configs
        stages=0, # Detail not in summary response
        boosters=0,
        cost_per_launch=0,
        success_rate_pct=0.0,
        first_flight=None,
        country="USA",
        company="SpaceX",
        height={},
        diameter={},
        mass={},
        description=data.get("description", "No description available."),
    )
