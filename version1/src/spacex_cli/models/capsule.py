from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Capsule:
    id: int
    name: str
    type: str
    agency: str
    in_use: bool
    capability: str
    maiden_flight: Optional[str]
    height: Optional[float]
    diameter: Optional[float]
    human_rated: bool
    crew_capacity: Optional[int]
    image_url: Optional[str]
    wiki_url: Optional[str]
