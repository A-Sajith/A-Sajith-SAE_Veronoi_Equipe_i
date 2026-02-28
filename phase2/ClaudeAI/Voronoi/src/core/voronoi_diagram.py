from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from src.core.point import Point
from src.core.bounding_box import BoundingBox


@dataclass(frozen=True)
class VoronoiEdge:
    x1: float
    y1: float
    x2: float
    y2: float
    left_site_index: int
    right_site_index: int

    def to_dict(self) -> dict:
        return {
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "left": self.left_site_index,
            "right": self.right_site_index,
        }


@dataclass(frozen=True)
class VoronoiDiagram:
    sites: List[Point]
    edges: List[VoronoiEdge]
    bounding_box: BoundingBox

    def cell_count(self) -> int:
        return len(self.sites)

    def edge_count(self) -> int:
        return len(self.edges)

    def to_dict(self) -> dict:
        return {
            "sites": [{"x": p.x, "y": p.y} for p in self.sites],
            "edges": [e.to_dict() for e in self.edges],
            "boundingBox": self.bounding_box.to_dict(),
        }
