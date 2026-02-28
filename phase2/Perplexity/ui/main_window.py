from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional

from voronoi.controller import VoronoiController
from voronoi.parsing import PointFileFormatError


class MainWindow(tk.Frame):
    def __init__(self, master: tk.Tk | None = None) -> None:
        super().__init__(master)
        self.master = master or tk.Tk()
        self.master.title("Générateur de diagrammes de Voronoï")
        self.controller = VoronoiController()
        self.canvas_width = 800
        self.canvas_height = 600

        self._build_widgets()

    def _build_widgets(self) -> None:
        toolbar = tk.Frame(self.master)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        open_button = tk.Button(toolbar, text="Importer points", command=self._on_open_file)
        open_button.pack(side=tk.LEFT, padx=4, pady=4)

        compute_button = tk.Button(toolbar, text="Calculer Voronoi", command=self._on_compute)
        compute_button.pack(side=tk.LEFT, padx=4, pady=4)

        export_svg_button = tk.Button(toolbar, text="Exporter SVG", command=self._on_export_svg)
        export_svg_button.pack(side=tk.LEFT, padx=4, pady=4)

        export_img_button = tk.Button(toolbar, text="Exporter PNG", command=self._on_export_image)
        export_img_button.pack(side=tk.LEFT, padx=4, pady=4)

        self.status_label = tk.Label(toolbar, text="Aucun fichier chargé")
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _on_open_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier de points",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not file_path:
            return

        try:
            self.controller.load_points_file(Path(file_path))
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Fichier introuvable.")
            return
        except PointFileFormatError as error:
            messagebox.showerror("Erreur de format", str(error))
            return

        points_count = len(self.controller.state.points)
        self.status_label.config(text=f"{points_count} points chargés")
        self.canvas.delete("all")

    def _on_compute(self) -> None:
        self.controller.compute_diagram()
        diagram = self.controller.state.diagram
        if diagram is None or not diagram.edges:
            messagebox.showinfo("Info", "Diagramme vide ou insuffisant.")
            return
        self._draw_diagram()

    def _on_export_svg(self) -> None:
        file_path = filedialog.asksaveasfilename(
            title="Exporter en SVG",
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg")],
        )
        if not file_path:
            return
        self.controller.export_svg(Path(file_path))
        messagebox.showinfo("Export", "Fichier SVG exporté.")

    def _on_export_image(self) -> None:
        file_path = filedialog.asksaveasfilename(
            title="Exporter en image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
        )
        if not file_path:
            return
        self.controller.export_image(Path(file_path))
        messagebox.showinfo("Export", "Image exportée.")

    def _draw_diagram(self) -> None:
        self.canvas.delete("all")
        diagram = self.controller.state.diagram
        if diagram is None:
            return

        min_x, min_y, max_x, max_y = self._compute_bounds(diagram)
        margin = 20.0
        width = self.canvas_width
        height = self.canvas_height

        scale_x = (width - 2 * margin) / max(1.0, (max_x - min_x))
        scale_y = (height - 2 * margin) / max(1.0, (max_y - min_y))
        scale = min(scale_x, scale_y)

        # DESSINE LES BORDS DU DIAGRAMME VORONOI (lignes noires)
        for edge in diagram.edges:
            x1, y1 = self._to_screen(edge.start, min_x, min_y, margin, scale, height)
            x2, y2 = self._to_screen(edge.end, min_x, min_y, margin, scale, height)
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

        # DESSINE TOUS LES POINTS D'ORIGINE (points ROUGES)
        for point in self.controller.state.points:
            sx, sy = self._to_screen((point.x, point.y), min_x, min_y, margin, scale, height)
            r = 5
            self.canvas.create_oval(sx - r, sy - r, sx + r, sy + r,
                                    fill="red", outline="black", width=1)

    def _compute_bounds(self, diagram):
        # PRIORITÉ ABSOLUE : TOUS LES POINTS D'ORIGINE doivent être visibles
        points_xs = [p.x for p in self.controller.state.points]
        points_ys = [p.y for p in self.controller.state.points]

        # + tous les sommets des edges du diagramme
        edge_xs = [e.start[0] for e in diagram.edges] + [e.end[0] for e in diagram.edges]
        edge_ys = [e.start[1] for e in diagram.edges] + [e.end[1] for e in diagram.edges]

        all_xs = points_xs + edge_xs
        all_ys = points_ys + edge_ys

        min_x, max_x = min(all_xs), max(all_xs)
        min_y, max_y = min(all_ys), max(all_ys)

        # MARGE 20% pour éviter tout clipping
        margin_x = (max_x - min_x) * 0.2
        margin_y = (max_y - min_y) * 0.2

        return (min_x - margin_x, min_y - margin_y, max_x + margin_x, max_y + margin_y)

    def _to_screen(self, point, min_x, min_y, margin, scale, height):
        x, y = point
        sx = margin + (x - min_x) * scale
        sy = margin + (y - min_y) * scale
        return sx, height - sy

    def run(self) -> None:
        self.master.mainloop()
