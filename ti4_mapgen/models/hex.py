from __future__ import annotations

from typing import Literal, NamedTuple, Optional, overload

from bidict import bidict


CardinalDirection = Literal[
    "SE",
    "S",
    "SW",
    "NW",
    "N",
    "NE",
]


class CubePosition(NamedTuple):
    "A cube representation of a position in a hexagonal grid."
    q: int
    r: int
    s: int


class CubeVector(NamedTuple):
    "A cube representation of a vector in a hexagonal grid."
    q: int
    r: int
    s: int


_CARDINAL_TO_VECTOR: bidict[CardinalDirection, CubeVector] = bidict(
    {
        "SE": CubeVector(1, 0, -1),
        "S": CubeVector(0, 1, -1),
        "SW": CubeVector(-1, 1, 0),
        "NW": CubeVector(-1, 0, 1),
        "N": CubeVector(0, -1, 1),
        "NE": CubeVector(1, -1, 0),
    }
)


@overload
def add(a: CubePosition, b: CubePosition) -> CubePosition:
    ...


@overload
def add(a: CubePosition, b: CubeVector) -> CubePosition:
    ...


@overload
def add(a: CubeVector, b: CubeVector) -> CubeVector:
    ...


def add(a: CubePosition | CubeVector, b: CubePosition | CubeVector) -> CubePosition | CubeVector:
    """Add a cube position or a cube vector to a cube vector."""
    if isinstance(a, CubeVector) and isinstance(b, CubeVector):
        return CubeVector(a.q + b.q, a.r + b.r, a.s + b.s)

    return CubePosition(a.q + b.q, a.r + b.r, a.s + b.s)


@overload
def subtract(a: CubePosition, b: CubePosition) -> CubeVector:
    ...


@overload
def subtract(a: CubePosition, b: CubeVector) -> CubePosition:
    ...


@overload
def subtract(a: CubeVector, b: CubeVector) -> CubeVector:
    ...


def subtract(a: CubePosition | CubeVector, b: CubePosition | CubeVector) -> CubePosition | CubeVector:
    """Subtract a cube position or a cube vector from a cube position."""
    if isinstance(a, CubePosition) and isinstance(b, CubeVector):
        return CubePosition(a.q - b.q, a.r - b.r, a.s - b.s)

    return CubeVector(a.q - b.q, a.r - b.r, a.s - b.s)


@overload
def scale(a: CubePosition, scalar: int) -> CubePosition:
    ...


@overload
def scale(a: CubeVector, scalar: int) -> CubeVector:
    ...


def scale(a: CubePosition | CubeVector, scalar: int) -> CubePosition | CubeVector:
    """Scale a cube position or cube vector by a scalar."""
    return CubePosition(a.q * scalar, a.r * scalar, a.s * scalar)


def find_vector_from_cardinal(direction: CardinalDirection) -> CubeVector:
    """Find the cube vector corresponding to a cardinal direction."""
    return _CARDINAL_TO_VECTOR[direction]


def find_cardinal_from_vector(vector: CubeVector) -> CardinalDirection:
    """Find the cardinal direction corresponding to a cube vector."""
    return _CARDINAL_TO_VECTOR.inv[vector]


def find_adjacent(a: CubePosition, direction: CardinalDirection) -> CubePosition:
    """Find neighbor cube position in cardinal direction or cube vector from cube position."""
    if isinstance(direction, CardinalDirection):
        vector = find_vector_from_cardinal(direction)
    elif isinstance(direction, CubeVector):
        vector = direction

    return add(a, vector)


def ring(center: CubePosition, radius: int) -> list[CubePosition]:
    """Calculate all positions on a ring which is radius distance from the center position."""
    vector = find_vector_from_cardinal("NW")
    scaled_vector = scale(vector, radius)
    position = add(center, scaled_vector)

    results: list[CubePosition] = []

    for cardinal_direction in _CARDINAL_TO_VECTOR.keys():
        for _ in range(radius):
            results.append(position)
            position = find_adjacent(position, cardinal_direction)

    return results


def _rotate_left(a: CubeVector) -> CubeVector:
    """Rotate a cube vector counterclockwise."""
    return CubeVector(-a.s, -a.q, -a.r)


def _rotate_right(a: CubeVector) -> CubeVector:
    """Rotate a cube vector clockwise."""
    return CubeVector(-a.r, -a.s, -a.q)


def rotate(a: CubePosition | CubeVector, center: CubePosition, angle: int = 0) -> CubePosition:
    """Rotate a cube position around a center position."""

    # Check if 'angle' is divisible by 60, if not raise an error.
    if 360 % angle != 0:
        raise ValueError("Argument 'angle' must be in 60 degree increments")

    if isinstance(a, CubePosition):
        vector = subtract(a, center)
    elif isinstance(a, CubeVector):
        vector = a

    steps = int((angle % 360) / 60)

    if steps == 0:
        pass
    elif steps > 0:
        *_, vector = tuple(_rotate_right(vector) for _ in range(steps))
    elif steps < 0:
        *_, vector = tuple(_rotate_left(vector) for _ in range(steps))

    return add(center, vector)


def calculate_length(a: CubeVector) -> int:
    """Calculate the length of a cube vector."""
    return abs(a.q) + abs(a.r) + abs(a.s) // 2

