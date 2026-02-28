from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point2D:
    x: float
    y: float


@dataclass(frozen=True, slots=True)
class RGBColor:
    red: int
    green: int
    blue: int

    def as_tuple(self) -> tuple[int, int, int]:
        return self.red, self.green, self.blue


@dataclass(frozen=True, slots=True)
class BoundingBox:
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    def width(self) -> float:
        return self.max_x - self.min_x

    def height(self) -> float:
        return self.max_y - self.min_y


@dataclass(frozen=True, slots=True)
class VoronoiCell:
    site_index: int
    polygon: tuple[Point2D, ...]


@dataclass(frozen=True, slots=True)
class VoronoiDiagram:
    sites: tuple[Point2D, ...]
    colors: tuple[RGBColor, ...]
    bounding_box: BoundingBox
    cells: tuple[VoronoiCell, ...]
