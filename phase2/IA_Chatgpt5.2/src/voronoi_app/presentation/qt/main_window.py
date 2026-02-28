from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from voronoi_app.application.point_parsing import parse_points_text
from voronoi_app.application.voronoi_service import build_voronoi_diagram
from voronoi_app.domain.errors import ParseError, VoronoiComputationError
from voronoi_app.domain.models import VoronoiDiagram
from voronoi_app.infrastructure.exports.png_exporter import PngExporter
from voronoi_app.infrastructure.exports.svg_exporter import SvgExporter
from voronoi_app.presentation.qt.point_table_model import PointTableModel
from voronoi_app.presentation.qt.voronoi_view import VoronoiView


@dataclass(frozen=True, slots=True)
class _LoadedData:
    text: str
    diagram: VoronoiDiagram


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Diagramme de Voronoï")

        self._svg_exporter = SvgExporter()
        self._png_exporter = PngExporter()

        self._loaded: _LoadedData | None = None

        self._view = VoronoiView()
        self._table_model = PointTableModel()
        self._table = QTableView()
        self._configure_table()

        self._import_button = QPushButton("Importer")
        self._export_svg_button = QPushButton("Exporter SVG")
        self._export_png_button = QPushButton("Exporter Image")
        self._set_export_enabled(False)
        self._connect_signals()

        self.setCentralWidget(self._build_central_widget())
        self.resize(1200, 800)

    def _configure_table(self) -> None:
        self._table.setModel(self._table_model)
        self._table.verticalHeader().setVisible(False)
        self._table.verticalHeader().setDefaultSectionSize(28)
        self._table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self._table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self._table.setAlternatingRowColors(True)
        from PySide6.QtCore import QSize

        self._table.setIconSize(QSize(20, 20))
        self._table.setColumnWidth(0, 70)

    def _connect_signals(self) -> None:
        self._import_button.clicked.connect(self._on_import_clicked)
        self._export_svg_button.clicked.connect(self._on_export_svg_clicked)
        self._export_png_button.clicked.connect(self._on_export_png_clicked)

    def _set_export_enabled(self, enabled: bool) -> None:
        self._export_svg_button.setEnabled(enabled)
        self._export_png_button.setEnabled(enabled)

    def _build_central_widget(self) -> QWidget:
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(10, 10, 10, 10)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.addWidget(self._import_button)
        buttons_layout.addWidget(self._export_svg_button)
        buttons_layout.addWidget(self._export_png_button)
        buttons_layout.addStretch(1)
        root_layout.addLayout(buttons_layout)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self._view, 3)
        content_layout.addWidget(self._table, 1)
        root_layout.addLayout(content_layout, 1)

        return root

    def _on_import_clicked(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Importer des points", "", "Fichiers texte (*.txt);;Tous les fichiers (*)")
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                text = handle.read()
            points = parse_points_text(text)
            diagram = build_voronoi_diagram(points)
        except (OSError, ParseError, VoronoiComputationError) as exc:
            QMessageBox.critical(self, "Erreur", str(exc))
            return

        self._loaded = _LoadedData(text=text, diagram=diagram)
        self._view.set_diagram(diagram)
        self._table_model.set_diagram(diagram)
        self._set_export_enabled(True)

    def _on_export_svg_clicked(self) -> None:
        loaded = self._loaded
        if loaded is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Exporter SVG", "voronoi.svg", "SVG (*.svg)")
        if not file_path:
            return

        svg_text = self._svg_exporter.export(loaded.diagram)
        try:
            with open(file_path, "w", encoding="utf-8") as handle:
                handle.write(svg_text)
        except OSError as exc:
            QMessageBox.critical(self, "Erreur", str(exc))

    def _on_export_png_clicked(self) -> None:
        loaded = self._loaded
        if loaded is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Exporter image", "voronoi.png", "PNG (*.png)")
        if not file_path:
            return

        png_bytes = self._png_exporter.export(loaded.diagram, width=1600, height=1000)
        try:
            with open(file_path, "wb") as handle:
                handle.write(png_bytes)
        except OSError as exc:
            QMessageBox.critical(self, "Erreur", str(exc))
