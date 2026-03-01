import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List
from ..model.point import Point
from ..model.voronoi_diagram import VoronoiDiagram
from ..io.point_parser import PointParser, ParseError
from ..algorithm.voronoi_calculator import VoronoiCalculator
from ..io.diagram_exporter import DiagramExporter
from .diagram_canvas import DiagramCanvas, MatplotlibDiagramRenderer
from .point_list_view import PointListView

class MainWindow(tk.Tk):
    def __init__(self,
                 point_parser: PointParser,
                 voronoi_calculator: VoronoiCalculator,
                 diagram_exporter: DiagramExporter):
        super().__init__()
        self.title("Voronoi Diagram Generator")
        self.geometry("1000x600")

        self.point_parser = point_parser
        self.voronoi_calculator = voronoi_calculator
        self.diagram_exporter = diagram_exporter

        self.current_points: List[Point] = []
        self.current_diagram: VoronoiDiagram = None
        self.point_colors: List[str] = []

        self._create_widgets()
        self._create_menu()

    def _create_widgets(self):
        left_frame = tk.Frame(self, width=250)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        tk.Label(left_frame, text="Points").pack()
        self.point_list_view = PointListView(left_frame)
        self.point_list_view.pack(fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.diagram_canvas = DiagramCanvas(right_frame, MatplotlibDiagramRenderer())
        self.diagram_canvas.pack(fill=tk.BOTH, expand=True)

    def _create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Import Points...", command=self.import_points)
        file_menu.add_command(label="Export SVG...", command=self.export_svg)
        file_menu.add_command(label="Export Image...", command=self.export_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    def import_points(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        try:
            points = self.point_parser.parse(file_path)
        except ParseError as e:
            messagebox.showerror("Parse Error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
            return

        self.current_points = points
        self.point_colors = self._generate_colors(len(points))
        self._refresh_point_list()
        self._compute_and_draw()

    def _generate_colors(self, count: int) -> List[str]:
        base_colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'brown', 'pink']
        return [base_colors[i % len(base_colors)] for i in range(count)]

    def _refresh_point_list(self):
        self.point_list_view.clear()
        for point, color in zip(self.current_points, self.point_colors):
            text = f"({point.x:.3f}, {point.y:.3f})"
            self.point_list_view.add_point(color, text)

    def _compute_and_draw(self):
        try:
            self.current_diagram = self.voronoi_calculator.compute(self.current_points)
        except Exception as e:
            messagebox.showerror("Computation Error", str(e))
            return
        self.diagram_canvas.draw_diagram(self.current_diagram, self.point_colors)

    def export_svg(self):
        if not self.current_diagram:
            messagebox.showwarning("No diagram", "Generate a diagram first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG files", "*.svg")])
        if file_path:
            self.diagram_exporter.export_svg(self.current_diagram, file_path, self.point_colors)

    def export_image(self):
        if not self.current_diagram:
            messagebox.showwarning("No diagram", "Generate a diagram first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.diagram_exporter.export_image(self.current_diagram, file_path, self.point_colors)