import unittest
import tempfile
import os
from deepseek.model.point import Point
from deepseek.model.voronoi_diagram import VoronoiDiagram
from deepseek.io.diagram_exporter import MatplotlibDiagramExporter
from deepseek.gui.diagram_canvas import MatplotlibDiagramRenderer

class TestMatplotlibDiagramExporter(unittest.TestCase):
    def setUp(self):
        renderer = MatplotlibDiagramRenderer()
        self.exporter = MatplotlibDiagramExporter(renderer)
        self.diagram = VoronoiDiagram(
            sites=[Point(0,0), Point(1,0), Point(0,1)],
            vertices=[Point(0.5,0.5)],
            ridges=[(0, -1)],
            regions=[],
            point_regions=[]
        )

    def test_export_svg(self):
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            path = tmp.name
        self.exporter.export_svg(self.diagram, path)
        self.assertTrue(os.path.exists(path))
        os.unlink(path)

    def test_export_image(self):
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            path = tmp.name
        self.exporter.export_image(self.diagram, path)
        self.assertTrue(os.path.exists(path))
        os.unlink(path)