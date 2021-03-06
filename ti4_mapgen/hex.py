from __future__ import annotations

import enum
from collections import deque
from collections.abc import Iterator

from pydantic import dataclasses


@dataclasses.dataclass(frozen=True)
class Cube:
    "A cube representation of a position or vector in a hexagonal grid."
    q: int
    r: int
    s: int

    def __post_init__(self):
        # Perform sanity check on coordinate.
        if self.q + self.r + self.s != 0:
            raise ValueError(f"attributes 'q', 'r', 's' must have a sum of 0, not {self.q + self.r + self.s}")

    def __add__(self, other) -> Cube:
        if isinstance(other, Cube):
            return Cube(q=self.q + other.q, r=self.r + other.r, s=self.s + other.s)
        raise TypeError("unsupported operand type(s) for +: " + f"{type(self).__name__!r} and {type(other).__name__!r}")

    def __sub__(self, other) -> Cube:
        if isinstance(other, Cube):
            return Cube(q=self.q - other.q, r=self.r - other.r, s=self.s - other.s)
        raise TypeError("unsupported operand type(s) for -: " + f"{type(self).__name__!r} and {type(other).__name__!r}")

    def __mul__(self, other) -> Cube:
        if isinstance(other, int):
            return Cube(q=self.q * other, r=self.r * other, s=self.s * other)
        raise TypeError(f"unsupported operand type(s) for *: {type(self).__name__!r} and {type(other).__name__!r}")

    def __floordiv__(self, other) -> Cube:
        if isinstance(other, int):
            return Cube(q=int(self.q / other), r=int(self.r / other), s=int(self.s / other))
        raise TypeError(f"unsupported operand type(s) for //: {type(self).__name__!r} and {type(other).__name__!r}")

    def __abs__(self) -> int:
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2


class Adjacent(enum.Enum):
    N = Cube(q=0, r=-1, s=1)
    NE = Cube(q=1, r=-1, s=0)
    SE = Cube(q=1, r=0, s=-1)
    S = Cube(q=0, r=1, s=-1)
    SW = Cube(q=-1, r=1, s=0)
    NW = Cube(q=-1, r=0, s=1)


class Diagonal(enum.Enum):
    E = Cube(q=2, r=-1, s=-1)
    NNE = Cube(q=1, r=-2, s=1)
    NNW = Cube(q=-1, r=-1, s=2)
    W = Cube(q=-2, r=1, s=1)
    SSW = Cube(q=-1, r=2, s=-1)
    SSE = Cube(q=1, r=1, s=-2)


class Move(enum.Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


def adjacent(hex: Cube, *, direction: Adjacent) -> Cube:
    """Find an adjacent cube position in direction from initial cube position."""
    return hex + direction.value


def diagonal(hex: Cube, *, direction: Diagonal) -> Cube:
    """Find a diagonal cube position in direction from initial cube position."""
    return hex + direction.value


def ring(center: Cube, radius: int, *, direction: Adjacent = Adjacent.N, move: Move = Move.CLOCKWISE) -> Iterator[Cube]:
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
    neighbors = deque(direction.value for direction in Adjacent)

    if move is Move.COUNTERCLOCKWISE:
        neighbors.reverse()

    # Rearranges 'neighbors' to the correct order for moving around the ring
    steps = neighbors.index(vector) + 2
    neighbors.rotate(-steps)

    for neighbor in neighbors:
        for _ in range(radius):
            yield position
            position = adjacent(position, direction=Adjacent(neighbor))


def _rotate_clockwise(hex: Cube) -> Cube:
    """Rotate a cube vector counterclockwise."""
    return Cube(q=-hex.r, r=-hex.s, s=-hex.q)


def _rotate_counterclockwise(hex: Cube) -> Cube:
    """Rotate a cube vector counterclockwise."""
    return Cube(q=-hex.s, r=-hex.q, s=-hex.r)


def rotate(hex: Cube, center: Cube, *, angle: int) -> Cube:
    """Rotate a cube position or vector around a center position.

    Note:
        If argument 'angle' is positive rotation is clockwise, if negative rotation is counterclockwise.

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
        raise ValueError("argument 'angle' must be in 60 degree increments")

    vector = hex - center
    steps = abs((angle % 360) // 60)

    if angle > 0:
        *_, vector = (_rotate_clockwise(vector) for _ in range(steps))
    elif angle < 0:
        *_, vector = (_rotate_counterclockwise(vector) for _ in range(steps))

    return center + vector


def length(hex: Cube) -> int:
    """Calculate the length of a cube vector."""
    return abs(hex)


def distance(hex1: Cube, hex2: Cube) -> int:
    """Find the distance between two cube positions."""
    return length(hex1 - hex2)


def spiral(
    center: Cube, radius: int, *, direction: Adjacent = Adjacent.N, move: Move = Move.CLOCKWISE
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
