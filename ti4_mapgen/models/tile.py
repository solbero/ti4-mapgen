from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from dataclass_wizard import JSONFileWizard, JSONWizard

from ti4_mapgen.models.typing import Name, Release, Letter, Back
from ti4_mapgen.models.hex import CardinalDirection, CubePosition
from ti4_mapgen.models.system import System


@dataclass(kw_only=True)
class BaseTile:
    """Class representing a base tile."""

    position: Optional[CubePosition] = None
    number: int


@dataclass()
class SystemTile(BaseTile):
    """Class representing a system tile."""

    back: Optional[Back]
    release: Release
    system: System


@dataclass(kw_only=True)
class HyperlaneTile(BaseTile):
    """Class representing a hyperlane tile."""

    letter: Letter
    rotation: Optional[int] = 0
    hyperlanes: list[list[CardinalDirection]]


@dataclass()
class HomeSystemTile(SystemTile):
    """Class representing a home system tile."""

    faction: Name


@dataclass()
class Stack(JSONWizard, JSONFileWizard):
    """Class representing stacks of tiles."""

    class _(JSONWizard.Meta):
        skip_defaults = True

    system_tiles: list[SystemTile] = field(default_factory=list)
    home_system_tiles: list[HomeSystemTile] = field(default_factory=list)
    special_tiles: list[SystemTile] = field(default_factory=list)
    hyperlane_tiles: list[HyperlaneTile] = field(default_factory=list)
