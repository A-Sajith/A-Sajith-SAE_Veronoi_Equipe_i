from dataclasses import dataclass, field
from typing import List, Tuple
from .point import Point

@dataclass
class VoronoiDiagram:
    sites: List[Point] = field(default_factory=list)
    vertices: List[Point] = field(default_factory=list)
    ridges: List[Tuple[int, int]] = field(default_factory=list)
    regions: List[List[int]] = field(default_factory=list)
    point_regions: List[int] = field(default_factory=list)