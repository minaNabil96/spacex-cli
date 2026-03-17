import requests
from typing import Optional

from spacex_cli.config.settings import get_api_url, get_timeout
from spacex_cli.utils.errors import APIError, NetworkError, NotFoundError


class SpaceXClient:
    """Thin wrapper around requests.Session for Launch Library 2 API."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers.update(
            {"Accept": "application/json", "User-Agent": "SpaceX-CLI/0.1"}
        )
        self._base_url = get_api_url()
        self._timeout = get_timeout()

    def get(self, endpoint: str, params: Optional[dict] = None) -> requests.Response:
        url = f"{self._base_url}{endpoint}"
        try:
            response = self._session.get(url, params=params, timeout=self._timeout)
        except requests.exceptions.RequestException as exc:
            raise NetworkError(f"Network error: {exc}") from exc
        self._raise_for_status(response)
        return response

    def get_all(
        self, endpoint: str, params: Optional[dict] = None, limit: int = 100
    ) -> list[dict]:
        # If limit is already in params, use it; otherwise use the default limit argument
        if params and "limit" in params:
            limit = params["limit"]
        params = {**(params or {}), "limit": limit}
        # Launch Library 2 API returns a dict with 'results' list
        # We need to handle this correctly as per the API's structure
        response = self.get(endpoint, params=params).json()
        if isinstance(response, dict) and "results" in response:
            return response["results"]
        # If it's already a list (unlikely based on LL2 API docs but just in case)
        if isinstance(response, list):
            return response
        return [response]

    @staticmethod
    def _raise_for_status(response: requests.Response) -> None:
        match response.status_code:
            case 200 | 201 | 204:
                return
            case 404:
                raise NotFoundError("resource", response.url)
            case _:
                try:
                    msg = response.json().get("message", "Unknown error")
                except Exception:
                    msg = response.text
                raise APIError(response.status_code, msg)

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "SpaceXClient":
        return self

    def __exit__(self, *exc) -> None:
        self.close()
