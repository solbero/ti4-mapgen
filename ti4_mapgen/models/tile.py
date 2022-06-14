from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from dataclass_wizard import JSONFileWizard, JSONWizard

from .hex import Cube
from .typing import Anomaly, Back, Faction, Letter, Release, Tag, Tech, Trait, Wormhole


@dataclass(frozen=False, kw_only=True)
class Tile(JSONWizard, JSONFileWizard):
    """Class representing a tile."""

    class _(JSONWizard.Meta):
        skip_defaults = True

    tag: Tag
    number: Optional[int] = None
    letter: Optional[Letter] = None
    position: Optional[Cube] = None
    release: Optional[Release] = None
    faction: Optional[Faction] = None
    back: Optional[Back] = None
    rotation: Optional[int] = 0
    system: Optional[System] = None
    hyperlanes: list[list[Cube]] = field(default_factory=list)


@dataclass(frozen=True, kw_only=True)
class System:
    """Class representing the system in a tile."""

    resources: int
    influence: int
    planets: int
    traits: list[Trait] = field(default_factory=list)
    techs: list[Tech] = field(default_factory=list)
    anomaly: Optional[Anomaly] = None
    wormhole: Optional[Wormhole] = None
    legendary: bool = False
