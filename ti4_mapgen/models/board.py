from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from dataclass_wizard import JSONFileWizard, JSONWizard

from .hex import CubePosition
from .tile import Tile


@dataclass(frozen=True, kw_only=True)
class Layout:
    """Class representing a map layout."""

    center: CubePosition
    rings: dict[int, list[CubePosition]]
    homes: dict[int, CubePosition]
    hyperlanes: Optional[list[Tile]] = None


@dataclass(frozen=True)
class Map(JSONWizard, JSONFileWizard):
    """Class representing a map."""

    players: int
    style: str
    description: str
    source: str
    layout: Layout
