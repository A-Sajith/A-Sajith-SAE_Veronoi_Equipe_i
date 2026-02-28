from pathlib import Path
from voronoi.domain import VoronoiDiagram, Edge, Cell, Point
from voronoi.svg_export import SvgExporter


def test_svg_export_creates_file(tmp_path: Path) -> None:
    diagram = VoronoiDiagram(
        cells=[Cell(site=Point(0.0, 0.0), vertices=[(0.0, 0.0), (1.0, 0.0)])],
        edges=[Edge(start=(0.0, 0.0), end=(1.0, 0.0))],
    )

    exporter = SvgExporter()
    output = tmp_path / "diagram.svg"
    exporter.export(diagram, output)

    content = output.read_text(encoding="utf-8")
    assert "<svg" in content
    assert "<line" in content

