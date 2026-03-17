from typing import Generator, Optional
from spacex_cli.api.client import SpaceXClient


def paginate(
    client: SpaceXClient,
    endpoint: str,
    params: Optional[dict] = None,
    limit: int = 100,
) -> Generator[dict, None, None]:
    """Yields individual objects from a paginated API response."""
    for item in client.get_all(endpoint, params=params, limit=limit):
        yield item
