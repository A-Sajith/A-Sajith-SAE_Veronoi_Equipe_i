from abc import ABC, abstractmethod
from typing import List
from ..model.point import Point
from ..model.voronoi_diagram import VoronoiDiagram

class VoronoiCalculator(ABC):
    @abstractmethod
    def compute(self, points: List[Point]) -> VoronoiDiagram:
        pass