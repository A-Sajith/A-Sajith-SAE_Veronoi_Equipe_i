from voronoi_app.application.color_assignment import assign_distinct_colors


def test_assign_distinct_colors_is_deterministic() -> None:
    colors_1 = assign_distinct_colors(5)
    colors_2 = assign_distinct_colors(5)
    assert colors_1 == colors_2


def test_assign_distinct_colors_returns_unique_first_values() -> None:
    colors = assign_distinct_colors(20)
    assert len({c.as_tuple() for c in colors}) == 20
