from voronoi_app.application.voronoi_service import build_voronoi_diagram
from voronoi_app.domain.models import Point2D


def _point_on_segment(px: float, py: float, ax: float, ay: float, bx: float, by: float, eps: float = 1e-9) -> bool:
    cross = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
    if abs(cross) > eps:
        return False
    dot = (px - ax) * (px - bx) + (py - ay) * (py - by)
    return dot <= eps


def _point_in_polygon(px: float, py: float, polygon: tuple[Point2D, ...]) -> bool:
    n = len(polygon)
    if n < 3:
        return False

    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]
        if _point_on_segment(px, py, a.x, a.y, b.x, b.y):
            return True

    inside = False
    for i in range(n):
        x1, y1 = polygon[i].x, polygon[i].y
        x2, y2 = polygon[(i + 1) % n].x, polygon[(i + 1) % n].y
        if (y1 > py) != (y2 > py):
            xinters = (x2 - x1) * (py - y1) / (y2 - y1) + x1
            if px < xinters:
                inside = not inside
    return inside


def test_build_voronoi_diagram_returns_cells_and_bbox() -> None:
    diagram = build_voronoi_diagram([Point2D(0, 0), Point2D(10, 0), Point2D(5, 10)])
    assert len(diagram.cells) >= 3
    assert diagram.bounding_box.width() > 0
    assert diagram.bounding_box.height() > 0


def test_voronoi_cells_contain_their_site_for_infinite_regions_case() -> None:
    points = [Point2D(2, 4), Point2D(5.3, 4.5), Point2D(18, 29), Point2D(12.5, 23.7)]
    diagram = build_voronoi_diagram(points)

    cells_by_site = {cell.site_index: cell for cell in diagram.cells}
    assert set(cells_by_site.keys()) == {0, 1, 2, 3}

    for index, site in enumerate(diagram.sites):
        cell = cells_by_site[index]
        assert _point_in_polygon(site.x, site.y, cell.polygon)


def test_all_cell_vertices_are_within_bbox() -> None:
    diagram = build_voronoi_diagram([Point2D(0, 0), Point2D(10, 0), Point2D(5, 10), Point2D(6, 3)])
    bbox = diagram.bounding_box
    for cell in diagram.cells:
        for point in cell.polygon:
            assert bbox.min_x - 1e-9 <= point.x <= bbox.max_x + 1e-9
            assert bbox.min_y - 1e-9 <= point.y <= bbox.max_y + 1e-9
