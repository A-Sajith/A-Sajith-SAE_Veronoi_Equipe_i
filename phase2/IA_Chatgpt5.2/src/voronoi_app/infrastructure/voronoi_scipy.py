from __future__ import annotations

from collections.abc import Iterable

import math

from voronoi_app.domain.errors import VoronoiComputationError
from voronoi_app.domain.models import BoundingBox, Point2D, VoronoiCell


def compute_voronoi_cells(*, points: list[Point2D], bounding_box: BoundingBox) -> list[VoronoiCell]:
    if len(points) < 2:
        raise VoronoiComputationError("Au moins 2 points sont nécessaires")

    if len(points) > 1000:
        raise VoronoiComputationError("Trop de points (maximum 1000)")

    if len({(point.x, point.y) for point in points}) != len(points):
        raise VoronoiComputationError("Calcul Voronoï impossible (points dupliqués)")

    bbox_polygon = _bbox_as_polygon(bounding_box)
    cells: list[VoronoiCell] = []

    for site_index, site in enumerate(points):
        polygon = list(bbox_polygon)
        for other_index, other in enumerate(points):
            if other_index == site_index:
                continue
            polygon = _clip_polygon_to_halfplane_closer_to_site(polygon=polygon, site=site, other=other)
            if len(polygon) < 3:
                break

        polygon = _deduplicate_sequential_points_with_epsilon(polygon)
        if len(polygon) >= 3:
            cells.append(VoronoiCell(site_index=site_index, polygon=tuple(polygon)))

    return cells


def _bbox_as_polygon(bbox: BoundingBox) -> tuple[Point2D, Point2D, Point2D, Point2D]:
    return (
        Point2D(x=bbox.min_x, y=bbox.min_y),
        Point2D(x=bbox.max_x, y=bbox.min_y),
        Point2D(x=bbox.max_x, y=bbox.max_y),
        Point2D(x=bbox.min_x, y=bbox.max_y),
    )


def _clip_polygon_to_halfplane_closer_to_site(*, polygon: list[Point2D], site: Point2D, other: Point2D) -> list[Point2D]:
    # Keep points x such that dist(x, site) <= dist(x, other)
    # Equivalent half-plane: x·n <= c, where n = (other - site)
    # and c = (|other|^2 - |site|^2) / 2
    nx = other.x - site.x
    ny = other.y - site.y
    if nx == 0 and ny == 0:
        return []

    c = (other.x * other.x + other.y * other.y - site.x * site.x - site.y * site.y) / 2.0
    return _clip_polygon_to_halfplane(polygon=polygon, nx=nx, ny=ny, c=c)


def _clip_polygon_to_halfplane(*, polygon: list[Point2D], nx: float, ny: float, c: float) -> list[Point2D]:
    if not polygon:
        return []

    eps = 1e-10

    def value(p: Point2D) -> float:
        return p.x * nx + p.y * ny - c

    output: list[Point2D] = []
    previous = polygon[-1]
    prev_v = value(previous)

    for current in polygon:
        curr_v = value(current)
        prev_inside = prev_v <= eps
        curr_inside = curr_v <= eps

        if curr_inside and prev_inside:
            output.append(current)
        elif prev_inside and not curr_inside:
            inter = _segment_intersection_with_halfplane_boundary(prev=previous, curr=current, prev_v=prev_v, curr_v=curr_v)
            output.append(inter)
        elif not prev_inside and curr_inside:
            inter = _segment_intersection_with_halfplane_boundary(prev=previous, curr=current, prev_v=prev_v, curr_v=curr_v)
            output.append(inter)
            output.append(current)

        previous = current
        prev_v = curr_v

    return output


def _segment_intersection_with_halfplane_boundary(*, prev: Point2D, curr: Point2D, prev_v: float, curr_v: float) -> Point2D:
    # Intersect segment prev->curr with boundary value(p)=0 using linear interpolation.
    denom = (prev_v - curr_v)
    if denom == 0:
        return Point2D(x=curr.x, y=curr.y)
    t = prev_v / denom
    t = max(0.0, min(1.0, t))
    return Point2D(
        x=prev.x + (curr.x - prev.x) * t,
        y=prev.y + (curr.y - prev.y) * t,
    )


def _finite_regions_2d(*args, **kwargs):  # pragma: no cover
    raise NotImplementedError("La reconstruction SciPy des régions finies n'est plus utilisée")


def _clip_polygon_to_bbox(polygon: list[Point2D], bbox: BoundingBox) -> list[Point2D]:
    def inside(point: Point2D, edge: str) -> bool:
        if edge == "left":
            return point.x >= bbox.min_x
        if edge == "right":
            return point.x <= bbox.max_x
        if edge == "bottom":
            return point.y >= bbox.min_y
        if edge == "top":
            return point.y <= bbox.max_y
        raise ValueError(edge)

    def intersection(p1: Point2D, p2: Point2D, edge: str) -> Point2D:
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        if edge == "left":
            x = bbox.min_x
            t = (x - p1.x) / dx
            return Point2D(x=x, y=p1.y + t * dy)
        if edge == "right":
            x = bbox.max_x
            t = (x - p1.x) / dx
            return Point2D(x=x, y=p1.y + t * dy)
        if edge == "bottom":
            y = bbox.min_y
            t = (y - p1.y) / dy
            return Point2D(x=p1.x + t * dx, y=y)
        if edge == "top":
            y = bbox.max_y
            t = (y - p1.y) / dy
            return Point2D(x=p1.x + t * dx, y=y)
        raise ValueError(edge)

    def clip_with_edge(subject: list[Point2D], edge: str) -> list[Point2D]:
        if not subject:
            return []

        output: list[Point2D] = []
        previous = subject[-1]
        for current in subject:
            current_inside = inside(current, edge)
            previous_inside = inside(previous, edge)

            if current_inside and previous_inside:
                output.append(current)
            elif previous_inside and not current_inside:
                output.append(intersection(previous, current, edge))
            elif not previous_inside and current_inside:
                output.append(intersection(previous, current, edge))
                output.append(current)

            previous = current

        return output

    clipped = polygon
    for edge in ("left", "right", "bottom", "top"):
        clipped = clip_with_edge(clipped, edge)

    return _deduplicate_sequential_points(clipped)


def _deduplicate_sequential_points(points: Iterable[Point2D]) -> list[Point2D]:
    deduplicated: list[Point2D] = []
    previous: Point2D | None = None
    for point in points:
        if previous is None or (point.x != previous.x or point.y != previous.y):
            deduplicated.append(point)
            previous = point

    if len(deduplicated) >= 2 and deduplicated[0] == deduplicated[-1]:
        deduplicated.pop()

    return deduplicated


def _deduplicate_sequential_points_with_epsilon(points: Iterable[Point2D], *, eps: float = 1e-9) -> list[Point2D]:
    deduplicated: list[Point2D] = []
    previous: Point2D | None = None
    for point in points:
        if previous is None:
            deduplicated.append(point)
            previous = point
            continue

        if math.hypot(point.x - previous.x, point.y - previous.y) > eps:
            deduplicated.append(point)
            previous = point

    if len(deduplicated) >= 2 and math.hypot(deduplicated[0].x - deduplicated[-1].x, deduplicated[0].y - deduplicated[-1].y) <= eps:
        deduplicated.pop()

    return deduplicated
