from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CompanyInfo:
    name: str
    founder: str
    founded: int
    employees: int
    vehicles: int
    launch_sites: int
    test_sites: int
    ceo: str
    cto: str
    coo: str
    valuation: int
    headquarters: dict
    links: dict
    summary: str
