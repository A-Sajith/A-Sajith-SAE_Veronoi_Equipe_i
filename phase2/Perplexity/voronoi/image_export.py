from __future__ import annotations
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageDraw

from .domain import VoronoiDiagram


class ImageExporter:
    def export(
            self,
            diagram: VoronoiDiagram,
            path: Path,
            size: Tuple[int, int] = (900, 700),
    ) -> None:
        scale_factor = 3

        width, height = size
        W = width * scale_factor
        H = height * scale_factor

        image = Image.new("RGB", (W, H), "white")
        draw = ImageDraw.Draw(image)

        min_x, min_y, max_x, max_y = self._compute_full_bounds(diagram)
        margin = 60 * scale_factor

        scale_x = (W - 2 * margin) / max(1.0, (max_x - min_x))
        scale_y = (H - 2 * margin) / max(1.0, (max_y - min_y))
        scale = min(scale_x, scale_y)

        def to_screen(point):
            x, y = point
            sx = margin + (x - min_x) * scale
            sy = margin + (y - min_y) * scale
            return sx, H - sy

        # Edges
        for edge in diagram.edges:
            x1, y1 = to_screen(edge.start)
            x2, y2 = to_screen(edge.end)
            draw.line((x1, y1, x2, y2), fill="black", width=6)

        # Points rouges uniquement
        for cell in diagram.cells:
            if not hasattr(cell.site, "x"):
                continue

            sx, sy = to_screen((cell.site.x, cell.site.y))
            r = 20

            draw.ellipse(
                (sx - r, sy - r, sx + r, sy + r),
                fill="red",
                outline="darkred",
                width=6,
            )

        image = image.resize((width, height), Image.LANCZOS)

        if path.suffix.lower() in [".jpg", ".jpeg"]:
            image.save(path, quality=95)
        else:
            image.save(path)

    def _compute_full_bounds(
            self, diagram: VoronoiDiagram
    ) -> tuple[float, float, float, float]:
        all_x = []
        all_y = []

        for edge in diagram.edges:
            all_x.extend([edge.start[0], edge.end[0]])
            all_y.extend([edge.start[1], edge.end[1]])

        for cell in diagram.cells:
            if hasattr(cell.site, "x"):
                all_x.append(cell.site.x)
                all_y.append(cell.site.y)

        if not all_x:
            return -10, -10, 10, 10

        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        padding_x = (max_x - min_x) * 0.2
        padding_y = (max_y - min_y) * 0.2

        return (
            min_x - padding_x,
            min_y - padding_y,
            max_x + padding_x,
            max_y + padding_y,
        )