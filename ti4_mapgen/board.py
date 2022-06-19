from __future__ import annotations

import random
from copy import deepcopy
from dataclasses import InitVar, dataclass, field
from typing import Optional

from dataclass_wizard import JSONFileWizard, JSONWizard

from ti4_mapgen.typing import Anomaly, Back, Faction, Letter, Release, Tag, Tech, Trait, Wormhole

from .hex import Cube


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


@dataclass(frozen=False)
class Map(JSONWizard, JSONFileWizard):
    """Class representing a map."""

    class _(JSONWizard.Meta):
        skip_defaults = True

    players: int
    style: str
    description: str
    source: str
    layout: dict[Cube, Tile]


@dataclass()
class Board(JSONWizard, JSONFileWizard):
    """Class representing a board."""

    map: InitVar[Map]
    tiles: InitVar[list[Tile]]
    factions: InitVar[list[Faction]]
    layout = None

    def __post_init__(self, map: Map, stack: list[Tile], factions: list[Faction]):
        self.players = map.players
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
