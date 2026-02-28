from __future__ import annotations

from voronoi_app.application.color_assignment import assign_distinct_colors
from voronoi_app.domain.models import BoundingBox, Point2D, VoronoiDiagram
from voronoi_app.infrastructure.voronoi_scipy import compute_voronoi_cells


def _compute_default_bounding_box(points: list[Point2D]) -> BoundingBox:
    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)

    width = max_x - min_x
    height = max_y - min_y
    margin = max(width, height) * 0.05
    if margin == 0:
        margin = 1.0

    return BoundingBox(
        min_x=min_x - margin,
        min_y=min_y - margin,
        max_x=max_x + margin,
        max_y=max_y + margin,
    )


def build_voronoi_diagram(points: list[Point2D], *, bounding_box: BoundingBox | None = None) -> VoronoiDiagram:
    bbox = bounding_box or _compute_default_bounding_box(points)
    colors = assign_distinct_colors(len(points))
    cells = compute_voronoi_cells(points=points, bounding_box=bbox)
    return VoronoiDiagram(
        sites=tuple(points),
        colors=tuple(colors),
        bounding_box=bbox,
        cells=tuple(cells),
    )
