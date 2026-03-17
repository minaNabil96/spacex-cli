import responses
from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.pagination import paginate


@responses.activate
def test_paginate(launches_data):
    responses.add(
        responses.GET,
        "https://lldev.thespacedevs.com/2.2.0/launch",
        json=launches_data,
        status=200
    )
    
    with SpaceXClient() as client:
        items = list(paginate(client, "launch", limit=2))
        
    assert len(items) == 2
    assert items[0]["name"] == "Falcon 9 Block 5 | Crew-1"
