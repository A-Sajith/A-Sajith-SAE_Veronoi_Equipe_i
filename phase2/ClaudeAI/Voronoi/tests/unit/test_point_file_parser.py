import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.io.point_file_parser import parse_points_from_text


class TestParsePointsFromTextValidInput(unittest.TestCase):

    def test_parses_single_integer_coordinate_pair(self):
        result = parse_points_from_text("2,4")
        self.assertEqual(len(result.points), 1)
        self.assertEqual(result.points[0].x, 2.0)
        self.assertEqual(result.points[0].y, 4.0)
        self.assertEqual(len(result.errors), 0)

    def test_parses_decimal_coordinate_pair(self):
        result = parse_points_from_text("5.3,4.5")
        self.assertAlmostEqual(result.points[0].x, 5.3)
        self.assertAlmostEqual(result.points[0].y, 4.5)
        self.assertEqual(len(result.errors), 0)

    def test_parses_multiple_lines(self):
        result = parse_points_from_text("1,2\n3,4\n5,6")
        self.assertEqual(len(result.points), 3)
        self.assertEqual(len(result.errors), 0)

    def test_ignores_empty_lines(self):
        result = parse_points_from_text("1,2\n\n3,4\n")
        self.assertEqual(len(result.points), 2)
        self.assertEqual(len(result.errors), 0)

    def test_handles_spaces_around_coordinates(self):
        result = parse_points_from_text("  1 , 2  ")
        self.assertEqual(result.points[0].x, 1.0)
        self.assertEqual(result.points[0].y, 2.0)
        self.assertEqual(len(result.errors), 0)

    def test_handles_negative_coordinates(self):
        result = parse_points_from_text("-1,-2.5")
        self.assertEqual(result.points[0].x, -1.0)
        self.assertAlmostEqual(result.points[0].y, -2.5)
        self.assertEqual(len(result.errors), 0)

    def test_returns_empty_result_for_empty_string(self):
        result = parse_points_from_text("")
        self.assertEqual(len(result.points), 0)
        self.assertEqual(len(result.errors), 0)

    def test_returns_empty_result_for_whitespace_only(self):
        result = parse_points_from_text("   \n  \n")
        self.assertEqual(len(result.points), 0)
        self.assertEqual(len(result.errors), 0)

    def test_parses_zero_coordinates(self):
        result = parse_points_from_text("0,0")
        self.assertEqual(result.points[0].x, 0.0)
        self.assertEqual(result.points[0].y, 0.0)


class TestParsePointsFromTextInvalidInput(unittest.TestCase):

    def test_reports_parse_error_for_missing_comma(self):
        result = parse_points_from_text("1 2")
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].line_number, 1)
        self.assertEqual(len(result.points), 0)

    def test_reports_parse_error_for_non_numeric_values(self):
        result = parse_points_from_text("a,b")
        self.assertEqual(len(result.errors), 1)
        self.assertIn("format", result.errors[0].reason)

    def test_continues_parsing_after_invalid_line(self):
        result = parse_points_from_text("1,2\nbad line\n3,4")
        self.assertEqual(len(result.points), 2)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].line_number, 2)

    def test_reports_correct_line_numbers_for_multiple_errors(self):
        result = parse_points_from_text("bad\n1,2\nalso bad")
        self.assertEqual(result.errors[0].line_number, 1)
        self.assertEqual(result.errors[1].line_number, 3)

    def test_includes_raw_content_in_error(self):
        result = parse_points_from_text("invalid content")
        self.assertEqual(result.errors[0].raw_content, "invalid content")

    def test_reports_error_for_extra_values(self):
        result = parse_points_from_text("1,2,3")
        self.assertEqual(len(result.errors), 1)

    def test_reports_error_for_semicolon_separator(self):
        result = parse_points_from_text("1;2")
        self.assertEqual(len(result.errors), 1)


if __name__ == "__main__":
    unittest.main()
