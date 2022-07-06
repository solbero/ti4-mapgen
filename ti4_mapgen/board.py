from __future__ import annotations

import dataclasses
import random
from typing import Optional

import dataclass_wizard

from ti4_mapgen import schema


@dataclasses.dataclass()
class Board(dataclass_wizard.JSONWizard):
    """Class representing a board."""

    class _(dataclass_wizard.JSONWizard.Meta):
        skip_defaults = True

    layout: list[schema.Tile]
    stack: list[schema.Tile]
    home_system_tiles: dataclasses.InitVar[list[schema.Tile]]

    def __post_init__(self, home_systems):
        random.shuffle(self.stack)
        self._setup(self.layout, self.stack, home_systems)

    def _setup(self, layout: list[schema.Tile], stack: list[schema.Tile], home_system_tiles: list[schema.Tile]):
        """Populate the layout with tiles from the stack."""
        for index, tile in enumerate(layout):
            if tile.tag is schema.Tag.HOME and home_system_tiles:
                home_system = home_system_tiles.pop(0)
                home_system.position = tile.position
                layout[index] = home_system
            elif tile.tag is schema.Tag.SYSTEM and stack:
                system = stack.pop(0)
                system.position = tile.position
                layout[index] = system
