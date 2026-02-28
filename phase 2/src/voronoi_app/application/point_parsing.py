from __future__ import annotations

import math
import re

from voronoi_app.domain.errors import ParseError
from voronoi_app.domain.models import Point2D


_FLOAT_PATTERN = re.compile(
    r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$"
)


MAX_POINTS = 1000
MAX_ABS_COORD = 1e9


def parse_points_text(text: str) -> list[Point2D]:
    points: list[Point2D] = []
    for index, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("#"):
            continue

        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 2:
            raise ParseError("format attendu: x,y", line_number=index, line_text=raw_line)

        x_text, y_text = parts
        if not _FLOAT_PATTERN.match(x_text) or not _FLOAT_PATTERN.match(y_text):
            raise ParseError("coordonnées non numériques", line_number=index, line_text=raw_line)

        x_value = float(x_text)
        y_value = float(y_text)

        if not (math.isfinite(x_value) and math.isfinite(y_value)):
            raise ParseError("coordonnées non finies (inf/-inf)", line_number=index, line_text=raw_line)

        if abs(x_value) > MAX_ABS_COORD or abs(y_value) > MAX_ABS_COORD:
            raise ParseError(
                f"coordonnées trop grandes (|x| ou |y| > {MAX_ABS_COORD:g})",
                line_number=index,
                line_text=raw_line,
            )

        points.append(Point2D(x=x_value, y=y_value))

        if len(points) > MAX_POINTS:
            raise ParseError(f"trop de points (maximum {MAX_POINTS})")

    if not points:
        raise ParseError("aucun point valide trouvé")

    return points
