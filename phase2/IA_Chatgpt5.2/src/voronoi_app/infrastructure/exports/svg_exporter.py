from __future__ import annotations

import math
from xml.sax.saxutils import escape

from voronoi_app.domain.models import Point2D, VoronoiDiagram


class SvgExporter:
    def export(self, diagram: VoronoiDiagram) -> str:
        bbox = diagram.bounding_box
        world_width = bbox.width()
        world_height = bbox.height()
        if world_width <= 0 or world_height <= 0:
            raise ValueError("Bounding box invalide pour l'export SVG")

        export_width_px = 1600
        export_height_px = 1000
        scale = min(export_width_px / world_width, export_height_px / world_height)
        if not math.isfinite(scale) or scale <= 0:
            scale = 1.0

        point_radius_px = 3.0
        stroke_width_px = 1.0
        point_radius_world = point_radius_px / scale
        stroke_width_world = stroke_width_px / scale

        fill_border_width_world = stroke_width_world

        def to_svg_x(x: float) -> float:
            return x - bbox.min_x

        def to_svg_y(y: float) -> float:
            return (bbox.max_y - y)

        polygons_svg: list[str] = []
        unique_edges: dict[tuple[int, int, int, int], tuple[float, float, float, float]] = {}

        def quantize(x: float, y: float) -> tuple[int, int]:
            return int(round(x * 4.0)), int(round(y * 4.0))

        def add_edge(x1: float, y1: float, x2: float, y2: float) -> None:
            if (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) < 0.25:
                return

            q1 = quantize(x1, y1)
            q2 = quantize(x2, y2)
            if q1 <= q2:
                key = (q1[0], q1[1], q2[0], q2[1])
                value = (x1, y1, x2, y2)
            else:
                key = (q2[0], q2[1], q1[0], q1[1])
                value = (x2, y2, x1, y1)

            unique_edges.setdefault(key, value)

        for cell in diagram.cells:
            color = diagram.colors[cell.site_index]
            mapped_points = [(to_svg_x(point.x), to_svg_y(point.y)) for point in cell.polygon]
            points_attribute = " ".join(f"{x:.6f},{y:.6f}" for x, y in mapped_points)
            polygons_svg.append(
                "<polygon "
                f"points=\"{escape(points_attribute)}\" "
                f"fill=\"rgb({color.red},{color.green},{color.blue})\" "
                "fill-opacity=\"0.35\" "
                f"stroke=\"rgb({color.red},{color.green},{color.blue})\" stroke-opacity=\"0.45\" "
                f"stroke-width=\"{fill_border_width_world:.6f}\" />"
            )

            if len(mapped_points) >= 2:
                for (x1, y1), (x2, y2) in zip(mapped_points, mapped_points[1:], strict=False):
                    add_edge(x1, y1, x2, y2)
                add_edge(mapped_points[-1][0], mapped_points[-1][1], mapped_points[0][0], mapped_points[0][1])

        edges_svg: list[str] = []
        for x1, y1, x2, y2 in unique_edges.values():
            edges_svg.append(
                "<line "
                f"x1=\"{x1:.6f}\" y1=\"{y1:.6f}\" x2=\"{x2:.6f}\" y2=\"{y2:.6f}\" "
                f"stroke=\"black\" stroke-width=\"{stroke_width_world:.6f}\" />"
            )

        points_svg: list[str] = []
        for index, site in enumerate(diagram.sites):
            color = diagram.colors[index]
            points_svg.append(
                "<circle "
                f"cx=\"{to_svg_x(site.x):.6f}\" cy=\"{to_svg_y(site.y):.6f}\" r=\"{point_radius_world:.6f}\" "
                f"fill=\"rgb({color.red},{color.green},{color.blue})\" stroke=\"black\" stroke-width=\"{stroke_width_world:.6f}\" />"
            )

        content = "\n".join([*polygons_svg, *edges_svg, *points_svg])
        return (
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{export_width_px}\" height=\"{export_height_px}\" "
            f"viewBox=\"0 0 {world_width:.6f} {world_height:.6f}\" preserveAspectRatio=\"xMidYMid meet\">\n"
            f"{content}\n"
            "</svg>\n"
        )
