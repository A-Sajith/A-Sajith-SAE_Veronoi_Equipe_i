from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QBrush, QColor, QIcon, QPainter, QPixmap

from voronoi_app.domain.models import VoronoiDiagram


class PointTableModel(QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()
        self._diagram: VoronoiDiagram | None = None

    def set_diagram(self, diagram: VoronoiDiagram) -> None:
        self.beginResetModel()
        self._diagram = diagram
        self.endResetModel()

    def rowCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        diagram = self._diagram
        return 0 if diagram is None else len(diagram.sites)

    def columnCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        return 3

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):  # noqa: N802
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return None
        return {0: "Couleur", 1: "x", 2: "y"}.get(section)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):  # noqa: N802
        diagram = self._diagram
        if diagram is None or not index.isValid():
            return None

        row = index.row()
        column = index.column()
        site = diagram.sites[row]

        if column == 0 and role == Qt.ItemDataRole.DecorationRole:
            color = diagram.colors[row]
            pixmap = QPixmap(20, 20)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setBrush(QBrush(QColor(color.red, color.green, color.blue)))
            painter.setPen(QColor(0, 0, 0))
            painter.drawEllipse(2, 2, 16, 16)
            painter.end()
            return QIcon(pixmap)

        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if column == 1:
            return f"{site.x:.6g}"
        if column == 2:
            return f"{site.y:.6g}"
        return None
