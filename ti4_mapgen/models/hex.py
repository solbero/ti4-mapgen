from __future__ import annotations

from dataclasses import dataclass


@dataclass()
class Cube:
    """Class representing a position in a hexagonal grid as a cube coordinate."""

    q: int
    r: int
    s: int

    def __post__init__(self) -> None:
        # Perfor sanity check on cube coordinate
        assert sum((self.q, self.r, self.s)) == 0
