import unittest
import tempfile
import os
from deepseek.io.point_parser import SimplePointParser
from deepseek.algorithm.scipy_calculator import ScipyVoronoiCalculator
from deepseek.io.diagram_exporter import MatplotlibDiagramExporter
from deepseek.gui.diagram_canvas import MatplotlibDiagramRenderer

class TestFullFlow(unittest.TestCase):
    def setUp(self):
        self.parser = SimplePointParser()
        self.calculator = ScipyVoronoiCalculator()
        self.renderer = MatplotlibDiagramRenderer()
        self.exporter = MatplotlibDiagramExporter(self.renderer)

    def test_parse_compute_export(self):
        content = "0,0\n1,0\n0,1\n"
        tmp_input = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmp_input.write(content)
        tmp_input.close()

        points = self.parser.parse(tmp_input.name)
        self.assertEqual(len(points), 3)

        diagram = self.calculator.compute(points)
        self.assertIsNotNone(diagram)

        svg_path = tempfile.NamedTemporaryFile(suffix='.svg', delete=False).name
        self.exporter.export_svg(diagram, svg_path)
        self.assertTrue(os.path.exists(svg_path))

        png_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
        self.exporter.export_image(diagram, png_path)
        self.assertTrue(os.path.exists(png_path))

        os.unlink(tmp_input.name)
        os.unlink(svg_path)
        os.unlink(png_path)