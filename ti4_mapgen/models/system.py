from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ti4_mapgen.models.typing import Anomaly, Wormhole, Trait, Tech
from ti4_mapgen.models.hex import CardinalDirection


@dataclass(frozen=True)
class System:
    """Class representing a standard system."""

    anomaly: Optional[Anomaly]
    wormhole: Optional[Wormhole]
    planets: Optional[tuple[Planet]]


@dataclass(frozen=True)
class Planet:
    """Class representing a planet in a system."""

    name: str
    resources: int
    influence: int
    trait: Optional[Trait]
    tech: Optional[Tech]
    legendary: bool


@dataclass(frozen=True)
class Hyperlane:
    """Class representing a hyperlane system."""

    hyperlanes: list[list[CardinalDirection]]
    rotation: Optional[int] = 0
