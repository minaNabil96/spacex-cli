from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Rocket:
    id: int
    name: str
    full_name: str
    variant: str
    family: str
    active: bool
    reusable: bool
    description: str
    capacity_leo: Optional[int]
    capacity_gto: Optional[int]
    maiden_flight: Optional[str]
    height: Optional[float]
    diameter: Optional[float]
    info_url: Optional[str]
    wiki_url: Optional[str]
