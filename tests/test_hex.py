import pytest

from ti4_mapgen.models.hex import (
    Cube,
    Diagonal,
    Direction,
    Move,
    _rotate_left,
    _rotate_right,
    adjacent,
    diagonal,
    ring,
    rotate,
    length,
    distance,
    spiral,
)


def test_hex():
    hex = Cube(0, 0, 0)
    assert hex == Cube(0, 0, 0)


def test_hex_has_attributes():
    hex = Cube(0, 0, 0)
    attributes = ("q", "r", "s")

    for attribute in attributes:
        assert hasattr(hex, attribute) == True


def test_hex_attributes_access():
    hex = Cube(0, 1, -1)
    assert hex.q == 0
    assert hex.r == 1
    assert hex.s == -1


def test_hex_raises():
    with pytest.raises(AssertionError) as exec_info:
        Cube(0, 1, 1)
    msg, *_ = exec_info.value.args
    assert msg == "Sum of 'q', 'r', 's' must be 0"


def test_hex_add():
    sum = Cube(0, -1, 1) + Cube(0, 1, -1)
    assert sum == Cube(0, 0, 0)


def test_hex_sub():
    diff = Cube(0, -1, 1) - Cube(0, 1, -1)
    assert diff == Cube(0, -2, 2)


def test_hex_mul():
    prod = Cube(0, -1, 1) * 2
    assert prod == Cube(0, -2, 2)


def test_hex_floordiv():
    quot_1 = Cube(0, -2, 2) // 2
    assert quot_1 == Cube(0, -1, 1)

    quot_2 = Cube(0, -1, 1) // 2
    assert quot_2 == Cube(0, 0, 0)


def test_hex_abs():
    hex_1 = Cube(0, -1, 1)
    assert abs(hex_1) == 1

    hex_2 = Cube(0, -4, 4)
    assert abs(hex_2) == 4


def test_hex_adjacent():
    hex = Cube(0, 0, 0)
    for direction in Direction:
        assert adjacent(hex, direction) == direction.value


def test_hex_diagonal():
    hex = Cube(0, 0, 0)
    for direction in Diagonal:
        assert diagonal(hex, direction) == direction.value


def test_hex_ring_radius():
    center = Cube(0, 0, 0)
    radius_0 = 0
    ring_ = ring(center, radius_0)
    assert tuple(ring_) == ()

    center = Cube(0, 0, 0)
    radius_1 = 1
    ring_ = ring(center, radius_1)
    assert tuple(ring_) == (
        Cube(0, -1, 1),
        Cube(1, -1, 0),
        Cube(1, 0, -1),
        Cube(0, 1, -1),
        Cube(-1, 1, 0),
        Cube(-1, 0, 1),
    )

    radius_2 = 2
    ring_ = ring(center, radius_2)
    assert tuple(ring_) == (
        Cube(0, -2, 2),
        Cube(1, -2, 1),
        Cube(2, -2, 0),
        Cube(2, -1, -1),
        Cube(2, 0, -2),
        Cube(1, 1, -2),
        Cube(0, 2, -2),
        Cube(-1, 2, -1),
        Cube(-2, 2, 0),
        Cube(-2, 1, 1),
        Cube(-2, 0, 2),
        Cube(-1, -1, 2),
    )


def test_hex_ring_len():
    center = Cube(0, 0, 0)
    radius_1 = 1
    ring_1 = ring(center, radius_1)
    assert sum(1 for _ in ring_1) == 6

    radius_2 = 2
    ring_2 = ring(center, radius_2)
    assert sum(1 for _ in ring_2) == 12


def test_hex_ring_center():
    center = Cube(0, -1, 1)
    radius = 1
    ring_ = ring(center, radius)
    assert tuple(ring_) == (
        Cube(0, -2, 2),
        Cube(1, -2, 1),
        Cube(1, -1, 0),
        Cube(0, 0, 0),
        Cube(-1, 0, 1),
        Cube(-1, -1, 2),
    )


def test_hex_ring_direction():
    center = Cube(0, 0, 0)
    radius = 1
    direction = Direction.S
    ring_ = ring(center, radius, direction=direction)
    assert tuple(ring_) == (
        Cube(0, 1, -1),
        Cube(-1, 1, 0),
        Cube(-1, 0, 1),
        Cube(0, -1, 1),
        Cube(1, -1, 0),
        Cube(1, 0, -1),
    )


def test_hex_ring_rotate():
    center = Cube(0, 0, 0)
    radius = 1
    move = Move.COUNTERCLOCKWISE
    ring_ = ring(center, radius, move=move)
    assert tuple(ring_) == (
        Cube(0, -1, 1),
        Cube(-1, 0, 1),
        Cube(-1, 1, 0),
        Cube(0, 1, -1),
        Cube(1, 0, -1),
        Cube(1, -1, 0),
    )


