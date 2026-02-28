from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from .domain import Point


@dataclass
class PointFileFormatError(Exception):
    line_number: int
    line_content: str
    message: str

    def __str__(self) -> str:
        return (
            f"Invalid point format at line {self.line_number}: "
            f"{self.message!s} (content={self.line_content!r})"
        )


class PointFileImporter:
    def import_points(self, path: Path) -> List[Point]:
        if not path.exists():
            raise FileNotFoundError(str(path))

        points: List[Point] = []
        with path.open("r", encoding="utf-8") as handle:
            for index, raw_line in enumerate(handle, start=1):
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                point = self._parse_line(line, index)
                points.append(point)
        return points

    def _parse_line(self, line: str, line_number: int) -> Point:
        parts = line.split(",")
        if len(parts) != 2:
            raise PointFileFormatError(
                line_number=line_number,
                line_content=line,
                message="Expected format 'x,y'",
            )

        x_str = parts[0].strip()
        y_str = parts[1].strip()

        try:
            x_value = float(x_str)
        except ValueError:
            raise PointFileFormatError(
                line_number=line_number,
                line_content=line,
                message=f"Invalid x coordinate: {x_str!r}",
            )

        try:
            y_value = float(y_str)
        except ValueError:
            raise PointFileFormatError(
                line_number=line_number,
                line_content=line,
                message=f"Invalid y coordinate: {y_str!r}",
            )

        return Point(x=x_value, y=y_value)
