from __future__ import annotations

import math
from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QFont, QFontMetricsF, QPainter, QPen
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsPolygonItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
)

from voronoi_app.domain.models import VoronoiDiagram


class VoronoiView(QGraphicsView):
    def __init__(self) -> None:
        super().__init__()
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        self._diagram: VoronoiDiagram | None = None

    def set_diagram(self, diagram: VoronoiDiagram) -> None:
        self._diagram = diagram
        self._render()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        if self._diagram is not None:
            self._render()

    def _render(self) -> None:
        diagram = self._diagram
        if diagram is None:
            return

        self._scene.clear()

        viewport_size = self.viewport().size()
        scene_width = float(viewport_size.width() if viewport_size.width() > 0 else 1200)
        scene_height = float(viewport_size.height() if viewport_size.height() > 0 else 800)

        self._scene.setSceneRect(0.0, 0.0, scene_width, scene_height)
        self.resetTransform()

        font = QFont()
        font.setPointSize(9)
        metrics = QFontMetricsF(font)

        world_bounds = _compute_world_bounds_from_sites(diagram)
        x_step = _nice_tick_step(world_bounds.max_x - world_bounds.min_x, target_tick_count=6)
        y_step = _nice_tick_step(world_bounds.max_y - world_bounds.min_y, target_tick_count=6)

        sample_x_texts = [_format_tick_value(world_bounds.min_x), _format_tick_value(world_bounds.max_x)]
        sample_y_texts = [_format_tick_value(world_bounds.min_y), _format_tick_value(world_bounds.max_y)]

        max_y_label_width = max((metrics.horizontalAdvance(text) for text in sample_y_texts), default=40.0)
        label_height = metrics.height()

        margins = _Margins(
            left=max(55.0, max_y_label_width + 18.0),
            right=15.0,
            top=15.0,
            bottom=max(45.0, (label_height * 2.0) + 18.0),
        )

        plot = _PlotRect.from_scene(scene_width=scene_width, scene_height=scene_height, margins=margins)
        if plot.width < 80 or plot.height < 80:
            return

        mapper = _CoordinateMapper(world=world_bounds, plot=plot)

        self._draw_axes_and_ticks(mapper=mapper, font=font, metrics=metrics, x_step=x_step, y_step=y_step)
        self._draw_voronoi(diagram=diagram, mapper=mapper)

    def _draw_voronoi(self, *, diagram: VoronoiDiagram, mapper: "_CoordinateMapper") -> None:
        edge_pen = QPen(QColor(0, 0, 0))
        edge_pen.setWidthF(1.2)
        edge_pen.setCosmetic(True)

        no_pen = QPen(Qt.PenStyle.NoPen)

        from PySide6.QtCore import QPointF
        from PySide6.QtGui import QPolygonF

        unique_edges: dict[tuple[int, int, int, int], tuple[float, float, float, float]] = {}

        def quantize(x: float, y: float) -> tuple[int, int]:
            return int(round(x * 4.0)), int(round(y * 4.0))

        def add_edge(x1: float, y1: float, x2: float, y2: float) -> None:
            if (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) < 0.25:
                return

            q1 = quantize(x1, y1)
            q2 = quantize(x2, y2)
            if q1 <= q2:
                key = (q1[0], q1[1], q2[0], q2[1])
                value = (x1, y1, x2, y2)
            else:
                key = (q2[0], q2[1], q1[0], q1[1])
                value = (x2, y2, x1, y1)

            unique_edges.setdefault(key, value)

        for cell in diagram.cells:
            color = diagram.colors[cell.site_index]
            fill = QColor(color.red, color.green, color.blue, 60)
            fill_border = QColor(color.red, color.green, color.blue, 90)
            fill_border_pen = QPen(fill_border)
            fill_border_pen.setWidthF(1.0)
            fill_border_pen.setCosmetic(True)

            mapped_points = [mapper.world_to_pixel(point.x, point.y) for point in cell.polygon]
            polygon = QPolygonF([QPointF(x, y) for x, y in mapped_points])
            item = QGraphicsPolygonItem(polygon)
            item.setPen(fill_border_pen)
            item.setBrush(QBrush(fill))
            item.setZValue(0)
            self._scene.addItem(item)

            if len(mapped_points) >= 2:
                for (x1, y1), (x2, y2) in zip(mapped_points, mapped_points[1:], strict=False):
                    add_edge(x1, y1, x2, y2)
                x_first, y_first = mapped_points[0]
                x_last, y_last = mapped_points[-1]
                add_edge(x_last, y_last, x_first, y_first)

        for x1, y1, x2, y2 in unique_edges.values():
            self._scene.addLine(x1, y1, x2, y2, edge_pen).setZValue(2)

        point_radius = 3.0
        for index, site in enumerate(diagram.sites):
            color = diagram.colors[index]
            qcolor = QColor(color.red, color.green, color.blue)
            x_px, y_px = mapper.world_to_pixel(site.x, site.y)
            ellipse = QGraphicsEllipseItem(x_px - point_radius, y_px - point_radius, point_radius * 2, point_radius * 2)
            ellipse.setPen(edge_pen)
            ellipse.setBrush(QBrush(qcolor))
            ellipse.setZValue(5)
            self._scene.addItem(ellipse)

    def _draw_axes_and_ticks(
        self,
        *,
        mapper: "_CoordinateMapper",
        font: QFont,
        metrics: QFontMetricsF,
        x_step: float,
        y_step: float,
    ) -> None:
        axis_pen = QPen(QColor(120, 120, 120))
        axis_pen.setWidthF(1.0)
        tick_pen = QPen(QColor(140, 140, 140))
        tick_pen.setWidthF(1.0)
        label_color = QColor(40, 40, 40)

        drawing_left, drawing_top, drawing_width, drawing_height = mapper.drawing_rect()
        drawing_right = drawing_left + drawing_width
        drawing_bottom = drawing_top + drawing_height

        frame = QGraphicsRectItem(drawing_left, drawing_top, drawing_width, drawing_height)
        frame.setPen(axis_pen)
        frame.setBrush(Qt.BrushStyle.NoBrush)
        frame.setZValue(-10)
        self._scene.addItem(frame)

        x_axis_y = drawing_bottom
        y_axis_x = drawing_left

        self._scene.addLine(drawing_left, x_axis_y, drawing_right, x_axis_y, axis_pen).setZValue(-10)
        self._scene.addLine(y_axis_x, drawing_top, y_axis_x, drawing_bottom, axis_pen).setZValue(-10)

        tick_length = 6.0

        world = mapper.world
        x_tick = math.ceil(world.min_x / x_step) * x_step
        while x_tick <= world.max_x + 1e-12:
            x_px, _ = mapper.world_to_pixel(x_tick, world.min_y)
            x_px = _clamp(x_px, drawing_left, drawing_right)
            self._scene.addLine(x_px, x_axis_y, x_px, x_axis_y + tick_length, tick_pen).setZValue(-10)

            text = _format_tick_value(x_tick)
            text_width = metrics.horizontalAdvance(text)
            label_x = _clamp(x_px - text_width / 2.0, drawing_left, drawing_right - text_width)
            label_y = _clamp(x_axis_y + tick_length + 2.0, drawing_bottom + 2.0, mapper.plot.scene_height - metrics.height() - 1.0)
            label = QGraphicsTextItem(text)
            label.setFont(font)
            label.setDefaultTextColor(label_color)
            label.setPos(label_x, label_y)
            label.setZValue(-10)
            self._scene.addItem(label)

            x_tick += x_step

        y_tick = math.ceil(world.min_y / y_step) * y_step
        while y_tick <= world.max_y + 1e-12:
            _, y_px = mapper.world_to_pixel(world.min_x, y_tick)
            y_px = _clamp(y_px, drawing_top, drawing_bottom)
            self._scene.addLine(y_axis_x - tick_length, y_px, y_axis_x, y_px, tick_pen).setZValue(-10)

            text = _format_tick_value(y_tick)
            text_width = metrics.horizontalAdvance(text)
            label_x = _clamp(y_axis_x - tick_length - 4.0 - text_width, 1.0, drawing_left - text_width - 1.0)
            label_y = _clamp(y_px - metrics.height() / 2.0, drawing_top, drawing_bottom - metrics.height())
            label = QGraphicsTextItem(text)
            label.setFont(font)
            label.setDefaultTextColor(label_color)
            label.setPos(label_x, label_y)
            label.setZValue(-10)
            self._scene.addItem(label)

            y_tick += y_step

        x_label = QGraphicsTextItem("X")
        x_label.setFont(font)
        x_label.setDefaultTextColor(label_color)
        x_label.setPos(drawing_right - metrics.horizontalAdvance("X") - 2.0, mapper.plot.scene_height - metrics.height() - 2.0)
        x_label.setZValue(-10)
        self._scene.addItem(x_label)

        y_label = QGraphicsTextItem("Y")
        y_label.setFont(font)
        y_label.setDefaultTextColor(label_color)
        y_label.setPos(2.0, drawing_top)
        y_label.setZValue(-10)
        self._scene.addItem(y_label)


