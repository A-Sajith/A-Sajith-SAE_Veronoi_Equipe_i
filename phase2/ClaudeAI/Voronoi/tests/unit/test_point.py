import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.point import Point


class TestPointCreation(unittest.TestCase):

    def test_creates_point_with_integer_coordinates(self):
        point = Point(x=3, y=4)
        self.assertEqual(point.x, 3)
        self.assertEqual(point.y, 4)

    def test_creates_point_with_decimal_coordinates(self):
        point = Point(x=1.5, y=2.7)
        self.assertAlmostEqual(point.x, 1.5)
        self.assertAlmostEqual(point.y, 2.7)

    def test_creates_point_with_negative_coordinates(self):
        point = Point(x=-3, y=-4)
        self.assertEqual(point.x, -3)
        self.assertEqual(point.y, -4)

    def test_creates_point_at_origin(self):
        point = Point(x=0, y=0)
        self.assertEqual(point.x, 0)
        self.assertEqual(point.y, 0)

    def test_raises_value_error_for_nan_x(self):
        with self.assertRaises(ValueError):
            Point(x=float("nan"), y=1)

    def test_raises_value_error_for_infinite_y(self):
        with self.assertRaises(ValueError):
            Point(x=1, y=float("inf"))

    def test_raises_value_error_for_negative_infinite_x(self):
        with self.assertRaises(ValueError):
            Point(x=float("-inf"), y=0)


class TestPointDistanceTo(unittest.TestCase):

    def test_returns_zero_for_same_point(self):
        point = Point(x=1, y=1)
        self.assertEqual(point.distance_to(point), 0)

    def test_computes_pythagorean_distance(self):
        origin = Point(x=0, y=0)
        other = Point(x=3, y=4)
        self.assertAlmostEqual(origin.distance_to(other), 5.0)

    def test_distance_is_symmetric(self):
        a = Point(x=1, y=2)
        b = Point(x=4, y=6)
        self.assertAlmostEqual(a.distance_to(b), b.distance_to(a))

    def test_distance_with_decimal_coordinates(self):
        a = Point(x=0.0, y=0.0)
        b = Point(x=1.0, y=1.0)
        self.assertAlmostEqual(a.distance_to(b), math.sqrt(2))


class TestPointEquality(unittest.TestCase):

    def test_equal_points_with_same_coordinates(self):
        self.assertEqual(Point(x=2, y=3), Point(x=2, y=3))

    def test_unequal_points_with_different_coordinates(self):
        self.assertNotEqual(Point(x=2, y=3), Point(x=2, y=4))

    def test_point_is_frozen_immutable(self):
        point = Point(x=1, y=2)

        self.assertRaises(AttributeError, setattr, point, "x", 99)
        self.assertRaises(AttributeError, setattr, point, "y", 88)

        self.assertEqual(point.x, 1)
        self.assertEqual(point.y, 2)

class TestPointStringRepresentation(unittest.TestCase):

    def test_str_returns_readable_representation(self):
        self.assertEqual(str(Point(x=1, y=2)), "Point(1, 2)")


if __name__ == "__main__":
    unittest.main()
