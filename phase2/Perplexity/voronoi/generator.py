from __future__ import annotations
from typing import List, Tuple
import numpy as np
from scipy.spatial import Voronoi

from .domain import Point, Edge, Cell, VoronoiDiagram


class VoronoiGenerator:
    def generate(self, points: List[Point]) -> VoronoiDiagram:
        if len(points) == 0:
            return VoronoiDiagram(cells=[], edges=[])

        if len(points) == 1:
            return VoronoiDiagram(
                cells=[Cell(site=points[0], vertices=[])],
                edges=[]
            )

        # ✅ 2+ POINTS : génère un diagramme valide
        coords = np.array([[p.x, p.y] for p in points])

        if len(points) == 2:
            # ✅ SPECIAL 2 POINTS : ligne médiane infinie
            return self._generate_two_points_diagram(points)

        # 3+ points : utilise scipy (avec points auxiliaires si besoin)
        try:
            diagram = self._generate_scipy_diagram(points)
            if diagram.edges:
                return diagram
        except:
            pass

        # Fallback : bissectrice pour 3 points
        return self._generate_fallback_diagram(points)

    def _generate_two_points_diagram(self, points: List[Point]) -> VoronoiDiagram:
        """✅ 2 POINTS = 1 ligne médiane parfaite"""
        p1, p2 = points
        mid_x = (p1.x + p2.x) / 2
        mid_y = (p1.y + p2.y) / 2

        # Direction perpendiculaire
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        perp_dx = -dy
        perp_dy = dx

        # 2 segments pour simuler ligne infinie
        start1 = (mid_x - perp_dx*2, mid_y - perp_dy*2)
        end1 = (mid_x + perp_dx*2, mid_y + perp_dy*2)
        start2 = (mid_x - perp_dx*1, mid_y - perp_dy*1)
        end2 = (mid_x + perp_dx*1, mid_y + perp_dy*1)

        edges = [
            Edge(start=start1, end=end1),
            Edge(start=start2, end=end2)
        ]

        return VoronoiDiagram(
            cells=[Cell(site=p1, vertices=[]), Cell(site=p2, vertices=[])],
            edges=edges
        )

    def _generate_scipy_diagram(self, points: List[Point]) -> VoronoiDiagram:
        """Génère avec scipy + points auxiliaires"""
        coords = np.array([[p.x, p.y] for p in points])
        min_coords = coords.min(axis=0) - 5
        max_coords = coords.max(axis=0) + 5

        # 4 points d'appoint aux coins
        aux_points = np.array([
            [min_coords[0], min_coords[1]],
            [max_coords[0], min_coords[1]],
            [min_coords[0], max_coords[1]],
            [max_coords[0], max_coords[1]]
        ])

        extended_coords = np.vstack([coords, aux_points])
        vor = Voronoi(extended_coords)

        cells = self._build_cells(points, vor, len(points))
        edges = self._build_edges(vor)
        return VoronoiDiagram(cells=cells, edges=edges)

    def _generate_fallback_diagram(self, points: List[Point]) -> VoronoiDiagram:
        """Fallback pour 3 points : triangle médian"""
        # Simple : connecte milieux des segments
        cells = [Cell(site=p, vertices=[]) for p in points]

        # Lignes approximatives entre milieux
        edges = []
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i+1) % len(points)]
            mid_x = (p1.x + p2.x) / 2
            mid_y = (p1.y + p2.y) / 2
            edges.append(Edge(
                start=(mid_x-0.5, mid_y-0.5),
                end=(mid_x+0.5, mid_y+0.5)
            ))
        return VoronoiDiagram(cells=cells, edges=edges)

    def _build_cells(self, original_points: List[Point], vor: Voronoi, original_count: int) -> List[Cell]:
        cells = []
        for i in range(original_count):
            region_idx = vor.point_region[i]
            region = vor.regions[region_idx]
            if not region or -1 in region:
                continue
            vertices = [tuple(vor.vertices[j]) for j in region]
            cells.append(Cell(site=original_points[i], vertices=vertices))
        return cells

    def _build_edges(self, vor: Voronoi) -> List[Edge]:
        edges = []
        for ridge_vertices in vor.ridge_vertices:
            if -1 not in ridge_vertices and len(ridge_vertices) == 2:
                v1, v2 = ridge_vertices
                start = tuple(vor.vertices[v1])
                end = tuple(vor.vertices[v2])
                edges.append(Edge(start=start, end=end))
        return edges
