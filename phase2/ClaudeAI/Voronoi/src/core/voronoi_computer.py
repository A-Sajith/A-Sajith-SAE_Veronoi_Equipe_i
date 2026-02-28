from __future__ import annotations
from typing import List, Sequence, Tuple
from src.core.point import Point
from src.core.bounding_box import BoundingBox
from src.core.voronoi_diagram import VoronoiDiagram, VoronoiEdge

GRID_RESOLUTION = 600


def compute_voronoi_diagram(points: Sequence[Point]) -> VoronoiDiagram:
    if not points:
        empty_box = BoundingBox(0.0, 100.0, 0.0, 100.0)
        return VoronoiDiagram(sites=[], edges=[], bounding_box=empty_box)

    bounding_box = BoundingBox.from_points(points)

    if len(points) == 1:
        return VoronoiDiagram(sites=list(points), edges=[], bounding_box=bounding_box)

    region_map = _build_region_map(points, bounding_box)
    edges = _extract_edges_from_region_boundaries(region_map, bounding_box)

    return VoronoiDiagram(sites=list(points), edges=edges, bounding_box=bounding_box)


def _build_region_map(points: Sequence[Point], bb: BoundingBox) -> List[List[int]]:
    region_map = [[0] * GRID_RESOLUTION for _ in range(GRID_RESOLUTION)]

    for row in range(GRID_RESOLUTION):
        world_y = bb.min_y + (row / GRID_RESOLUTION) * bb.height()
        for col in range(GRID_RESOLUTION):
            world_x = bb.min_x + (col / GRID_RESOLUTION) * bb.width()
            region_map[row][col] = _find_nearest_site_index(world_x, world_y, points)

    return region_map


def _find_nearest_site_index(world_x: float, world_y: float, points: Sequence[Point]) -> int:
    nearest_index = 0
    min_squared_distance = float("inf")

    for index, point in enumerate(points):
        dx = world_x - point.x
        dy = world_y - point.y
        squared_distance = dx * dx + dy * dy
        if squared_distance < min_squared_distance:
            min_squared_distance = squared_distance
            nearest_index = index

    return nearest_index


def _extract_edges_from_region_boundaries(
    region_map: List[List[int]], bb: BoundingBox
) -> List[VoronoiEdge]:
    edges: List[VoronoiEdge] = []
    seen_edge_keys: set = set()

    def scale_x(col: float) -> float:
        return bb.min_x + (col / GRID_RESOLUTION) * bb.width()

    def scale_y(row: float) -> float:
        return bb.min_y + (row / GRID_RESOLUTION) * bb.height()

    for row in range(GRID_RESOLUTION - 1):
        for col in range(GRID_RESOLUTION - 1):
            current = region_map[row][col]
            right = region_map[row][col + 1]
            below = region_map[row + 1][col]

            if current != right:
                edge_key = (min(current, right), max(current, right), "h", row, col)
                if edge_key not in seen_edge_keys:
                    seen_edge_keys.add(edge_key)
                    edges.append(VoronoiEdge(
                        x1=scale_x(col + 0.5), y1=scale_y(row),
                        x2=scale_x(col + 0.5), y2=scale_y(row + 1),
                        left_site_index=current,
                        right_site_index=right,
                    ))

            if current != below:
                edge_key = (min(current, below), max(current, below), "v", row, col)
                if edge_key not in seen_edge_keys:
                    seen_edge_keys.add(edge_key)
                    edges.append(VoronoiEdge(
                        x1=scale_x(col), y1=scale_y(row + 0.5),
                        x2=scale_x(col + 1), y2=scale_y(row + 0.5),
                        left_site_index=current,
                        right_site_index=below,
                    ))

    return edges
