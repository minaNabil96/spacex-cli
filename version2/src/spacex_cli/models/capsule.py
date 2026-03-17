from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Capsule:
    id: str
    serial: str
    status: str
    type: str
    reuse_count: int
    water_landings: int
    land_landings: int
    last_update: Optional[str]
    launches: list[str]
