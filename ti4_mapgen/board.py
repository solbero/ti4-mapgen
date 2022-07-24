from __future__ import annotations

import dataclasses
import random

from ti4_mapgen import schemas


@dataclasses.dataclass()
class Board(dataclass_wizard.JSONWizard):
    """Class representing a board."""

    class _(dataclass_wizard.JSONWizard.Meta):
        skip_defaults = True

    layout: list[schemas.Tile]
    stack: list[schemas.Tile]
    homes: dataclasses.InitVar[list[schemas.Tile]]

    def __post_init__(self, homes):
        self._setup(self.layout, self.stack, homes)

    def _setup(self, layout: list[schemas.Tile], stack: list[schemas.Tile], homes: list[schemas.Tile]):
        """Populate the layout with tiles from the stack."""
        for index, tile in enumerate(layout):
            if homes and tile.type is schemas.Type.HOME:
                home_system = homes.pop(0)
                home_system.position = tile.position
                layout[index] = home_system
            elif tile.type is schemas.Type.SYSTEM and stack:
                random_index = random.randint(0, len(stack) - 1)
                system = stack.pop(random_index)
                system.position = tile.position
                layout[index] = system
