from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True, slots=True)
class Launch:
    id: str
    name: str
    date_utc: datetime
    success: Optional[bool]
    rocket: str
    launchpad: str
    flight_number: int
    details: Optional[str]
    links_webcast: Optional[str]
    links_article: Optional[str]


@dataclass(frozen=True, slots=True)
class LaunchDetails:
    launch: Launch
    payload_mass_kg: Optional[float]
    payload_mass_lbs: Optional[float]
    orbit: Optional[str]
    customers: list[str]
