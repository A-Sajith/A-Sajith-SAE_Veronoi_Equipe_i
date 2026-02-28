#!/usr/bin/env python3
"""
Voronoï — Générateur de diagrammes
BUT Informatique 3ème année

Usage:
    python main.py            # démarre le serveur sur le port 8765
    python main.py --port 9000
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.ui.http_server import start_server


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Générateur de diagrammes de Voronoï"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Port du serveur HTTP (défaut: 8765)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    start_server(port=args.port)


if __name__ == "__main__":
    main()
