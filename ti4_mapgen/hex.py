from __future__ import annotations

import dataclasses
import enum
from collections import deque
from collections.abc import Iterator
from typing import Iterable, Mapping


@dataclasses.dataclass(frozen=True, slots=True)
class Cube:
    "A cube representation of a position or vector in a hexagonal grid."
    q: int
    r: int
    s: int

    def __post_init__(self):
        # Perform sanity check on coordinate.
        if self.q + self.r + self.s != 0:
            raise ValueError("Sum of 'q', 'r', 's' must be 0")

    def __add__(self, cube) -> Cube:
        match cube:
            case Cube(q, r, s) | (q, r, s) | {"q": q, "r": r, "s": s}:
                return Cube(self.q + q, self.r + r, self.s + s)
        raise TypeError(f"Unsupported operand type(s) for +: '{type(self)}' and '{type(cube)}'")

    def __sub__(self, cube) -> Cube:
        match cube:
            case Cube(q, r, s) | (q, r, s) | {"q": q, "r": r, "s": s}:
                return Cube(self.q - q, self.r - r, self.s - s)
        raise TypeError(f"Unsupported operand type(s) for -: '{type(self)}' and '{type(cube)}'")

    def __mul__(self, scalar) -> Cube:
        if isinstance(scalar, int):
            return Cube(self.q * scalar, self.r * scalar, self.s * scalar)
        raise TypeError(f"Unsupported operand type(s) for *: '{type(self)}' and '{type(scalar)}'")

    def __floordiv__(self, scalar) -> Cube:
        if isinstance(scalar, int):
            return Cube(int(self.q / scalar), int(self.r / scalar), int(self.s / scalar))
        raise TypeError(f"Unsupported operand type(s) for //: '{type(self)}' and '{type(scalar)}'")

    def __abs__(self) -> int:
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2


class Direction(enum.Enum):
    N = Cube(0, -1, 1)
    NE = Cube(1, -1, 0)
    SE = Cube(1, 0, -1)
    S = Cube(0, 1, -1)
    SW = Cube(-1, 1, 0)
    NW = Cube(-1, 0, 1)


class Diagonal(enum.Enum):
    E = Cube(2, -1, -1)
    NNE = Cube(1, -2, 1)
    NNW = Cube(-1, -1, 2)
    W = Cube(-2, 1, 1)
    SSW = Cube(-1, 2, -1)
    SSE = Cube(1, 1, -2)


class move(enum.Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


def adjacent(hex: Cube, *, direction: Direction) -> Cube:
    """Find an adjacent cube position in direction from initial cube position."""
    return hex + direction.value


def diagonal(hex: Cube, *, direction: Diagonal) -> Cube:
    """Find a diagonal cube position in direction from initial cube position."""
    return hex + direction.value


def ring(
    center: Cube, radius: int, *, direction: Direction = Direction.N, move: move = move.CLOCKWISE
) -> Iterator[Cube]:
    """Calculate all positions on a ring which is radius distance from a center position.

    The iterator yields cube positions in the ring starting from the passed direction and moving
    around the ring in passed move direction.

    Args:
        center: Cube position in center of ring.
        radius: Ring distance from center position.
        direction (optional): Direction to start from center position.
        move (optional): Direction to move around the ring.

    Yields:
        Cube position in ring.
    """
    vector = direction.value
    scaled_vector = vector * radius
    position = center + scaled_vector
    neighbors = deque(direction.value for direction in Direction)

    if move is move.COUNTERCLOCKWISE:
        neighbors.reverse()

    # Rearranges 'neighbors' to the correct order for moving around the ring
    steps = neighbors.index(vector) + 2
    neighbors.rotate(-steps)

    for neighbor in neighbors:
        for _ in range(radius):
            yield position
            position = adjacent(position, direction=Direction(neighbor))


def _rotate_clockwise(hex: Cube) -> Cube:
    """Rotate a cube vector counterclockwise."""
    return Cube(-hex.r, -hex.s, -hex.q)


def _rotate_counterclockwise(hex: Cube) -> Cube:
    """Rotate a cube vector counterclockwise."""
    return Cube(-hex.s, -hex.q, -hex.r)


def rotate(hex: Cube, center: Cube, *, angle: int) -> Cube:
    """Rotate a cube position or vector around a center position.

    Args:
        hex: Cube position or vector to rotate around a center.
        center: Cube position to use as the center of rotation.
        angle: Degrees to rotate a cube position or vector around the center.

    Raises:
        ValueError: If 'angle' is not divisible by 60.

    Returns:
        Rotated cube position.
    """

    # Check if 'angle' is divisible by 60.
    if angle % 60 != 0:
        raise ValueError("Argument 'angle' must be in 60 degree increments")

    vector = hex - center
    steps = abs((angle % 360) // 60)

    if angle > 0:
        *_, vector = [_rotate_clockwise(vector) for _ in range(steps)]
    elif angle < 0:
        *_, vector = [_rotate_counterclockwise(vector) for _ in range(steps)]

    return center + vector


def length(hex: Cube) -> int:
    """Calculate the length of a cube vector."""
    return abs(hex)


def distance(hex1: Cube, hex2: Cube) -> int:
    """Find the distance between two cube positions."""
    return length(hex1 - hex2)


def spiral(
    center: Cube, radius: int, *, direction: Direction = Direction.N, move: move = move.CLOCKWISE
) -> Iterator[Cube]:
    """Calculate all positions in a spiral pattern which is radius distance from a center position.

    Args:
        center: Cube position in center of spiral.
        radius: Spiral distance from center position.
        direction (optional): Direction to start from center position.
        clockwise (optional): Direction to move around the spiral.

    Yields:
        Cube position in spiral.
    """

    yield center

    radiuses = range(1, radius + 1)
    for radius in radiuses:
        for position in ring(center, radius, direction=direction, move=move):
            yield position
