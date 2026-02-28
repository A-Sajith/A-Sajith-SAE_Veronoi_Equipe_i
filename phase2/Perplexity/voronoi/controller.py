from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from .domain import Point, VoronoiDiagram
from .parsing import PointFileImporter, PointFileFormatError
from .generator import VoronoiGenerator
from .svg_export import SvgExporter
from .image_export import ImageExporter


@dataclass
class ApplicationState:
    points: List[Point]
    diagram: VoronoiDiagram | None


class VoronoiController:
    def __init__(
            self,
            point_importer: PointFileImporter | None = None,
            generator: VoronoiGenerator | None = None,
            svg_exporter: SvgExporter | None = None,
            image_exporter: ImageExporter | None = None,
    ) -> None:
        self._point_importer = point_importer or PointFileImporter()
        self._generator = generator or VoronoiGenerator()
        self._svg_exporter = svg_exporter or SvgExporter()
        self._image_exporter = image_exporter or ImageExporter()
        self._state = ApplicationState(points=[], diagram=None)

    @property
    def state(self) -> ApplicationState:
        return self._state

    def load_points_file(self, path: Path) -> None:
        points = self._point_importer.import_points(path)
        self._state.points = points
        self._state.diagram = None

    def compute_diagram(self) -> None:
        diagram = self._generator.generate(self._state.points)
        self._state.diagram = diagram

    def export_svg(self, path: Path) -> None:
        if self._state.diagram is None:
            self.compute_diagram()
        if self._state.diagram is None:
            return
        self._svg_exporter.export(self._state.diagram, path)

    def export_image(self, path: Path) -> None:
        if self._state.diagram is None:
            self.compute_diagram()
        if self._state.diagram is None:
            return
        self._image_exporter.export(self._state.diagram, path)
