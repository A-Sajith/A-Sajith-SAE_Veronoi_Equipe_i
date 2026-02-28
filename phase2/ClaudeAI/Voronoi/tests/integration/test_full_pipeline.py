import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.io.point_file_parser import parse_points_from_text
from src.core.voronoi_computer import compute_voronoi_diagram
from src.io.svg_exporter import export_diagram_to_svg


class TestFullPipelineParseComputeExport(unittest.TestCase):

    def test_produces_valid_svg_from_valid_text_file(self):
        file_content = "0,0\n100,0\n50,100"
        parse_result = parse_points_from_text(file_content)
        self.assertEqual(len(parse_result.errors), 0)

        diagram = compute_voronoi_diagram(parse_result.points)
        self.assertEqual(diagram.cell_count(), 3)

        svg = export_diagram_to_svg(diagram)
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)

    def test_handles_mix_of_valid_and_invalid_lines(self):
        file_content = "1,2\nINVALID\n3,4\n5.5,6.5"
        parse_result = parse_points_from_text(file_content)

        self.assertEqual(len(parse_result.errors), 1)
        self.assertEqual(parse_result.errors[0].line_number, 2)
        self.assertEqual(len(parse_result.points), 3)

        diagram = compute_voronoi_diagram(parse_result.points)
        self.assertEqual(diagram.cell_count(), 3)

        svg = export_diagram_to_svg(diagram)
        self.assertIn("<svg", svg)

    def test_handles_decimal_and_negative_coordinates_end_to_end(self):
        file_content = "-10.5,20.3\n0,0\n15.7,-8.2\n100,100"
        parse_result = parse_points_from_text(file_content)

        self.assertEqual(len(parse_result.errors), 0)
        self.assertEqual(len(parse_result.points), 4)

        diagram = compute_voronoi_diagram(parse_result.points)
        self.assertEqual(len(diagram.sites), 4)

        svg = export_diagram_to_svg(diagram)
        self.assertIn("</svg>", svg)

    def test_svg_embeds_site_coordinates_end_to_end(self):
        file_content = "42,99"
        parse_result = parse_points_from_text(file_content)
        diagram = compute_voronoi_diagram(parse_result.points)
        svg = export_diagram_to_svg(diagram)
        self.assertIn("42", svg)
        self.assertIn("99", svg)

    def test_returns_empty_svg_container_for_fully_invalid_input(self):
        file_content = "bad\nworse\nterrible"
        parse_result = parse_points_from_text(file_content)

        self.assertEqual(len(parse_result.errors), 3)
        self.assertEqual(len(parse_result.points), 0)

        diagram = compute_voronoi_diagram(parse_result.points)
        svg = export_diagram_to_svg(diagram)
        self.assertIn("<svg", svg)

    def test_diagram_to_dict_serializes_correctly(self):
        file_content = "0,0\n100,0\n50,86"
        parse_result = parse_points_from_text(file_content)
        diagram = compute_voronoi_diagram(parse_result.points)
        data = diagram.to_dict()

        self.assertIsInstance(data["sites"], list)
        self.assertEqual(len(data["sites"]), 3)
        self.assertIn("x", data["sites"][0])
        self.assertIn("y", data["sites"][0])
        self.assertIsInstance(data["edges"], list)
        self.assertIn("minX", data["boundingBox"])

    def test_spaces_around_coordinates_are_handled_end_to_end(self):
        file_content = "  10 , 20  \n  30 , 40  "
        parse_result = parse_points_from_text(file_content)
        self.assertEqual(len(parse_result.errors), 0)
        self.assertEqual(len(parse_result.points), 2)
        diagram = compute_voronoi_diagram(parse_result.points)
        svg = export_diagram_to_svg(diagram)
        self.assertIn("10.0", svg)


if __name__ == "__main__":
    unittest.main()
