import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.point import Point
from src.core.voronoi_computer import compute_voronoi_diagram
from src.io.svg_exporter import export_diagram_to_svg


def build_diagram_from_coordinate_pairs(pairs):
    return compute_voronoi_diagram([Point(x=x, y=y) for x, y in pairs])


class TestExportDiagramToSvg(unittest.TestCase):

    def test_starts_with_xml_declaration(self):
        diagram = build_diagram_from_coordinate_pairs([(0, 0), (10, 10)])
        svg = export_diagram_to_svg(diagram)
        self.assertTrue(svg.startswith("<?xml"))

    def test_contains_svg_opening_and_closing_tags(self):
        diagram = build_diagram_from_coordinate_pairs([(0, 0), (10, 10)])
        svg = export_diagram_to_svg(diagram)
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)

    def test_uses_provided_width_and_height(self):
        diagram = build_diagram_from_coordinate_pairs([(0, 0), (10, 10)])
        svg = export_diagram_to_svg(diagram, svg_width=1024, svg_height=768)
        self.assertIn('width="1024"', svg)
        self.assertIn('height="768"', svg)

    def test_embeds_site_coordinates_in_labels(self):
        diagram = build_diagram_from_coordinate_pairs([(42, 99)])
        svg = export_diagram_to_svg(diagram)
        self.assertIn("42", svg)
        self.assertIn("99", svg)

    def test_generates_valid_svg_for_empty_diagram(self):
        diagram = compute_voronoi_diagram([])
        svg = export_diagram_to_svg(diagram)
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)

    def test_includes_line_elements_for_multiple_points(self):
        diagram = build_diagram_from_coordinate_pairs([(0, 0), (100, 0), (50, 100)])
        svg = export_diagram_to_svg(diagram)
        self.assertIn("<line", svg)

    def test_includes_circle_elements_for_sites(self):
        diagram = build_diagram_from_coordinate_pairs([(10, 20)])
        svg = export_diagram_to_svg(diagram)
        self.assertIn("<circle", svg)

    def test_default_dimensions_are_applied(self):
        diagram = build_diagram_from_coordinate_pairs([(0, 0), (10, 10)])
        svg = export_diagram_to_svg(diagram)
        self.assertIn('width="1200"', svg)
        self.assertIn('height="900"', svg)


if __name__ == "__main__":
    unittest.main()
