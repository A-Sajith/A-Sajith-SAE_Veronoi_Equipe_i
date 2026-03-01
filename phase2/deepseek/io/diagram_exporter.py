from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from ..model.voronoi_diagram import VoronoiDiagram

class DiagramExporter(ABC):
    @abstractmethod
    def export_svg(self, diagram: VoronoiDiagram, file_path: str, site_colors=None) -> None:
        pass

    @abstractmethod
    def export_image(self, diagram: VoronoiDiagram, file_path: str, site_colors=None, dpi=300) -> None:
        pass

class MatplotlibDiagramExporter(DiagramExporter):
    def __init__(self, renderer):
        self._renderer = renderer

    def export_svg(self, diagram: VoronoiDiagram, file_path: str, site_colors=None) -> None:
        fig, ax = plt.subplots()
        self._renderer.draw(ax, diagram, site_colors)
        ax.set_aspect('equal')
        plt.savefig(file_path, format='svg')
        plt.close(fig)

    def export_image(self, diagram: VoronoiDiagram, file_path: str, site_colors=None, dpi=300) -> None:
        fig, ax = plt.subplots()
        self._renderer.draw(ax, diagram, site_colors)
        ax.set_aspect('equal')
        plt.savefig(file_path, dpi=dpi)
        plt.close(fig)