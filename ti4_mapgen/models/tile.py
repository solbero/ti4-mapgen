from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from dataclass_wizard import JSONWizard, JSONFileWizard

from .hex import CardinalDirection, CubePosition
from .typing import Back, Letter, Name, Release, Anomaly, Wormhole, Trait, Tech


@dataclass(frozen=True, kw_only=True)
class Tile(JSONWizard, JSONFileWizard):
    """Class representing a tile."""

    class _(JSONWizard.Meta):
        skip_defaults = True

    position: Optional[CubePosition] = None
    number: int
    letter: Optional[Letter] = None
    type: str
    back: Optional[Back] = None
    release: Release
    rotation: Optional[int] = 0
    faction: Optional[Name] = None
    anomaly: Optional[Anomaly] = None
    wormhole: Optional[Wormhole] = None
    planets: Optional[list[Planet]] = field(default_factory=list)
    hyperlanes: list[list[CardinalDirection]] = field(default_factory=list)


@dataclass(frozen=True, kw_only=True)
class Planet:
    """Class representing a planet in a system."""

    name: str
    resources: int
    influence: int
    trait: Optional[Trait] = None
    tech: Optional[Tech] = None
    legendary: bool
