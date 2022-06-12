from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from dataclass_wizard import JSONWizard, JSONFileWizard

from .hex import CardinalDirection, Cube
from .typing import Back, Letter, Faction, Release, Anomaly, Wormhole, Trait, Tech, Tag


@dataclass(frozen=False, kw_only=True)
class Tile(JSONWizard, JSONFileWizard):
    """Class representing a tile."""

    class _(JSONWizard.Meta):
        skip_defaults = True

    tag: Tag
    number: int
    letter: Optional[Letter] = None
    release: Release
    back: Optional[Back] = None
    rotation: Optional[int] = 0
    system: Optional[System] = None


@dataclass()
class TileFaceDown:
    """Class representing a face-down tile."""
    tag: Tag
    back: Back


@dataclass(frozen=True, kw_only=True)
class System:
    """Class representing the system in a tile."""

    faction: Optional[Faction] = None
    anomaly: Optional[Anomaly] = None
    wormhole: Optional[Wormhole] = None
    planets: list[Planet] = field(default_factory=list)
    hyperlanes: list[list[CardinalDirection | Cube]] = field(default_factory=list)


@dataclass(frozen=True, kw_only=True)
class Planet:
    """Class representing a planet in a system."""

    name: str
    resources: int
    influence: int
    trait: Optional[Trait] = None
    tech: Optional[Tech] = None
    legendary: bool
