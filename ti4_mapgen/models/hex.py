from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from collections.abc import Iterator, Sequence
from typing import overload


@dataclass(frozen=True, slots=True)
class Cube:
    "A cube representation of a position or vector in a hexagonal grid."
    q: int
    r: int
    s: int

    def __post_init__(self):
        # Perform sanity check on coordinate.
        assert self.q + self.r + self.s == 0, "Sum of 'q', 'r', 's' must be 0"

    def __add__(self, other: Cube) -> Cube:
        if not isinstance(other, Cube):
            raise NotImplementedError
        return Cube(self.q + other.q, self.r + other.r, self.s + other.s)

    def __sub__(self, other: Cube) -> Cube:
        if not isinstance(other, Cube):
            raise NotImplementedError
        return Cube(self.q - other.q, self.r - other.r, self.s - other.s)

    def __mul__(self, other: int):
        if not isinstance(other, int):
            raise NotImplementedError
        return Cube(self.q * other, self.r * other, self.s * other)

    def __floordiv__(self, other: Cube | int):
        if not isinstance(other, int):
            raise NotImplementedError
        return Cube(int(self.q / other), int(self.r / other), int(self.s / other))

    def __abs__(self) -> int:
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2


class Direction(Enum):
    N = Cube(0, -1, 1)
    NE = Cube(1, -1, 0)
    SE = Cube(1, 0, -1)
    S = Cube(0, 1, -1)
    SW = Cube(-1, 1, 0)
    NW = Cube(-1, 0, 1)


class Diagonal(Enum):
    E = Cube(2, -1, -1)
    NNE = Cube(1, -2, 1)
    NNW = Cube(-1, -1, 2)
    W = Cube(-2, 1, 1)
    SSW = Cube(-1, 2, -1)
    SSE = Cube(1, 1, -2)


class Move(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


def adjacent(a: Cube, direction: Direction) -> Cube:
    """Find an adjacent cube position in direction from initial cube position."""
    return a + direction.value


def diagonal(a: Cube, direction: Diagonal) -> Cube:
    """Find a diagonal cube position in direction from initial cube position."""
    return a + direction.value


def ring(
    center: Cube, radius: int, *, direction: Direction = Direction.N, move: Move = Move.CLOCKWISE
) -> Iterator[Cube]:
    """Calculate all positions on a ring which is radius distance from a center position.

    The iterator yields cube positions in the ring starting from the passed direction and moving
    around the ring in passed move direction.

    Args:
        center: Cube position in center of ring.
        radius: Ring distance from center position.
        direction (optional): Direction to start from center position. Defaults to Direction.N.
        move (optional): Direction to move around the ring. Defaults to Move.CLOCKWISE.

    Yields:
        Cube position in ring.
    """
    vector = direction.value
    scaled_vector = vector * radius
    position = center + scaled_vector
    neighbors = deque(direction.value for direction in Direction)

    if move is Move.COUNTERCLOCKWISE:
        neighbors.reverse()

    # Rearranges 'neighbors' to the correct order for moving around the ring
    steps = neighbors.index(vector) + 2
    neighbors.rotate(-steps)

    for neighbor in neighbors:
        for _ in range(radius):
            yield position
            position = adjacent(position, Direction(neighbor))


def _rotate_right(a: Cube) -> Cube:
    """Rotate a cube vector counterclockwise."""
    return Cube(-a.r, -a.s, -a.q)


def _rotate_left(a: Cube) -> Cube:
    """Rotate a cube vector counterclockwise."""
    return Cube(-a.s, -a.q, -a.r)


def rotate(a: Cube, center: Cube, *, angle: int = 0, move: Move = Move.CLOCKWISE) -> Cube:
    """Rotate a cube position or vector around a center position.

    Args:
        a: Cube position or vector to rotate around a center.
        center (optional): Cube position to use as the center of rotation.
        angle (optional): Degrees to rotate a cube position or vector around the center. Defaults to 0.
        rotate (optional): Direction to perform rotation. Defaults to Move.CLOCKWISE.

    Raises:
        ValueError: If 'angle' is not a positive integer.
        ValueError: If 'angle' is not divisible by 60.

    Returns:
        Rotated cube position.
    """
    # Check if 'angle' is a positive number.
    if angle < 0:
        raise ValueError("Argument 'angle' must be a positive integer.")

    # Check if 'angle' is divisible by 60.
    if angle % 60 != 0:
        raise ValueError("Argument 'angle' must be in 60 degree increments")

    vector = a - center
    steps = (angle % 360) // 60

    for _ in range(steps):
        if move is Move.CLOCKWISE:
            vector = _rotate_right(vector)
        elif move is Move.COUNTERCLOCKWISE:
            vector = _rotate_left(vector)

    return center + vector


def length(a: Cube) -> int:
    """Calculate the length of a cube vector."""
    return abs(a)


def distance(a: Cube, b: Cube) -> int:
    """Find the distance between two cube positions."""
    return length(a - b)


def spiral(
    center: Cube, radius: int, *, direction: Direction = Direction.N, move: Move = Move.CLOCKWISE
) -> Iterator[Cube]:
    """Calculate all positions in a spiral pattern which is radius distance from a center position.

    Args:
        center: Cube position in center of spiral.
        radius: Spiral distance from center position.
        direction (optional): Direction to start from center position. Defaults to "Direction.N".
        clockwise (optional): Direction to move around the spiral. Defaults to Rotate.CLOCKWISE.

    Yields:
        Cube position in spiral.
    """

    yield center

    radiuses = range(1, radius + 1)
    for radius in radiuses:
        for position in ring(center, radius, direction=direction, move=move):
            yield position
