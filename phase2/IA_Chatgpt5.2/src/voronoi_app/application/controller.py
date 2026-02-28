from __future__ import annotations

from dataclasses import dataclass

from voronoi_app.application.point_parsing import parse_points_text
from voronoi_app.application.voronoi_service import build_voronoi_diagram
from voronoi_app.infrastructure.exports.png_exporter import PngExporter
from voronoi_app.infrastructure.exports.svg_exporter import SvgExporter


@dataclass(frozen=True, slots=True)
class ExportResult:
    svg_text: str
    png_bytes: bytes


class ApplicationController:
    def __init__(self, *, svg_exporter: SvgExporter | None = None, png_exporter: PngExporter | None = None) -> None:
        self._svg_exporter = svg_exporter or SvgExporter()
        self._png_exporter = png_exporter or PngExporter()

    def load_and_compute(self, points_text: str):
        points = parse_points_text(points_text)
        return build_voronoi_diagram(points)

    def export_all(self, points_text: str, *, image_width: int = 1200, image_height: int = 800) -> ExportResult:
        diagram = self.load_and_compute(points_text)
        svg_text = self._svg_exporter.export(diagram)
        png_bytes = self._png_exporter.export(diagram, width=image_width, height=image_height)
        return ExportResult(svg_text=svg_text, png_bytes=png_bytes)
