from pathlib import Path
from voronoi.parsing import PointFileImporter, PointFileFormatError


def test_import_valid_file(tmp_path: Path) -> None:
    content = "1,2\n 3.5 , 4.7\n# comment\n\n"
    file_path = tmp_path / "points.txt"
    file_path.write_text(content, encoding="utf-8")

    importer = PointFileImporter()
    points = importer.import_points(file_path)

    assert len(points) == 2
    assert points[0].x == 1.0
    assert points[0].y == 2.0


def test_import_invalid_line_raises(tmp_path: Path) -> None:
    content = "1,2\ninvalid\n"
    file_path = tmp_path / "points.txt"
    file_path.write_text(content, encoding="utf-8")

    importer = PointFileImporter()

    try:
        importer.import_points(file_path)
        assert False, "Expected PointFileFormatError"
    except PointFileFormatError as error:
        assert error.line_number == 2
