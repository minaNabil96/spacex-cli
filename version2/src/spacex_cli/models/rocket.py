from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Rocket:
    id: str
    name: str
    type: str
    active: bool
    stages: int
    boosters: int
    cost_per_launch: int
    success_rate_pct: float
    first_flight: Optional[str]
    country: str
    company: str
    height: dict
    diameter: dict
    mass: dict
    description: str
