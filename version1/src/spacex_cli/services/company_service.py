from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import AGENCY_DETAIL
from spacex_cli.models.company import CompanyInfo


def get_company_info(client: SpaceXClient) -> CompanyInfo:
    # Agency 121 is SpaceX
    data = client.get(AGENCY_DETAIL.format(id=121)).json()
    return _parse_agency(data)


def _parse_agency(data: dict) -> CompanyInfo:
    return CompanyInfo(
        id=data["id"],
        name=data["name"],
        abbrev=data.get("abbreviation", "N/A"),
        type=data.get("type", "Private"),
        country_code=data.get("country_code", "USA"),
        description=data.get("description", "No description available."),
        administrator=data.get("administrator", "N/A"),
        founding_year=data.get("founding_year", "N/A"),
        launchers=data.get("launchers", "N/A"),
        spacecraft=data.get("spacecraft", "N/A"),
        total_launch_count=data.get("total_launch_count", 0),
        successful_launches=data.get("successful_launches", 0),
        consecutive_successful_launches=data.get("consecutive_successful_launches", 0),
        failed_launches=data.get("failed_launches", 0),
        pending_launches=data.get("pending_launches", 0),
        info_url=data.get("info_url"),
        wiki_url=data.get("wiki_url"),
        logo_url=data.get("logo_url"),
    )
