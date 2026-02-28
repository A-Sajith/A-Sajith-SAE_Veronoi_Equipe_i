from __future__ import annotations
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.x) or not math.isfinite(self.y):
            raise ValueError(f"Coordonnées invalides : x={self.x}, y={self.y}")

    def distance_to(self, other: Point) -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"
