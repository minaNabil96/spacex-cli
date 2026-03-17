from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class CompanyInfo:
    id: int
    name: str
    abbrev: str
    type: str
    country_code: str
    description: str
    administrator: str
    founding_year: str
    launchers: str
    spacecraft: str
    total_launch_count: int
    successful_launches: int
    consecutive_successful_launches: int
    failed_launches: int
    pending_launches: int
    info_url: Optional[str]
    wiki_url: Optional[str]
    logo_url: Optional[str]
