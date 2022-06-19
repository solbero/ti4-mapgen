import pytest

from ti4_mapgen.models import hex


class TestHex:
    def test_hex_contains_field(self):
        hex_ = hex.Cube(0, 0, 0)
        assert hasattr(hex_, "q") is True
        assert hasattr(hex_, "r") is True
        assert hasattr(hex_, "s") is True

    def test_hex_field_access(self):
        hex_ = hex.Cube(0, 0, 0)
        assert hex_.q == 0
        assert hex_.r == 0
        assert hex_.s == 0

    def test_hex_raises(self):
        with pytest.raises(AssertionError) as exc_info:
            hex.Cube(1, 0, 1)
        message, *_ = exc_info.value.args
        expected = "Sum of 'q', 'r', 's' must be 0"
        assert message == expected


class TestHexOperators:
    def test_hex_equal(self):
        hex1 = hex.Cube(0, 0, 0)
        hex2 = hex.Cube(0, 0, 0)
        assert hex1 == hex2

    def test_hex_unequal(self):
        hex1 = hex.Cube(0, 0, 0)
        hex2 = hex.Cube(0, 1, -1)
        assert hex1 != hex2

    def test_hex_add(self):
        hex1 = hex.Cube(0, 1, -1)
        hex2 = hex.Cube(0, -1, 1)
        expected = hex.Cube(0, 0, 0)
        assert hex1 + hex2 == expected

    def test_hex_sub(self):
        hex1 = hex.Cube(0, 1, -1)
        hex2 = hex.Cube(0, -1, 1)
        expected = hex.Cube(0, 2, -2)
        assert hex1 - hex2 == expected

    def test_hex_mul(self):
        hex_ = hex.Cube(0, 1, -1)
        expected = hex.Cube(0, 2, -2)
        assert hex_ * 2 == expected

    def test_hex_floordiv(self):
        hex_ = hex.Cube(0, -2, 2)
        expected = hex.Cube(0, -1, 1)
        assert hex_ // 2 == expected

    def test_hex_floordiv_rounding(self):
        hex_ = hex.Cube(0, -1, 1)
        expected = hex.Cube(0, 0, 0)
        assert hex_ // 2 == expected

    def test_hex_abs(self):
        hex_ = hex.Cube(0, -2, 2)
        assert abs(hex_) == 2


class TestNeighbor:
    @pytest.mark.parametrize(
        "direction, expected",
        [
            (hex.Direction.N, hex.Cube(0, -1, 1)),
            (hex.Direction.NE, hex.Cube(1, -1, 0)),
            (hex.Direction.SE, hex.Cube(1, 0, -1)),
            (hex.Direction.S, hex.Cube(0, 1, -1)),
            (hex.Direction.SW, hex.Cube(-1, 1, 0)),
            (hex.Direction.NW, hex.Cube(-1, 0, 1)),
        ],
    )
    def test_hex_adjacent(self, direction, expected):
        hex1 = hex.Cube(0, 0, 0)
        adjacent = hex.adjacent(hex1, direction=direction)
        assert adjacent == expected

    @pytest.mark.parametrize(
        "direction, expected",
        [
            (hex.Diagonal.E, hex.Cube(2, -1, -1)),
            (hex.Diagonal.NNE, hex.Cube(1, -2, 1)),
            (hex.Diagonal.NNW, hex.Cube(-1, -1, 2)),
            (hex.Diagonal.W, hex.Cube(-2, 1, 1)),
            (hex.Diagonal.SSW, hex.Cube(-1, 2, -1)),
            (hex.Diagonal.SSE, hex.Cube(1, 1, -2)),
        ],
    )
    def test_hex_diagonal(self, direction, expected):
        hex_ = hex.Cube(0, 0, 0)
        diagonal = hex.diagonal(hex_, direction=direction)
        assert diagonal == expected


class TestHexRing:
    def test_hex_ring_radius(self):
        center = hex.Cube(0, 0, 0)
        radius = 1
        ring = list(hex.ring(center, radius))
        expected = [
            hex.Cube(0, -1, 1),
            hex.Cube(1, -1, 0),
            hex.Cube(1, 0, -1),
            hex.Cube(0, 1, -1),
            hex.Cube(-1, 1, 0),
            hex.Cube(-1, 0, 1),
        ]
        assert ring == expected

    def test_hex_ring_center(self):
        center = hex.Cube(0, -1, 1)
        radius = 1
        ring = list(hex.ring(center, radius))
        expected = [
            hex.Cube(0, -2, 2),
            hex.Cube(1, -2, 1),
            hex.Cube(1, -1, 0),
            hex.Cube(0, 0, 0),
            hex.Cube(-1, 0, 1),
            hex.Cube(-1, -1, 2),
        ]
        assert ring == expected

    def test_hex_ring_direction(self):
        center = hex.Cube(0, 0, 0)
        radius = 1
        direction = hex.Direction.S
        ring = list(hex.ring(center, radius, direction=direction))
        expected = [
            hex.Cube(0, 1, -1),
            hex.Cube(-1, 1, 0),
            hex.Cube(-1, 0, 1),
            hex.Cube(0, -1, 1),
            hex.Cube(1, -1, 0),
            hex.Cube(1, 0, -1),
        ]
        assert ring == expected

    def test_hex_ring_move(self):
        center = hex.Cube(0, 0, 0)
        radius = 1
        move = hex.move.COUNTERCLOCKWISE
        ring = list(hex.ring(center, radius, move=move))
        expected = [
            hex.Cube(0, -1, 1),
            hex.Cube(-1, 0, 1),
            hex.Cube(-1, 1, 0),
            hex.Cube(0, 1, -1),
            hex.Cube(1, 0, -1),
            hex.Cube(1, -1, 0),
        ]
        assert ring == expected

    def test_hex_ring_len(self):
        center = hex.Cube(0, 0, 0)
        radius = 1
        elements = sum(1 for _ in hex.ring(center, radius))
        expected = 6
        assert elements == expected


