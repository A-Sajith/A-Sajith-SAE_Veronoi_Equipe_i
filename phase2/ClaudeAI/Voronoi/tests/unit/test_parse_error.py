import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.parse_error import ParseError


class TestParseError(unittest.TestCase):

    def test_stores_line_number(self):
        error = ParseError(line_number=5, raw_content="abc", reason="invalid")
        self.assertEqual(error.line_number, 5)

    def test_stores_raw_content(self):
        error = ParseError(line_number=1, raw_content="bad input", reason="reason")
        self.assertEqual(error.raw_content, "bad input")

    def test_stores_reason(self):
        error = ParseError(line_number=1, raw_content="x", reason="format incorrect")
        self.assertEqual(error.reason, "format incorrect")

    def test_str_includes_line_number(self):
        error = ParseError(line_number=42, raw_content="foo", reason="bad")
        self.assertIn("42", str(error))

    def test_str_includes_raw_content(self):
        error = ParseError(line_number=1, raw_content="oops", reason="bad")
        self.assertIn("oops", str(error))

    def test_is_exception(self):
        error = ParseError(line_number=1, raw_content="", reason="")
        self.assertIsInstance(error, Exception)

    def test_is_frozen_immutable(self):
        error = ParseError(line_number=1, raw_content="x", reason="r")
        self.assertRaises(AttributeError, setattr, error, "line_number", 99)

        self.assertEqual(error.line_number, 1)



if __name__ == "__main__":
    unittest.main()
