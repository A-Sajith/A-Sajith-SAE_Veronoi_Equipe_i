from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from voronoi_app.presentation.qt.main_window import MainWindow


def run_qt_application() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
