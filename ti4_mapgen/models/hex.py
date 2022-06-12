from __future__ import annotations

from typing import Literal, NamedTuple, overload

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
        "N": CubeVector(0, -1, 1),
        "NE": CubeVector(1, -1, 0),
        "SE": CubeVector(1, 0, -1),
        "S": CubeVector(0, 1, -1),
        "SW": CubeVector(-1, 1, 0),
        "NW": CubeVector(-1, 0, 1),
    }
)

_INDEX_TO_VECTOR: bidict[int, CubeVector] = bidict(
    {
        0: CubeVector(0, -1, 1),  # N
        1: CubeVector(1, -1, 0),  # NE
        2: CubeVector(1, 0, -1),  # SE
        3: CubeVector(0, 1, -1),  # S
        4: CubeVector(-1, 1, 0),  # SW
        5: CubeVector(-1, 0, 1),  # NW
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


def vector_from_cardinal(direction: CardinalDirection) -> CubeVector:
    """Find the cube vector corresponding to a cardinal direction."""
    return _CARDINAL_TO_VECTOR[direction]


def cardinal_from_vector(vector: CubeVector) -> CardinalDirection:
    """Find the cardinal direction corresponding to a cube vector."""
    return _CARDINAL_TO_VECTOR.inv[vector]


def vector_from_index(index: int) -> CubeVector:
    """Find the cube vector corresponding to an index."""
    return _INDEX_TO_VECTOR[index]


def index_from_vector(vector: CubeVector) -> int:
    """Find the index corresponding to a cube vector."""
    return _INDEX_TO_VECTOR.inv[vector]


def adjacent(a: CubePosition, direction: CardinalDirection | CubeVector) -> CubePosition:
    """Find neighbor cube position in cardinal direction or cube vector from cube position."""
    if isinstance(direction, str):
        vector = vector_from_cardinal(direction)
    elif isinstance(direction, CubeVector):
        vector = direction
    else:
        raise ValueError("Argument 'direction' must be 'CubeVector' or 'str'")

    return add(a, vector)


def ring(
    center: CubePosition, radius: int, direction: CardinalDirection = "N", clockwise: bool = True
) -> list[CubePosition]:
    """Calculate all positions on a ring which is radius distance from the center position."""
    vector = vector_from_cardinal(direction)
    scaled_vector = scale(vector, radius)
    position = add(center, scaled_vector)
    cardinal_list = list(_CARDINAL_TO_VECTOR.keys())

    if not clockwise:
        cardinal_list.reverse()

    ordinal = cardinal_list.index(direction) + 1

    # Rearranges the cardinal_list to the correct order, dependant on "starting direction".
    for _ in range(1, (ordinal % len(cardinal_list)) + 2):
        cardinal_list.append(cardinal_list.pop(0))

    results: list[CubePosition] = []
    for direction in cardinal_list:
        for _ in range(radius):
            results.append(position)
            position = adjacent(position, direction)

    return results


def _rotate_left(a: CubeVector) -> CubeVector:
    """Rotate a cube vector counterclockwise."""
    return CubeVector(-a.s, -a.q, -a.r)


def _rotate_right(a: CubeVector) -> CubeVector:
    """Rotate a cube vector clockwise."""
    return CubeVector(-a.r, -a.s, -a.q)


def rotate(a: CubePosition | CubeVector, center: CubePosition = CubePosition(0, 0, 0), angle: int = 0) -> CubePosition:
    """Rotate a cube position around a center position."""

    # Check if 'angle' is divisible by 60, if not raise an error.
    if angle % 60 != 0:
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


def length(a: CubeVector) -> int:
    """Calculate the length of a cube vector."""
    return abs(a.q) + abs(a.r) + abs(a.s) // 2


def distance(a: CubePosition, b: CubePosition) -> int:
    """Find the distance between two cube positions."""
    vector = subtract(a, b)
    return length(vector)


def spiral(
    center: CubePosition, radius: int, direction: CardinalDirection = "N", clockwise: bool = True
) -> list[CubePosition]:
    results = [center]
    for i in range(radius + 1):
        results.extend(ring(center, i))
    return results
