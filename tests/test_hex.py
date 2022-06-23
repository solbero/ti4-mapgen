import pytest

from ti4_mapgen import hex


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
        with pytest.raises(ValueError) as exc_info:
            _ = hex.Cube(1, 0, 1)
        error_message = str(exc_info.value)
        assert error_message == "attributes 'q', 'r', 's' must have a sum of 0, not 2"


class TestHexOperators:
    def test_hex_equal(self):
        hex1 = hex.Cube(0, 0, 0)
        hex2 = hex.Cube(0, 0, 0)
        assert hex1 == hex2

    def test_hex_unequal(self):
        hex1 = hex.Cube(0, 0, 0)
        hex2 = hex.Cube(0, 1, -1)
        assert hex1 != hex2

    @pytest.mark.parametrize(
        ["hex2", "expected"],
        [
            (hex.Cube(0, -1, 1), hex.Cube(0, 0, 0)),
            ((0, -1, 1), hex.Cube(0, 0, 0)),
            ([0, -1, 1], hex.Cube(0, 0, 0)),
            ({"q": 0, "r": -1, "s": 1}, hex.Cube(0, 0, 0)),
        ],
    )
    def test_hex_add(self, hex2, expected):
        hex1 = hex.Cube(0, 1, -1)
        assert hex1 + hex2 == expected

    @pytest.mark.parametrize(
        ["hex2", "exception", "message"],
        [
            ({"q": 0, "r": -1}, ValueError, "mapping must contain keys 'q', 'r', 's', not 'q', 'r'"),
            ({"a": 0, "b": -1, "c": 1}, ValueError, "mapping must contain keys 'q', 'r', 's', not 'a', 'b', 'c'"),
            ((1, -1), ValueError, "sequence must have length 3, not 2"),
            ((0, -1, 1, 0), ValueError, "sequence must have length 3, not 4"),
            (("0", "-1", "1"), TypeError, "unsupported operand type(s) for +: 'int' and 'str'"),
            ("0, -1, 1", TypeError, "unsupported operand type(s) for +: 'Cube' and 'str'"),
        ],
    )
    def test_hex_add_raises(self, hex2, exception, message):
        hex1 = hex.Cube(0, 1, -1)
        with pytest.raises(exception) as exc_info:
            _ = hex1 + hex2
        error_message = str(exc_info.value)
        assert error_message == message

    @pytest.mark.parametrize(
        ["hex2", "expected"],
        [
            (hex.Cube(0, -1, 1), hex.Cube(0, 2, -2)),
            ((0, -1, 1), hex.Cube(0, 2, -2)),
            ([0, -1, 1], hex.Cube(0, 2, -2)),
            ({"q": 0, "r": -1, "s": 1}, hex.Cube(0, 2, -2)),
        ],
    )
    def test_hex_sub(self, hex2, expected):
        hex1 = hex.Cube(0, 1, -1)
        assert hex1 - hex2 == expected

    @pytest.mark.parametrize(
        ["hex2", "exception", "message"],
        [
            ({"q": 0, "r": -1}, ValueError, "mapping must contain keys 'q', 'r', 's', not 'q', 'r'"),
            ({"a": 0, "b": -1, "c": 1}, ValueError, "mapping must contain keys 'q', 'r', 's', not 'a', 'b', 'c'"),
            ((1, -1), ValueError, "sequence must have length 3, not 2"),
            ((0, -1, 1, 0), ValueError, "sequence must have length 3, not 4"),
            (("0", "-1", "1"), TypeError, "unsupported operand type(s) for -: 'int' and 'str'"),
            ("0, -1, 1", TypeError, "unsupported operand type(s) for -: 'Cube' and 'str'"),
        ],
    )
    def test_hex_sub_raises(self, hex2, exception, message):
        hex1 = hex.Cube(0, 1, -1)
        with pytest.raises(exception) as exc_info:
            _ = hex1 - hex2
        error_message = str(exc_info.value)
        assert error_message == message

    def test_hex_mul(self):
        hex_ = hex.Cube(0, 1, -1)
        expected = hex.Cube(0, 2, -2)
        assert hex_ * 2 == expected

    @pytest.mark.parametrize(
        ["hex2", "exception", "message"],
        [
            (2.0, TypeError, "unsupported operand type(s) for *: 'Cube' and 'float'"),
            ("2", TypeError, "unsupported operand type(s) for *: 'Cube' and 'str'"),
        ],
    )
    def test_hex_mul_raises(self, hex2, exception, message):
        hex1 = hex.Cube(0, 1, -1)
        with pytest.raises(exception) as exc_info:
            _ = hex1 * hex2
        error_message = str(exc_info.value)
        assert error_message == message

    @pytest.mark.parametrize(
        ["hex_", "k", "expected"],
        [
            (hex.Cube(0, -2, 2), 2, hex.Cube(0, -1, 1)),
            (hex.Cube(0, -1, 1), 2, hex.Cube(0, 0, 0)),
        ],
    )
    def test_hex_floordiv(self, hex_, k, expected):
        assert hex_ // k == expected

    @pytest.mark.parametrize(
        ["hex2", "exception", "message"],
        [
            (2.0, TypeError, "unsupported operand type(s) for //: 'Cube' and 'float'"),
            ("2", TypeError, "unsupported operand type(s) for //: 'Cube' and 'str'"),
        ],
    )
    def test_hex_floordiv_raises(self, hex2, exception, message):
        hex1 = hex.Cube(0, 1, -1)
        with pytest.raises(exception) as exc_info:
            _ = hex1 // hex2
        error_message = str(exc_info.value)
        assert error_message == message

    def test_hex_abs(self):
        hex_ = hex.Cube(0, -2, 2)
        assert abs(hex_) == 2


class TestNeighbor:
    @pytest.mark.parametrize(
        ["direction", "expected"],
        [
            (hex.Adjacent.N, hex.Cube(0, -1, 1)),
            (hex.Adjacent.NE, hex.Cube(1, -1, 0)),
            (hex.Adjacent.SE, hex.Cube(1, 0, -1)),
            (hex.Adjacent.S, hex.Cube(0, 1, -1)),
            (hex.Adjacent.SW, hex.Cube(-1, 1, 0)),
            (hex.Adjacent.NW, hex.Cube(-1, 0, 1)),
        ],
    )
    def test_hex_adjacent(self, direction, expected):
        hex1 = hex.Cube(0, 0, 0)
        adjacent = hex.adjacent(hex1, direction=direction)
        assert adjacent == expected

    @pytest.mark.parametrize(
        ["direction", "expected"],
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
        direction = hex.Adjacent.S
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
        move = hex.Move.COUNTERCLOCKWISE
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
        expected = "argument 'angle' must be in 60 degree increments"
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
        direction = hex.Adjacent.S
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
