from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from dataclass_wizard import JSONFileWizard, JSONWizard

from models.hex import CardinalDirection, CubePosition
from models.system import System
from models.typing import Back, Letter, Name, Release, Tile


@dataclass(kw_only=True)
class BaseTile:
    """Class representing a base tile."""

    type: Literal[Tile]
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
