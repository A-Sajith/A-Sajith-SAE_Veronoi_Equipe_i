import sys
import os

# Ajoute le dossier parent (Desktop) au chemin de recherche des modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from deepseek.gui.main_window import MainWindow
from deepseek.io.point_parser import SimplePointParser
from deepseek.algorithm.scipy_calculator import ScipyVoronoiCalculator
from deepseek.io.diagram_exporter import MatplotlibDiagramExporter
from deepseek.gui.diagram_canvas import MatplotlibDiagramRenderer

def main():
    parser = SimplePointParser()
    calculator = ScipyVoronoiCalculator()
    renderer = MatplotlibDiagramRenderer()
    exporter = MatplotlibDiagramExporter(renderer)
    app = MainWindow(parser, calculator, exporter)
    app.mainloop()

if __name__ == "__main__":
    main()