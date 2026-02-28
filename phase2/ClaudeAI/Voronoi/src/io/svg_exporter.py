from __future__ import annotations
from src.core.voronoi_diagram import VoronoiDiagram
from src.core.bounding_box import BoundingBox

CELL_COLORS = [
    "#5865f2", "#eb459e", "#57f287", "#fee75c", "#ed4245",
    "#00b4d8", "#a050f0", "#ff9a33", "#50dcb4", "#c8c83c",
]

DEFAULT_SVG_WIDTH = 1200
DEFAULT_SVG_HEIGHT = 900


def export_diagram_to_svg(
    diagram: VoronoiDiagram,
    svg_width: int = DEFAULT_SVG_WIDTH,
    svg_height: int = DEFAULT_SVG_HEIGHT,
) -> str:
    parts = [
        _build_svg_header(svg_width, svg_height),
        _build_background(svg_width, svg_height),
        _build_defs(),
        _build_edge_group(diagram, svg_width, svg_height),
        _build_site_group(diagram, svg_width, svg_height),
        "</svg>",
    ]
    return "\n".join(parts)


def _build_svg_header(width: int, height: int) -> str:
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
    )


def _build_background(width: int, height: int) -> str:
    return f'  <rect width="{width}" height="{height}" fill="#0a0a0f"/>'


def _build_defs() -> str:
    return (
        "  <defs>"
        '<filter id="glow">'
        '<feGaussianBlur stdDeviation="3" result="blur"/>'
        "<feMerge><feMergeNode in=\"blur\"/><feMergeNode in=\"SourceGraphic\"/></feMerge>"
        "</filter>"
        "</defs>"
    )


def _world_to_svg(
    world_x: float, world_y: float, bb: BoundingBox, svg_width: int, svg_height: int
) -> tuple[float, float]:
    svg_x = ((world_x - bb.min_x) / bb.width()) * svg_width
    svg_y = ((world_y - bb.min_y) / bb.height()) * svg_height
    return svg_x, svg_y


def _build_edge_group(diagram: VoronoiDiagram, svg_width: int, svg_height: int) -> str:
    bb = diagram.bounding_box
    lines = ['  <g id="edges" filter="url(#glow)">']
    for edge in diagram.edges:
        x1, y1 = _world_to_svg(edge.x1, edge.y1, bb, svg_width, svg_height)
        x2, y2 = _world_to_svg(edge.x2, edge.y2, bb, svg_width, svg_height)
        lines.append(
            f'    <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#5865f2" stroke-width="1" opacity="0.5"/>'
        )
    lines.append("  </g>")
    return "\n".join(lines)


def _build_site_group(diagram: VoronoiDiagram, svg_width: int, svg_height: int) -> str:
    bb = diagram.bounding_box
    lines = ['  <g id="sites">']
    for index, site in enumerate(diagram.sites):
        cx, cy = _world_to_svg(site.x, site.y, bb, svg_width, svg_height)
        color = CELL_COLORS[index % len(CELL_COLORS)]
        lines.append(
            f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="18" fill="{color}" opacity="0.15"/>'
        )
        lines.append(
            f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="6" '
            f'fill="{color}" stroke="white" stroke-width="1.5"/>'
        )
        lines.append(
            f'    <text x="{cx+10:.1f}" y="{cy-10:.1f}" '
            f'font-family="monospace" font-size="11" fill="rgba(232,232,240,0.9)">'
            f"({site.x}, {site.y})</text>"
        )
    lines.append("  </g>")
    return "\n".join(lines)
