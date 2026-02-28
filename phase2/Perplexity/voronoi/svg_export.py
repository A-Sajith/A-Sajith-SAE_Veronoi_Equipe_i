from __future__ import annotations
from pathlib import Path
from typing import Tuple

from .domain import VoronoiDiagram


class SvgExporter:
    def export(
            self,
            diagram: VoronoiDiagram,
            path: Path,
            size: Tuple[int, int] = (900, 700),
    ) -> None:
        width, height = size

        min_x, min_y, max_x, max_y = self._compute_full_bounds(diagram)

        view_w = max_x - min_x
        view_h = max_y - min_y

        if view_w == 0:
            view_w = 1
        if view_h == 0:
            view_h = 1

        with path.open("w", encoding="utf-8") as f:
            f.write(f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}" height="{height}"
    viewBox="{min_x} {-max_y} {view_w} {view_h}"
    style="background:white">

    <g stroke="black"
       stroke-width="{view_w * 0.002}"
       vector-effect="non-scaling-stroke"
       stroke-linecap="round"
       stroke-linejoin="round"
       fill="none">
''')

            # Edges
            for edge in diagram.edges:
                f.write(
                    f'<line x1="{edge.start[0]}" y1="{-edge.start[1]}" '
                    f'x2="{edge.end[0]}" y2="{-edge.end[1]}"/>\n'
                )

            f.write('</g>\n')

            # Points rouges uniquement
            f.write('<g>\n')

            point_radius = view_w * 0.01

            for cell in diagram.cells:
                if not hasattr(cell.site, "x"):
                    continue

                x = cell.site.x
                y = -cell.site.y

                f.write(
                    f'<circle cx="{x}" cy="{y}" r="{point_radius}" '
                    f'fill="red" stroke="darkred" '
                    f'stroke-width="{point_radius * 0.4}"/>\n'
                )

            f.write('</g>\n</svg>')

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