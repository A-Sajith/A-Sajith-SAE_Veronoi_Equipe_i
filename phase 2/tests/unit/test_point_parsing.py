import pytest

from voronoi_app.application.point_parsing import parse_points_text
from voronoi_app.domain.errors import ParseError


def test_parse_points_accepts_spaces_and_decimals() -> None:
    points = parse_points_text(" 2,4\n5.3, 4.5 \n")
    assert [(p.x, p.y) for p in points] == [(2.0, 4.0), (5.3, 4.5)]


def test_parse_points_ignores_empty_lines() -> None:
    points = parse_points_text("\n\n1,2\n\n3,4\n")
    assert len(points) == 2


def test_parse_points_rejects_wrong_separator() -> None:
    with pytest.raises(ParseError):
        parse_points_text("1;2\n")


def test_parse_points_rejects_non_numeric() -> None:
    with pytest.raises(ParseError):
        parse_points_text("1,abc\n")


def test_parse_points_rejects_extra_values() -> None:
    with pytest.raises(ParseError):
        parse_points_text("1,2,3\n")


def test_parse_points_rejects_empty_file() -> None:
    with pytest.raises(ParseError):
        parse_points_text("\n\n")


def test_parse_points_accepts_negative_coordinates() -> None:
    points = parse_points_text("-1,-2\n")
    assert [(p.x, p.y) for p in points] == [(-1.0, -2.0)]


def test_parse_points_rejects_infinite_coordinates() -> None:
    with pytest.raises(ParseError):
        parse_points_text("1e309,0\n")


def test_parse_points_rejects_too_large_coordinates() -> None:
    with pytest.raises(ParseError):
        parse_points_text("10000000000,0\n")


def test_parse_points_rejects_too_many_points() -> None:
    text = "\n".join([f"{i},0" for i in range(0, 1002)]) + "\n"
    with pytest.raises(ParseError):
        parse_points_text(text)