def test_rotate_right():
    hex = Cube(0, -1, 1)
    assert _rotate_right(hex) == Cube(1, -1, 0)


def test_rotate_left():
    hex = Cube(0, -1, 1)
    assert _rotate_left(hex) == Cube(-1, 0, 1)


def test_rotate():
    hex = Cube(0, -2, 2)
    center = Cube(0, 0, 0)
    assert rotate(hex, center) == Cube(0, -2, 2)


def test_rotate_angle_60():
    hex = Cube(0, -2, 2)
    center = Cube(0, 0, 0)
    angle = 60
    assert rotate(hex, center, angle=angle) == Cube(2, -2, 0)


def test_rotate_center_angle_60():
    hex = Cube(0, -3, 3)
    center = Cube(0, -1, 1)
    angle = 60
    assert rotate(hex, center, angle=angle) == Cube(2, -3, 1)


def test_rotate_angle_60_counterclockwise():
    hex = Cube(0, -2, 2)
    center = Cube(0, 0, 0)
    angle = 60
    move = Move.COUNTERCLOCKWISE
    assert rotate(hex, center, angle=angle, move=move) == Cube(-2, 0, 2)


def test_rotate_raises_negative_angle():
    hex = Cube(0, -2, 2)
    center = Cube(0, 0, 0)
    angle = -60
    with pytest.raises(ValueError) as exec_info:
        rotate(hex, center, angle=angle)
    msg, *_ = exec_info.value.args
    assert msg == "Argument 'angle' must be a positive integer."


def test_rotate_raises_angle_increment():
    hex = Cube(0, -2, 2)
    center = Cube(0, 0, 0)
    angle = 30
    with pytest.raises(ValueError) as exec_info:
        rotate(hex, center, angle=angle)
    msg, *_ = exec_info.value.args
    assert msg == "Argument 'angle' must be in 60 degree increments"


def test_length():
    vector_1 = Cube(0, 0, 0)
    assert length(vector_1) == 0

    vector_2 = Cube(0, -3, 3)
    assert length(vector_2) == 3


def test_distance():
    hex_1 = Cube(0, 0, 0)
    assert distance(hex_1, hex_1) == 0

    hex_2 = Cube(0, -3, 3)
    assert distance(hex_1, hex_2) == 3

    hex_3 = Cube(0, 3, -3)
    assert distance(hex_2, hex_3) == 6

    hex_4 = Cube(3, -3, 0)
    assert distance(hex_3, hex_4) == 6


def test_spiral_radius():
    center = Cube(0, 0, 0)
    radius_0 = 0
    assert tuple(spiral(center, radius=radius_0)) == (Cube(0, 0, 0),)

    radius_1 = 1
    assert tuple(spiral(center, radius=radius_1)) == (
        Cube(0, 0, 0),
        Cube(0, -1, 1),
        Cube(1, -1, 0),
        Cube(1, 0, -1),
        Cube(0, 1, -1),
        Cube(-1, 1, 0),
        Cube(-1, 0, 1),
    )

    radius_2 = 2
    assert tuple(spiral(center, radius=radius_2)) == (
        Cube(0, 0, 0),
        Cube(0, -1, 1),
        Cube(1, -1, 0),
        Cube(1, 0, -1),
        Cube(0, 1, -1),
        Cube(-1, 1, 0),
        Cube(-1, 0, 1),
        Cube(0, -2, 2),
        Cube(1, -2, 1),
        Cube(2, -2, 0),
        Cube(2, -1, -1),
        Cube(2, 0, -2),
        Cube(1, 1, -2),
        Cube(0, 2, -2),
        Cube(-1, 2, -1),
        Cube(-2, 2, 0),
        Cube(-2, 1, 1),
        Cube(-2, 0, 2),
        Cube(-1, -1, 2),
    )


def test_spiral_center():
    center = Cube(0, -1, 1)
    radius = 1
    ring_ = spiral(center, radius)
    assert tuple(ring_) == (
        Cube(0, -1, 1),
        Cube(0, -2, 2),
        Cube(1, -2, 1),
        Cube(1, -1, 0),
        Cube(0, 0, 0),
        Cube(-1, 0, 1),
        Cube(-1, -1, 2),
    )


def test_spiral_direction():
    center = Cube(0, 0, 0)
    radius = 1
    direction = Direction.S
    ring_ = spiral(center, radius, direction=direction)
    assert tuple(ring_) == (
        Cube(0, 0, 0),
        Cube(0, 1, -1),
        Cube(-1, 1, 0),
        Cube(-1, 0, 1),
        Cube(0, -1, 1),
        Cube(1, -1, 0),
        Cube(1, 0, -1),
    )
