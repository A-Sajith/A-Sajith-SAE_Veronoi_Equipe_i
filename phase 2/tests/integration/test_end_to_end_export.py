from voronoi_app.application.controller import ApplicationController


def test_end_to_end_export_produces_svg_and_png() -> None:
    controller = ApplicationController()
    result = controller.export_all("0,0\n10,0\n5,10\n6,3\n", image_width=640, image_height=480)

    assert result.svg_text.lstrip().startswith("<?xml")
    assert "<svg" in result.svg_text
    assert result.png_bytes[:8] == b"\x89PNG\r\n\x1a\n"
