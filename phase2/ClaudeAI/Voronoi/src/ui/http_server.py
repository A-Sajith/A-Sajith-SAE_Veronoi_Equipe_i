from __future__ import annotations
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

from src.core.voronoi_computer import compute_voronoi_diagram
from src.io.point_file_parser import parse_points_from_text
from src.io.svg_exporter import export_diagram_to_svg

PUBLIC_DIR = Path(__file__).parent.parent / "public"
DEFAULT_PORT = 8765


class VoronoiRequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format_string: str, *args: Any) -> None:
        print(f"[{self.address_string()}] {format_string % args}")

    def do_GET(self) -> None:
        if self.path == "/" or self.path == "/index.html":
            # Chemin ABSOLU vers public/index.html depuis la racine du projet
            index_path = Path.cwd() / "public" / "index.html"
            self._serve_static_file(index_path, "text/html; charset=utf-8")
        else:
            self._send_json_error(404, "Route introuvable")

    def do_POST(self) -> None:
        if self.path == "/api/compute":
            self._handle_compute_voronoi()
        elif self.path == "/api/export/svg":
            self._handle_export_svg()
        else:
            self._send_json_error(404, "Route introuvable")

    def _handle_compute_voronoi(self) -> None:
        body = self._read_json_body()
        if body is None:
            return
        raw_text = body.get("text", "")
        parse_result = parse_points_from_text(raw_text)
        diagram = compute_voronoi_diagram(parse_result.points)
        response = {
            "diagram": diagram.to_dict(),
            "errors": [
                {
                    "lineNumber": error.line_number,
                    "rawContent": error.raw_content,
                    "reason": error.reason,
                }
                for error in parse_result.errors
            ],
        }
        self._send_json_response(200, response)

    def _handle_export_svg(self) -> None:
        body = self._read_json_body()
        if body is None:
            return
        raw_text = body.get("text", "")
        width = int(body.get("width", 1200))
        height = int(body.get("height", 900))
        parse_result = parse_points_from_text(raw_text)
        diagram = compute_voronoi_diagram(parse_result.points)
        svg_content = export_diagram_to_svg(diagram, svg_width=width, svg_height=height)
        self._send_text_response(200, svg_content, "image/svg+xml; charset=utf-8")

    def _read_json_body(self) -> dict | None:
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)
        try:
            return json.loads(raw_body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            self._send_json_error(400, f"Corps JSON invalide : {error}")
            return None

    def _serve_static_file(self, file_path: Path, content_type: str) -> None:
        try:
            content = file_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self._send_json_error(404, f"Fichier introuvable : {file_path.name}")

    def _send_json_response(self, status_code: int, data: Any) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_text_response(self, status_code: int, text: str, content_type: str) -> None:
        body = text.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_json_error(self, status_code: int, message: str) -> None:
        self._send_json_response(status_code, {"error": message})


def start_server(port: int = DEFAULT_PORT) -> None:
    server = HTTPServer(("localhost", port), VoronoiRequestHandler)
    print(f"🔷 Serveur Voronoï démarré → http://localhost:{port}")
    print("   Ctrl+C pour arrêter")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🔴 Serveur arrêté.")
        server.server_close()
