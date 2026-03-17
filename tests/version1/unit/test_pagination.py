"""Unit tests for pagination module."""

import responses

from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.pagination import paginate

BASE = "https://lldev.thespacedevs.com/2.2.0"


@responses.activate
def test_paginate_yields_all_items(launches_data):
    responses.add(
        responses.GET, 
        f"{BASE}/launches", 
        json={"results": launches_data, "count": len(launches_data)}
    )

    with SpaceXClient() as client:
        # Note: paginate currently loops forever if total count isn't handled or if results are always returned
        # However, it expects results to be empty to stop.
        items = list(paginate(client, "/launches", limit=100))

    assert len(items) == len(launches_data)
    assert items[0]["id"] == launches_data[0]["id"]


@responses.activate
def test_paginate_empty_response():
    responses.add(responses.GET, f"{BASE}/launches", json={"results": [], "count": 0})

    with SpaceXClient() as client:
        items = list(paginate(client, "/launches", limit=10))

    assert items == []


@responses.activate
def test_paginate_single_item():
    single = [{"id": "single", "name": "Test"}]
    responses.add(responses.GET, f"{BASE}/rockets", json={"results": single, "count": 1})

    with SpaceXClient() as client:
        items = list(paginate(client, "/rockets", limit=5))

    assert len(items) == 1
    assert items[0]["name"] == "Test"
