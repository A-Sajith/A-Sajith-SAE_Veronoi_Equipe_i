from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List, Tuple
from src.core.point import Point
from src.core.parse_error import ParseError

COORDINATE_PATTERN = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*$")
EMPTY_LINE_PATTERN = re.compile(r"^\s*$")


@dataclass(frozen=True)
class ParseResult:
    points: List[Point]
    errors: List[ParseError]


def parse_points_from_text(text: str) -> ParseResult:
    if not text or not text.strip():
        return ParseResult(points=[], errors=[])

    lines = text.splitlines()
    points: List[Point] = []
    errors: List[ParseError] = []

    for line_index, line in enumerate(lines):
        line_number = line_index + 1
        if EMPTY_LINE_PATTERN.match(line):
            continue
        result = _parse_coordinate_line(line, line_number)
        if isinstance(result, ParseError):
            errors.append(result)
        else:
            points.append(result)

    return ParseResult(points=points, errors=errors)


def _parse_coordinate_line(line: str, line_number: int) -> Point | ParseError:
    match = COORDINATE_PATTERN.match(line)
    if not match:
        return ParseError(
            line_number=line_number,
            raw_content=line.strip(),
            reason="format attendu : x,y (ex: 2,4 ou 5.3,4.5)",
        )
    x = float(match.group(1))
    y = float(match.group(2))
    try:
        return Point(x=x, y=y)
    except ValueError as error:
        return ParseError(line_number=line_number, raw_content=line.strip(), reason=str(error))
