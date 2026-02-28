from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
from src.core.point import Point


@dataclass(frozen=True)
class BoundingBox:
    min_x: float
    max_x: float
    min_y: float
    max_y: float

    @classmethod
    def from_points(cls, points: Sequence[Point], padding: float = 60.0) -> BoundingBox:
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        return cls(
            min_x=min(xs) - padding,
            max_x=max(xs) + padding,
            min_y=min(ys) - padding,
            max_y=max(ys) + padding,
        )

    def width(self) -> float:
        return self.max_x - self.min_x

    def height(self) -> float:
        return self.max_y - self.min_y

    def to_dict(self) -> dict:
        return {
            "minX": self.min_x,
            "maxX": self.max_x,
            "minY": self.min_y,
            "maxY": self.max_y,
        }
