from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Edge:
    start: Tuple[float, float]
    end: Tuple[float, float]


@dataclass
class Cell:
    site: Point
    vertices: List[Tuple[float, float]]


@dataclass
class VoronoiDiagram:
    cells: List[Cell]
    edges: List[Edge]
