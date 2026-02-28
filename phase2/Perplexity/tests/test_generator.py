import pytest
from voronoi.domain import Point
from voronoi.generator import VoronoiGenerator

def test_generate_two_points() -> None:
    generator = VoronoiGenerator()
    points = [Point(0.0, 0.0), Point(2.0, 0.0)]
    diagram = generator.generate(points)
    assert len(diagram.edges) == 2
    assert len(diagram.cells) == 2

def test_generate_one_point() -> None:
    generator = VoronoiGenerator()
    points = [Point(0.0, 0.0)]
    diagram = generator.generate(points)
    assert len(diagram.cells) == 1

def test_generate_three_points() -> None:
    generator = VoronoiGenerator()
    points = [Point(0,0), Point(3,0), Point(1,2)]
    diagram = generator.generate(points)
    assert len(diagram.edges) > 0
