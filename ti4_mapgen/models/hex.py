from __future__ import annotations

from typing import Literal, NamedTuple, Optional

from bidict import bidict


CardinalDirection = Literal[
    "SE",
    "S",
    "SW",
    "NW",
    "N",
    "NE",
]


class Cube(NamedTuple):
    "A cube representation of a position or vector in a hexagonal grid."
    q: int
    r: int
    s: int


_CARDINAL_TO_VECTOR: bidict[CardinalDirection, Cube] = bidict(
    {
        "N": Cube(0, -1, 1),
        "NE": Cube(1, -1, 0),
        "SE": Cube(1, 0, -1),
        "S": Cube(0, 1, -1),
        "SW": Cube(-1, 1, 0),
        "NW": Cube(-1, 0, 1),
    }
)

_INDEX_TO_VECTOR: bidict[int, Cube] = bidict(
    {
        0: Cube(0, -1, 1),  # N
        1: Cube(1, -1, 0),  # NE
        2: Cube(1, 0, -1),  # SE
        3: Cube(0, 1, -1),  # S
        4: Cube(-1, 1, 0),  # SW
        5: Cube(-1, 0, 1),  # NW
    }
)


def add(a: Cube, b: Cube) -> Cube:
    """Add a cube position or vector to a cube position or vector."""
    return Cube(a.q + b.q, a.r + b.r, a.s + b.s)


def subtract(a: Cube, b: Cube) -> Cube:
    """Subtract a cube position vector from a cube position or vector."""
    return Cube(a.q - b.q, a.r - b.r, a.s - b.s)


def scale(a: Cube, scalar: int) -> Cube:
    """Scale a cube position or vector by a scalar."""
    return Cube(a.q * scalar, a.r * scalar, a.s * scalar)


def vector_from_cardinal(direction: CardinalDirection) -> Cube:
    """Find the cube vector corresponding to a cardinal direction."""
    return _CARDINAL_TO_VECTOR[direction]


def cardinal_from_vector(vector: Cube) -> CardinalDirection:
    """Find the cardinal direction corresponding to a cube vector."""
    return _CARDINAL_TO_VECTOR.inv[vector]


def vector_from_index(index: int) -> Cube:
    """Find the cube vector corresponding to an index."""
    return _INDEX_TO_VECTOR[index]


def index_from_vector(vector: Cube) -> int:
    """Find the index corresponding to a cube vector."""
    return _INDEX_TO_VECTOR.inv[vector]


def adjacent(a: Cube, direction: CardinalDirection | Cube) -> Cube:
    """Find a neighbor cube position in cardinal direction or cube vector direction from initial cube position."""
    if isinstance(direction, str):
        vector = vector_from_cardinal(direction)
    elif isinstance(direction, Cube):
        vector = direction
    else:
        raise ValueError("Argument 'direction' must be 'Cube' or 'CardinalDirection'")

    return add(a, vector)


def ring(center: Cube, radius: int, direction: CardinalDirection = "N", clockwise: bool = True) -> list[Cube]:
    """Calculate all positions on a ring which is radius distance from the center position."""
    vector = vector_from_cardinal(direction)
    scaled_vector = scale(vector, radius)
    position = add(center, scaled_vector)
    cardinal_directions = list(_CARDINAL_TO_VECTOR.keys())

    if not clockwise:
        cardinal_directions.reverse()

    # Rearranges 'cardinal_directions' to the correct order for circeling around a ring, dependant on 'direction'
    dividend = cardinal_directions.index(direction) + 1
    divisor = len(cardinal_directions)
    for _ in range(1, dividend % divisor + 2):
        first_element = cardinal_directions.pop(0)
        cardinal_directions.append(first_element)

    results: list[Cube] = []
    for direction in cardinal_directions:
        for _ in range(radius):
            results.append(position)
            position = adjacent(position, direction)

    return results


def _rotate_left(a: Cube) -> Cube:
    """Rotate a cube vector counterclockwise."""
    return Cube(-a.s, -a.q, -a.r)


def _rotate_right(a: Cube) -> Cube:
    """Rotate a cube vector clockwise."""
    return Cube(-a.r, -a.s, -a.q)


def rotate(a: Cube, center: Optional[Cube] = None, angle: int = 0) -> Cube:
    """Rotate a cube position or vector around a center position."""
    if not center:
        center = Cube(0, 0, 0)

    vector = subtract(a, center)

    # Check if 'angle' is divisible by 60, if not raise an error.
    if angle % 60 != 0:
        raise ValueError("Argument 'angle' must be in 60 degree increments")

    steps = int((angle % 360) / 60)

    if steps > 0:
        *_, vector = tuple(_rotate_right(vector) for _ in range(steps))
    elif steps < 0:
        *_, vector = tuple(_rotate_left(vector) for _ in range(steps))

    return add(center, vector)


def length(a: Cube) -> int:
    """Calculate the length of a cube vector."""
    return abs(a.q) + abs(a.r) + abs(a.s) // 2


def distance(a: Cube, b: Cube) -> int:
    """Find the distance between two cube positions."""
    vector = subtract(a, b)
    return length(vector)


def spiral(center: Cube, radius: int, direction: CardinalDirection = "N", clockwise: bool = True) -> list[Cube]:
    """Calculate all positions which is radius distance from the center position."""
    results: list[Cube] = []
    results.append(center)

    steps = range(1, radius + 1)
    for step in steps:
        results.extend(ring(center, step, direction, clockwise))

    return results
