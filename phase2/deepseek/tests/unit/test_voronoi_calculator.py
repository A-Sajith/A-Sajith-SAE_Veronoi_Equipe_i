import unittest
from deepseek.model.point import Point
from deepseek.algorithm.scipy_calculator import ScipyVoronoiCalculator

class TestScipyVoronoiCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = ScipyVoronoiCalculator()

    def test_compute_with_three_points(self):
        points = [Point(0,0), Point(1,0), Point(0,1)]
        diagram = self.calculator.compute(points)
        self.assertEqual(len(diagram.sites), 3)
        self.assertGreater(len(diagram.vertices), 0)  # Au moins un sommet (le centre)
        self.assertEqual(len(diagram.point_regions), 3)  # Chaque point a une région associée
        # On ne teste pas ridges car elles peuvent être infinies

    def test_compute_with_less_than_three_points(self):
        points = [Point(0,0), Point(1,0)]
        with self.assertRaises(ValueError):
            self.calculator.compute(points)