from abc import ABC, abstractmethod
from typing import List
from ..model.point import Point

class ParseError(Exception):
    pass

class PointParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> List[Point]:
        pass

class SimplePointParser(PointParser):
    def parse(self, file_path: str) -> List[Point]:
        points = []
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    x_str, y_str = line.split(',')
                    x = float(x_str.strip())
                    y = float(y_str.strip())
                    points.append(Point(x, y))
                except ValueError as e:
                    raise ParseError(f"Line {line_num}: invalid format - {line}") from e
        return points