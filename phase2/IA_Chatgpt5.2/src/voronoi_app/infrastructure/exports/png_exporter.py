from __future__ import annotations

from io import BytesIO
from typing import Final

from PIL import Image, ImageDraw

from voronoi_app.domain.models import BoundingBox, Point2D, VoronoiDiagram


class PngExporter:
    def export(self, diagram: VoronoiDiagram, *, width: int, height: int) -> bytes:
        image = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(image, "RGBA")

        bbox = diagram.bounding_box

        # Match the Qt view behavior: draw into a centered square area.
        side = max(1, min(width, height))
        offset_x = (width - side) / 2.0
        offset_y = (height - side) / 2.0

        def to_px(point: Point2D) -> tuple[float, float]:
            x_norm = (point.x - bbox.min_x) / bbox.width()
            y_norm = (bbox.max_y - point.y) / bbox.height()
            return offset_x + x_norm * (side - 1), offset_y + y_norm * (side - 1)

        # 1) Fill cells (no black outline here; we draw unique edges once below)
        for cell in diagram.cells:
            rgb = diagram.colors[cell.site_index].as_tuple()
            fill = (*rgb, 60)
            fill_border = (*rgb, 90)
            polygon_pixels = [to_px(p) for p in cell.polygon]
            if len(polygon_pixels) >= 3:
                draw.polygon(polygon_pixels, fill=fill, outline=fill_border)

        # 2) Draw unique edges (avoid double-drawn borders)
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
            mapped = [to_px(p) for p in cell.polygon]
            if len(mapped) >= 2:
                for (x1, y1), (x2, y2) in zip(mapped, mapped[1:], strict=False):
                    add_edge(x1, y1, x2, y2)
                add_edge(mapped[-1][0], mapped[-1][1], mapped[0][0], mapped[0][1])

        edge_color: Final = (0, 0, 0, 255)
        edge_width: Final = 2
        for x1, y1, x2, y2 in unique_edges.values():
            draw.line((x1, y1, x2, y2), fill=edge_color, width=edge_width)

        # 3) Points on top
        for index, site in enumerate(diagram.sites):
            rgb = diagram.colors[index].as_tuple()
            x, y = to_px(site)
            radius = 3
            draw.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                fill=(*rgb, 255),
                outline=edge_color,
                width=1,
            )

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()
