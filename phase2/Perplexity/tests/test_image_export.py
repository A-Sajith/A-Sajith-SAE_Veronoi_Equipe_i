from pathlib import Path
from voronoi.domain import VoronoiDiagram, Edge, Cell, Point
from voronoi.image_export import ImageExporter


def test_image_export_creates_file(tmp_path: Path) -> None:
    diagram = VoronoiDiagram(
        cells=[Cell(site=Point(0.0, 0.0), vertices=[(0.0, 0.0), (1.0, 0.0)])],
        edges=[Edge(start=(0.0, 0.0), end=(1.0, 0.0))],
    )

    exporter = ImageExporter()
    output = tmp_path / "diagram.png"
    exporter.export(diagram, output)

    assert output.exists()
    assert output.stat().st_size > 0
