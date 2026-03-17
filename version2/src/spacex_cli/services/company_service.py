from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import COMPANY
from spacex_cli.models.company import CompanyInfo


def get_company_info(client: SpaceXClient) -> CompanyInfo:
    data = client.get(COMPANY).json()
    return CompanyInfo(
        name=data["name"],
        founder=data.get("administrator", "Elon Musk"),
        founded=data.get("founding_year", 2002),
        employees=0, # Not in LL2 agency response
        vehicles=len(data.get("launcher_list", [])),
        launch_sites=0,
        test_sites=0,
        ceo=data.get("administrator", "Elon Musk"),
        cto="Elon Musk",
        coo="Gwynne Shotwell",
        valuation=0,
        headquarters={},
        links={},
        summary=data.get("description", "SpaceX is a private American aerospace manufacturer and space transportation services company."),
    )
