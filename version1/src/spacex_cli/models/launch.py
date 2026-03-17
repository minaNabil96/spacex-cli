from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True, slots=True)
class Launch:
    id: str
    name: str
    date_utc: datetime
    status_name: str
    status_abbrev: str
    rocket: str
    launchpad: str
    location: str
    flight_number: Optional[int]
    details: Optional[str]
    links_webcast: Optional[str]
    links_article: Optional[str]
    image: Optional[str]


@dataclass(frozen=True, slots=True)
class LaunchDetails:
    launch: Launch
    agency_name: str
    agency_type: Optional[str]
    mission_name: Optional[str]
    mission_type: Optional[str]
    orbit: Optional[str]
    description: Optional[str]
