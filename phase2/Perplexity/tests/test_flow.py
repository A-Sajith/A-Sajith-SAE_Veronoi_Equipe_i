from pathlib import Path
from voronoi.controller import VoronoiController


def test_full_flow(tmp_path: Path) -> None:
    file_path = tmp_path / "points.txt"
    file_path.write_text("0,0\n1,0\n0,1\n", encoding="utf-8")

    controller = VoronoiController()
    controller.load_points_file(file_path)
    controller.compute_diagram()

    svg_path = tmp_path / "out.svg"
    controller.export_svg(svg_path)
    assert svg_path.exists()
