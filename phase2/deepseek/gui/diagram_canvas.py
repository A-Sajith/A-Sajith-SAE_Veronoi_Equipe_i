import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from scipy.spatial import Voronoi as ScipyVoronoi
from ..model.voronoi_diagram import VoronoiDiagram

class MatplotlibDiagramRenderer:
    def _finite_polygons(self, vor, radius=None):
        """
        Convert infinite Voronoi regions to finite polygons for plotting.
        """
        if vor.points.shape[1] != 2:
            raise ValueError("Requires 2D input")

        new_regions = []
        new_vertices = vor.vertices.tolist()

        center = vor.points.mean(axis=0)
        if radius is None:
            # Large radius to ensure polygons extend well beyond the visible area
            range_x = np.ptp(vor.points[:, 0])
            range_y = np.ptp(vor.points[:, 1])
            radius = max(range_x, range_y) * 10

        # Build a map of ridges for each point
        all_ridges = {}
        for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
            all_ridges.setdefault(p1, []).append((p2, v1, v2))
            all_ridges.setdefault(p2, []).append((p1, v1, v2))

        for point_idx, region_idx in enumerate(vor.point_region):
            vertices = vor.regions[region_idx]

            if all(v >= 0 for v in vertices):
                # Finite region
                new_regions.append(vertices)
                continue

            # Reconstruct infinite region
            ridges = all_ridges[point_idx]
            new_region = [v for v in vertices if v >= 0]

            for p2, v1, v2 in ridges:
                if v2 < 0 and v1 >= 0:
                    v1, v2 = v2, v1
                if v1 < 0:
                    # This ridge is infinite, add a far point
                    t = vor.points[p2] - vor.points[point_idx]
                    t /= np.linalg.norm(t)
                    n = np.array([-t[1], t[0]])  # normal
                    midpoint = vor.points[[point_idx, p2]].mean(axis=0)
                    direction = np.sign(np.dot(midpoint - center, n)) * n
                    far_point = vor.vertices[v2] + direction * radius

                    new_region.append(len(new_vertices))
                    new_vertices.append(far_point.tolist())

            # Sort region counterclockwise
            vs = np.array([new_vertices[v] for v in new_region])
            c = vs.mean(axis=0)
            angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
            new_region = [new_region[i] for i in np.argsort(angles)]
            new_regions.append(new_region)

        return new_regions, np.array(new_vertices)

    def draw(self, ax, diagram: VoronoiDiagram, site_colors=None):
        if not diagram.sites:
            return
        if site_colors is None:
            site_colors = ['blue'] * len(diagram.sites)

        n = len(diagram.sites)

        # ----- Cas spécial : 1 point -----
        if n == 1:
            point = diagram.sites[0]
            color = site_colors[0]
            margin = 1.0
            ax.set_xlim(point.x - margin, point.x + margin)
            ax.set_ylim(point.y - margin, point.y + margin)
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            rect = plt.Rectangle((xlim[0], ylim[0]),
                                  xlim[1] - xlim[0],
                                  ylim[1] - ylim[0],
                                  color=color, alpha=0.7)
            ax.add_patch(rect)
            ax.plot(point.x, point.y, 'o', color=color,
                    markersize=8, markeredgecolor='black')
            return

        # ----- Cas spécial : 2 points -----
        if n == 2:
            p1 = np.array([diagram.sites[0].x, diagram.sites[0].y])
            p2 = np.array([diagram.sites[1].x, diagram.sites[1].y])
            c1, c2 = site_colors[0], site_colors[1]

            # Vecteur direction de p1 vers p2
            d = p2 - p1
            # Équation de la médiatrice : d·x = (p2² - p1²)/2
            constante = (np.dot(p2, p2) - np.dot(p1, p1)) / 2.0

            # Déterminer les limites de la vue
            x_vals = [p1[0], p2[0]]
            y_vals = [p1[1], p2[1]]
            x_min, x_max = min(x_vals), max(x_vals)
            y_min, y_max = min(y_vals), max(y_vals)
            dx = x_max - x_min
            dy = y_max - y_min
            margin = max(dx, dy) * 0.8
            xlim = (x_min - margin, x_max + margin)
            ylim = (y_min - margin, y_max + margin)
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)

            # Créer un rectangle couvrant la vue
            corners = np.array([[xlim[0], ylim[0]],
                                [xlim[1], ylim[0]],
                                [xlim[1], ylim[1]],
                                [xlim[0], ylim[1]]])

            # Fonction de clipping pour un demi-plan défini par d·x < constante
            def clip_polygon(corners, a, b, c, keep_less):
                output = []
                for i in range(len(corners)):
                    curr = corners[i]
                    nxt = corners[(i+1) % len(corners)]
                    f_curr = a*curr[0] + b*curr[1] - c
                    f_next = a*nxt[0] + b*nxt[1] - c
                    curr_inside = f_curr < 0 if keep_less else f_curr > 0
                    next_inside = f_next < 0 if keep_less else f_next > 0
                    if curr_inside and next_inside:
                        output.append(nxt)
                    elif curr_inside and not next_inside:
                        t = f_curr / (f_curr - f_next)
                        inter = curr + t * (nxt - curr)
                        output.append(inter)
                    elif not curr_inside and next_inside:
                        t = f_curr / (f_curr - f_next)
                        inter = curr + t * (nxt - curr)
                        output.append(inter)
                        output.append(nxt)
                return np.array(output)

            a, b = d
            c = constante

            # Déterminer le côté de p1
            if np.dot(d, p1) < constante:
                poly1 = clip_polygon(corners, a, b, c, keep_less=True)
                poly2 = clip_polygon(corners, a, b, c, keep_less=False)
            else:
                poly1 = clip_polygon(corners, a, b, c, keep_less=False)
                poly2 = clip_polygon(corners, a, b, c, keep_less=True)

            if len(poly1) > 0:
                ax.fill(poly1[:,0], poly1[:,1], color=c1, alpha=0.7, edgecolor='none')
            if len(poly2) > 0:
                ax.fill(poly2[:,0], poly2[:,1], color=c2, alpha=0.7, edgecolor='none')

            # Tracer la médiatrice (ligne noire)
            if abs(a) > 1e-6:
                if abs(b) > 1e-6:
                    # Cas général : on cherche intersections avec les bords
                    x = np.array(xlim)
                    y_line = (constante - a*x) / b
                    mask = (y_line >= ylim[0]) & (y_line <= ylim[1])
                    if np.sum(mask) == 2:
                        ax.plot(x[mask], y_line[mask], 'k-', linewidth=1.5)
                    else:
                        y = np.array(ylim)
                        x_line = (constante - b*y) / a
                        mask2 = (x_line >= xlim[0]) & (x_line <= xlim[1])
                        if np.sum(mask2) == 2:
                            ax.plot(x_line[mask2], y[mask2], 'k-', linewidth=1.5)
                else:
                    # b == 0, droite verticale
                    x0 = constante / a
                    if xlim[0] <= x0 <= xlim[1]:
                        ax.plot([x0, x0], ylim, 'k-', linewidth=1.5)
            else:
                # a == 0, droite horizontale
                y0 = constante / b
                if ylim[0] <= y0 <= ylim[1]:
                    ax.plot(xlim, [y0, y0], 'k-', linewidth=1.5)

            # Tracer les points
            ax.plot(p1[0], p1[1], 'o', color=c1, markersize=8, markeredgecolor='black')
            ax.plot(p2[0], p2[1], 'o', color=c2, markersize=8, markeredgecolor='black')
            return

        # ----- Cas général : n >= 3 -----
        points = np.array([(p.x, p.y) for p in diagram.sites])
        vor = ScipyVoronoi(points)
        regions, vertices = self._finite_polygons(vor)

        # Fill each region with the corresponding site color
        for i, region in enumerate(regions):
            polygon = vertices[region]
            ax.fill(polygon[:, 0], polygon[:, 1],
                    color=site_colors[i], alpha=0.7, edgecolor='none')

        # Draw all ridges (including infinite ones) in black
        center = vor.points.mean(axis=0)
        range_x = np.ptp(vor.points[:, 0])
        range_y = np.ptp(vor.points[:, 1])
        radius = max(range_x, range_y) * 10  # same as in _finite_polygons

        for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
            if v1 >= 0 and v2 >= 0:
                # Finite ridge
                ax.plot([vertices[v1, 0], vertices[v2, 0]],
                        [vertices[v1, 1], vertices[v2, 1]],
                        'k-', linewidth=1.5)
            else:
                # Infinite ridge: find the finite vertex
                finite_v = v1 if v1 >= 0 else v2
                # Compute direction away from the region
                pt1 = vor.points[p1]
                pt2 = vor.points[p2]
                t = pt2 - pt1
                t /= np.linalg.norm(t)
                n_vec = np.array([-t[1], t[0]])  # normal
                midpoint = (pt1 + pt2) / 2
                # Determine sign based on side of center
                sign = np.sign(np.dot(midpoint - center, n_vec))
                direction = sign * n_vec
                far_point = vor.vertices[finite_v] + direction * radius
                ax.plot([vertices[finite_v, 0], far_point[0]],
                        [vertices[finite_v, 1], far_point[1]],
                        'k-', linewidth=1.5)

        # Draw sites as colored dots with black outline
        for point, color in zip(diagram.sites, site_colors):
            ax.plot(point.x, point.y, 'o', color=color,
                    markersize=8, markeredgecolor='black')

        # Force the plot to be a square around the points with extra margin
        x_vals = [p.x for p in diagram.sites]
        y_vals = [p.y for p in diagram.sites]
        x_min, x_max = min(x_vals), max(x_vals)
        y_min, y_max = min(y_vals), max(y_vals)
        dx = x_max - x_min
        dy = y_max - y_min
        margin = max(dx, dy) * 0.8
        ax.set_xlim(x_min - margin, x_max + margin)
        ax.set_ylim(y_min - margin, y_max + margin)
        ax.set_aspect('equal')

class DiagramCanvas(tk.Frame):
    def __init__(self, parent, renderer, **kwargs):
        super().__init__(parent, **kwargs)
        self.renderer = renderer
        self.figure = plt.Figure(figsize=(6, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw_diagram(self, diagram: VoronoiDiagram, site_colors=None):
        self.ax.clear()
        self.renderer.draw(self.ax, diagram, site_colors)
        self.canvas.draw()