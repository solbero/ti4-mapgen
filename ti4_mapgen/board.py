from __future__ import annotations

import dataclasses

import random
from copy import deepcopy
from typing import Optional

import dataclass_wizard

from ti4_mapgen.typing import Faction


@dataclass()
class Board(JSONWizard, JSONFileWizard):
    """Class representing a board."""

    map: dataclasses.InitVar[Map]
    tiles: dataclasses.InitVar[list[Tile]]
    factions: dataclasses.InitVar[list[Faction]]

    def __post_init__(self, map: Map, stack: list[Tile], factions: list[Faction]):
        self.players = map.no_players
        self.style = map.style
        self.layout = deepcopy(map.layout)
        self._setup_board()

    def _setup_board(self):
        """Populate the board with systems."""
        # Place the Mecatol Rex system (#18) in the center of the board
        self.immutable_board[self.layout.center] = self.tiles.pop(
            self.tiles.index(next(tile for tile in self.tiles if tile.number == 18))
        )

        for value in self.layout.homes.values():
            self.immutable_board[value] = None

        """self.layout.center = self.stack.pop(self.stack.index(next(tile for tile in self.stack if tile.number == 18)))
        board.append(center_position)"""

        # Assign a random system to every system tile.
        for tile in self.tiles:
            # Select a random system from the list of unassigned systems.
            selected_system = random.choice(self.unassigned_tiles)
            # Remove the selected system from the list of unassigned systems and assign the system to the current tile.
            self.unassigned_tiles.remove(selected_system)
            tile.system = selected_system

    def mutate(self, prob_func: Optional[Callable] = None) -> None:
        # If no probability function is passed to the method, use a default probability function.
        if prob_func is None:
            # The probability of mutating a tile is '1/n', where 'n' is the number of possible tiles to mutate.
            prob_func = lambda collection: random.randint(1, len(collection)) == 1

        # Iterate over all the system tiles.
        for tile in self.mutable_tiles:
            # Use the probability function to check if a tile is mutated.
            if prob_func(self.mutable_tiles):
                # Select a random system from the list of unassigned systems.
                selected_system = random.choice(self.unassigned_tiles)
                # Switch the current system with the selected system.
                tile.system, selected_system = selected_system, tile.system
