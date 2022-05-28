from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass()
class Cube:
    """Class representing a position in a hexagonal grid as a cube coordinate."""

    q: int
    r: int
    s: int

    def __post__init__(self) -> None:
        # Perfor sanity check on cube coordinate
        assert sum((self.q, self.r, self.s)) == 0

    @staticmethod
    def add(a: Cube, b: Cube) -> Cube:
        """Add two positions in a hexagonal grid."""
        return Cube(a.q + b.q, a.r + b.r, a.s + b.s)

    @staticmethod
    def rotate(a: Cube, center: Cube, angle: int = 0) -> Cube:
        """Rotate a position in a hexagonal grid around a center."""

        # Check if 'angle' is divisible by 60, if not raise an error.
        if 360 % angle != 0:
            raise ValueError("Argument 'angle' must be in 60 degree increments")

        # See https://www.redblobgames.com/grids/hexagons/implementation.html#rotation for for an explantion of
        # the implementation.

        # Create a multiplication array for rotation.
        m = np.array([[0, 0, -1], [-1, 0, 0], [0, -1, 0]])
        # Number of 60 degree steps to rotate.
        k = int((angle % 360) / 60)
        # Calculate cube vector from position to center.
        vec = np.array([[a.q - center.q], [a.r - center.r], [a.s - center.s]])

        # If 'angle' is negative inverse the multiplication array. This allows the position to rotate left or right
        # around the center.
        if k < 0:
            m = np.linalg.inv(m)

        # Calculate the rotated cube vector.
        rotated_vec = Cube(*np.multiply(vec, m ** abs(k)))

        # Add the rotated vector to the original position to get the rotated position.
        return Cube.add(center, rotated_vec)
