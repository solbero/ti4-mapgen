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
    homes: dataclasses.InitVar[list[schema.Tile]]

    def __post_init__(self, homes):
        self._setup(self.layout, self.stack, homes)

    def _setup(self, layout: list[schema.Tile], stack: list[schema.Tile], homes: list[schema.Tile]):
        """Populate the layout with tiles from the stack."""
        for index, tile in enumerate(layout):
            if homes and tile.tag is schema.Tag.HOME:
                home_system = homes.pop(0)
                home_system.position = tile.position
                layout[index] = home_system
            elif tile.tag is schema.Tag.SYSTEM and stack:
                random_index = random.randint(0, len(stack) - 1)
                system = stack.pop(random_index)
                system.position = tile.position
                layout[index] = system