@dataclass(frozen=True, slots=True)
class _WorldBounds:
    min_x: float
    max_x: float
    min_y: float
    max_y: float


@dataclass(frozen=True, slots=True)
class _Margins:
    left: float
    right: float
    top: float
    bottom: float


@dataclass(frozen=True, slots=True)
class _PlotRect:
    left: float
    top: float
    width: float
    height: float
    scene_width: float
    scene_height: float

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top + self.height

    @staticmethod
    def from_scene(*, scene_width: float, scene_height: float, margins: _Margins) -> "_PlotRect":
        available_width = max(1.0, scene_width - margins.left - margins.right)
        available_height = max(1.0, scene_height - margins.top - margins.bottom)

        side = max(1.0, min(available_width, available_height))
        left = margins.left + (available_width - side) / 2.0
        top = margins.top + (available_height - side) / 2.0

        return _PlotRect(left=left, top=top, width=side, height=side, scene_width=scene_width, scene_height=scene_height)


@dataclass(frozen=True, slots=True)
class _CoordinateMapper:
    world: _WorldBounds
    plot: _PlotRect

    def _content_inset_px(self) -> float:
        return 0.0

    def _content_rect(self) -> tuple[float, float, float, float]:
        inset = self._content_inset_px()
        left = self.plot.left + inset
        top = self.plot.top + inset
        width = max(self.plot.width - (2.0 * inset), 1.0)
        height = max(self.plot.height - (2.0 * inset), 1.0)
        return left, top, width, height

    def _uniform_scale(self) -> float:
        x_span = max(self.world.max_x - self.world.min_x, 1e-12)
        y_span = max(self.world.max_y - self.world.min_y, 1e-12)

        _, _, content_width, content_height = self._content_rect()
        return min(content_width / x_span, content_height / y_span)

    def _center_offsets(self, *, scale: float) -> tuple[float, float]:
        x_span = max(self.world.max_x - self.world.min_x, 1e-12)
        y_span = max(self.world.max_y - self.world.min_y, 1e-12)

        _, _, content_width, content_height = self._content_rect()
        drawing_width = x_span * scale
        drawing_height = y_span * scale

        offset_x = max((content_width - drawing_width) / 2.0, 0.0)
        offset_y = max((content_height - drawing_height) / 2.0, 0.0)
        return offset_x, offset_y

    def drawing_rect(self) -> tuple[float, float, float, float]:
        scale = self._uniform_scale()
        offset_x, offset_y = self._center_offsets(scale=scale)

        x_span = max(self.world.max_x - self.world.min_x, 1e-12)
        y_span = max(self.world.max_y - self.world.min_y, 1e-12)

        content_left, content_top, _, _ = self._content_rect()
        drawing_width = x_span * scale
        drawing_height = y_span * scale
        return content_left + offset_x, content_top + offset_y, drawing_width, drawing_height

    def world_to_pixel(self, x: float, y: float) -> tuple[float, float]:
        scale = self._uniform_scale()

        drawing_left, drawing_top, _, _ = self.drawing_rect()
        x_px = drawing_left + (x - self.world.min_x) * scale
        y_px = drawing_top + (self.world.max_y - y) * scale
        return x_px, y_px


def _compute_world_bounds_from_sites(diagram: VoronoiDiagram) -> _WorldBounds:
    diagram_bbox = diagram.bounding_box
    return _WorldBounds(
        min_x=diagram_bbox.min_x,
        max_x=diagram_bbox.max_x,
        min_y=diagram_bbox.min_y,
        max_y=diagram_bbox.max_y,
    )


def _clamp(value: float, minimum: float, maximum: float) -> float:
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def _nice_tick_step(span: float, *, target_tick_count: int = 8) -> float:
    if span <= 0:
        return 1.0

    rough_step = span / max(2, target_tick_count)
    magnitude = 10 ** math.floor(math.log10(rough_step))
    normalized = rough_step / magnitude

    if normalized <= 1:
        nice = 1
    elif normalized <= 2:
        nice = 2
    elif normalized <= 5:
        nice = 5
    else:
        nice = 10

    return nice * magnitude


def _format_tick_value(value: float) -> str:
    if abs(value) < 1e-12:
        value = 0.0
    return f"{value:.6g}"
