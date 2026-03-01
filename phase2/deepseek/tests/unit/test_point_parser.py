import unittest
import tempfile
import os
from deepseek.io.point_parser import SimplePointParser, ParseError

class TestSimplePointParser(unittest.TestCase):
    def setUp(self):
        self.parser = SimplePointParser()

    def _create_temp_file(self, content):
        tmp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_parse_valid_file(self):
        content = "1,2\n3.5,4.6\n 10.2 , 20.3 \n"
        path = self._create_temp_file(content)
        points = self.parser.parse(path)
        self.assertEqual(len(points), 3)
        self.assertEqual(points[0].x, 1.0)
        self.assertEqual(points[0].y, 2.0)
        self.assertEqual(points[1].x, 3.5)
        self.assertEqual(points[1].y, 4.6)
        self.assertEqual(points[2].x, 10.2)
        self.assertEqual(points[2].y, 20.3)
        os.unlink(path)

    def test_parse_empty_lines(self):
        content = "1,2\n\n3,4\n"
        path = self._create_temp_file(content)
        points = self.parser.parse(path)
        self.assertEqual(len(points), 2)
        os.unlink(path)

    def test_parse_invalid_format(self):
        content = "1,2\n3,4,5\n"
        path = self._create_temp_file(content)
        with self.assertRaises(ParseError):
            self.parser.parse(path)
        os.unlink(path)

    def test_parse_non_numeric(self):
        content = "1,2\na,b\n"
        path = self._create_temp_file(content)
        with self.assertRaises(ParseError):
            self.parser.parse(path)
        os.unlink(path)