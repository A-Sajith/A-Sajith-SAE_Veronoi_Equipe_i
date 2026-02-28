#!/usr/bin/env python3
"""
Lance la suite complète de tests unitaires et d'intégration.

Usage:
    python run_tests.py            # tous les tests
    python run_tests.py unit       # tests unitaires uniquement
    python run_tests.py integration # tests d'intégration uniquement
    python run_tests.py -v         # mode verbeux
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def discover_and_run_tests(test_path: str, verbosity: int) -> unittest.TestResult:
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_path, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


def main() -> None:
    args = sys.argv[1:]
    verbosity = 2 if "-v" in args else 1
    filter_args = [a for a in args if a != "-v"]

    if not filter_args or filter_args[0] == "all":
        target = "tests"
        label = "tous les tests"
    elif filter_args[0] == "unit":
        target = "tests/unit"
        label = "tests unitaires"
    elif filter_args[0] == "integration":
        target = "tests/integration"
        label = "tests d'intégration"
    else:
        print(f"Argument inconnu : {filter_args[0]}")
        print("Usage: python run_tests.py [all|unit|integration] [-v]")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Voronoï — Suite de tests : {label}")
    print(f"{'='*60}\n")

    result = discover_and_run_tests(target, verbosity)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
