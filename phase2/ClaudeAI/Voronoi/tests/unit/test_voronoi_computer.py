import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.point import Point
from src.core.voronoi_computer import compute_voronoi_diagram


class TestComputeVoronoiDiagramEdgeCases(unittest.TestCase):

    def test_returns_empty_diagram_for_empty_input(self):
        diagram = compute_voronoi_diagram([])
        self.assertEqual(len(diagram.sites), 0)
        self.assertEqual(len(diagram.edges), 0)

    def test_returns_single_cell_with_no_edges_for_one_point(self):
        diagram = compute_voronoi_diagram([Point(x=5, y=5)])
        self.assertEqual(len(diagram.sites), 1)
        self.assertEqual(len(diagram.edges), 0)


class TestComputeVoronoiDiagramStructure(unittest.TestCase):

    def test_produces_one_site_per_input_point(self):
        points = [Point(x=0, y=0), Point(x=10, y=0), Point(x=5, y=10)]
        diagram = compute_voronoi_diagram(points)
        self.assertEqual(len(diagram.sites), 3)

    def test_bounding_box_contains_all_sites(self):
        points = [Point(x=10, y=20), Point(x=30, y=40)]
        diagram = compute_voronoi_diagram(points)
        bb = diagram.bounding_box
        for point in points:
            self.assertGreaterEqual(point.x, bb.min_x)
            self.assertLessEqual(point.x, bb.max_x)
            self.assertGreaterEqual(point.y, bb.min_y)
            self.assertLessEqual(point.y, bb.max_y)

    def test_generates_edges_for_two_separated_points(self):
        points = [Point(x=0, y=0), Point(x=100, y=0)]
        diagram = compute_voronoi_diagram(points)
        self.assertGreater(len(diagram.edges), 0)

    def test_each_edge_has_finite_coordinates(self):
        points = [Point(x=0, y=0), Point(x=50, y=50), Point(x=100, y=0)]
        diagram = compute_voronoi_diagram(points)
        import math
        for edge in diagram.edges:
            self.assertTrue(math.isfinite(edge.x1))
            self.assertTrue(math.isfinite(edge.y1))
            self.assertTrue(math.isfinite(edge.x2))
            self.assertTrue(math.isfinite(edge.y2))

    def test_more_points_produce_more_edges(self):
        two_point_diagram = compute_voronoi_diagram([Point(x=0, y=0), Point(x=100, y=0)])
        four_point_diagram = compute_voronoi_diagram([
            Point(x=0, y=0), Point(x=100, y=0),
            Point(x=0, y=100), Point(x=100, y=100),
        ])
        self.assertGreater(len(four_point_diagram.edges), len(two_point_diagram.edges))

    def test_diagram_to_dict_contains_required_keys(self):
        diagram = compute_voronoi_diagram([Point(x=1, y=2), Point(x=3, y=4)])
        data = diagram.to_dict()
        self.assertIn("sites", data)
        self.assertIn("edges", data)
        self.assertIn("boundingBox", data)


if __name__ == "__main__":
    unittest.main()
