import unittest
from deepseek.model.point import Point

class TestPoint(unittest.TestCase):
    def test_creation(self):
        p = Point(1.5, 2.5)
        self.assertEqual(p.x, 1.5)
        self.assertEqual(p.y, 2.5)
        self.assertTrue(p == Point(1.5, 2.5))
        self.assertNotEqual(p, Point(1.5, 2.6))