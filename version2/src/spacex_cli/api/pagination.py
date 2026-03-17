from typing import Generator, Optional
from spacex_cli.api.client import SpaceXClient


def paginate(
    client: SpaceXClient,
    endpoint: str,
    params: Optional[dict] = None,
    limit: int = 100,
) -> Generator[dict, None, None]:
    """Возвращает отдельные объекты из постраничного ответа API."""
    data = client.get_all(endpoint, params=params, limit=limit)
    for item in data:
        yield item
