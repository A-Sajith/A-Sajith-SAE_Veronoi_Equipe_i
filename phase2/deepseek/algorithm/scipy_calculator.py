import numpy as np
from scipy.spatial import Voronoi as ScipyVoronoi
from typing import List
from ..model.point import Point
from ..model.voronoi_diagram import VoronoiDiagram
from .voronoi_calculator import VoronoiCalculator

class ScipyVoronoiCalculator(VoronoiCalculator):
    def compute(self, points: List[Point]) -> VoronoiDiagram:
        n = len(points)
        if n == 1:
            # Un seul point : diagramme vide, le renderer dessinera tout l'espace
            return VoronoiDiagram(sites=points, vertices=[], ridges=[], regions=[], point_regions=[])
        elif n == 2:
            # Deux points : on retourne juste les sites, le renderer tracera la médiatrice
            return VoronoiDiagram(sites=points, vertices=[], ridges=[], regions=[], point_regions=[])
        else:
            # n >= 3 : calcul classique
            coords = np.array([(p.x, p.y) for p in points])
            vor = ScipyVoronoi(coords)
            diagram = VoronoiDiagram(
                sites=points,
                vertices=[Point(v[0], v[1]) for v in vor.vertices],
                ridges=[tuple(r) for r in vor.ridge_vertices if -1 not in r],
                regions=[r for r in vor.regions if r and -1 not in r],
                point_regions=list(vor.point_region)
            )
            return diagram