class TestHexRotate:
    def test_rotate(self):
        hex_ = hex.Cube(0, -2, 2)
        hex_center = hex.Cube(0, 0, 0)
        angle = 0
        hex_rotated = hex.rotate(hex_, hex_center, angle=angle)
        expected = hex.Cube(0, -2, 2)
        assert hex_rotated == expected

    def test_rotate_angle(self):
        hex_ = hex.Cube(0, -2, 2)
        hex_center = hex.Cube(0, 0, 0)
        angle = 60
        hex_rotated = hex.rotate(hex_, hex_center, angle=angle)
        expected = hex.Cube(2, -2, 0)
        assert hex_rotated == expected

    def test_rotate_angle_counterclockwise(self):
        hex_ = hex.Cube(0, -2, 2)
        hex_center = hex.Cube(0, 0, 0)
        angle = -60
        hex_rotated = hex.rotate(hex_, hex_center, angle=angle)
        expected = hex.Cube(-2, 0, 2)
        assert hex_rotated == expected

    def test_rotate_raises_angle_increment(self):
        hex_ = hex.Cube(0, -2, 2)
        center = hex.Cube(0, 0, 0)
        angle = 30
        with pytest.raises(ValueError) as exc_info:
            hex.rotate(hex_, center, angle=angle)
        message, *_ = exc_info.value.args
        expected = "Argument 'angle' must be in 60 degree increments"
        assert message == expected


class TestHexDistance:
    @pytest.mark.parametrize(
        "vector, expected",
        [
            (hex.Cube(0, 0, 0), 0),
            (hex.Cube(0, -1, 1), 1),
            (hex.Cube(0, -2, 2), 2),
        ],
    )
    def test_length(self, vector, expected):
        length = hex.length(vector)
        assert length == expected

    @pytest.mark.parametrize(
        "hex1, hex2, expected",
        [
            (hex.Cube(0, 0, 0), hex.Cube(0, 0, 0), 0),
            (hex.Cube(0, 0, 0), hex.Cube(0, -3, 3), 3),
            (hex.Cube(0, -3, 3), hex.Cube(0, 3, -3), 6),
        ],
    )
    def test_distance(self, hex1, hex2, expected):
        distance = hex.distance(hex1, hex2)
        assert distance == expected


class TestSpiral:
    def test_spiral(self):
        hex_center = hex.Cube(0, 0, 0)
        radius = 0
        spiral = list(hex.spiral(hex_center, radius))
        expected = [
            hex.Cube(0, 0, 0),
        ]
        assert spiral == expected

    def test_spiral_radius(self):
        hex_center = hex.Cube(0, 0, 0)
        radius = 1
        spiral = list(hex.spiral(hex_center, radius))
        expected = [
            hex.Cube(0, 0, 0),
            hex.Cube(0, -1, 1),
            hex.Cube(1, -1, 0),
            hex.Cube(1, 0, -1),
            hex.Cube(0, 1, -1),
            hex.Cube(-1, 1, 0),
            hex.Cube(-1, 0, 1),
        ]
        assert spiral == expected

    def test_spiral_center(self):
        hex_center = hex.Cube(0, -1, 1)
        radius = 1
        spiral = list(hex.spiral(hex_center, radius))
        expected = [
            hex.Cube(0, -1, 1),
            hex.Cube(0, -2, 2),
            hex.Cube(1, -2, 1),
            hex.Cube(1, -1, 0),
            hex.Cube(0, 0, 0),
            hex.Cube(-1, 0, 1),
            hex.Cube(-1, -1, 2),
        ]
        assert spiral == expected

    def test_spiral_direction(self):
        center = hex.Cube(0, 0, 0)
        radius = 1
        direction = hex.Direction.S
        spiral = list(hex.spiral(center, radius, direction=direction))
        expected = [
            hex.Cube(0, 0, 0),
            hex.Cube(0, 1, -1),
            hex.Cube(-1, 1, 0),
            hex.Cube(-1, 0, 1),
            hex.Cube(0, -1, 1),
            hex.Cube(1, -1, 0),
            hex.Cube(1, 0, -1),
        ]
        assert spiral == expected
