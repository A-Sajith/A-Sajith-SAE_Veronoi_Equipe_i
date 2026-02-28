from __future__ import annotations

import colorsys

from voronoi_app.domain.models import RGBColor


def assign_distinct_colors(count: int) -> list[RGBColor]:
    if count <= 0:
        return []

    golden_ratio_conjugate = 0.618033988749895
    hue = 0.0
    colors: list[RGBColor] = []

    for _ in range(count):
        hue = (hue + golden_ratio_conjugate) % 1.0
        red, green, blue = colorsys.hsv_to_rgb(hue, 0.60, 0.95)
        colors.append(
            RGBColor(
                red=int(round(red * 255)),
                green=int(round(green * 255)),
                blue=int(round(blue * 255)),
            )
        )

    return colors
