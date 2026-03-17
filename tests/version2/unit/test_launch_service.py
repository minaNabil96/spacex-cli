import responses
from spacex_cli.api.client import SpaceXClient
from spacex_cli.services import launch_service


@responses.activate
def test_get_launches(launches_data):
    responses.add(
        responses.GET,
        "https://lldev.thespacedevs.com/2.2.0/launch/",
        json=launches_data,
        status=200,
        match_querystring=False
    )
    
    with SpaceXClient() as client:
        launches = launch_service.get_launches(client)
        
    assert len(launches) == 2
    assert launches[0].name == "Falcon 9 Block 5 | Crew-1"
    assert launches[0].success is True


@responses.activate
def test_get_launch_by_id(launches_data):
    responses.add(
        responses.GET,
        "https://lldev.thespacedevs.com/2.2.0/launch/1/",
        json=launches_data["results"][0],
        status=200
    )
    
    with SpaceXClient() as client:
        details = launch_service.get_launch_by_id(client, "1")
        
    assert details.launch.id == "1"
    assert "Crew-1" in details.launch.name
