import ast
import json
import pathlib
import types
import unittest
from math import sqrt


DOSSIER_PHASE1 = pathlib.Path(__file__).resolve().parent
FICHIER_VORONOI = DOSSIER_PHASE1 / "voronoi.py"
FICHIER_POINTS = DOSSIER_PHASE1 / "pointplan.json"


def charger_fonction_voronoi():
   

    tree = ast.parse(FICHIER_VORONOI.read_text(encoding="utf-8"))
    func = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "voronoi")

    module = ast.Module(body=[func], type_ignores=[])
    code = compile(module, filename=str(FICHIER_VORONOI), mode="exec")

    ns = {
        "sqrt": sqrt,
        "ZOOM": 20,
        "OFFSET_X": 150,
        "OFFSET_Y": 150,
        "HEIGHT": 800,
    }
    exec(code, ns)
    return ns["voronoi"]


class TestPhase1(unittest.TestCase):
    def test_pointplan_json_est_valide(self):
        points = json.loads(FICHIER_POINTS.read_text(encoding="utf-8"))
        self.assertIsInstance(points, list)
        self.assertGreater(len(points), 0)
        self.assertTrue(all("x" in p and "y" in p for p in points))

    def test_fonction_voronoi_existe_et_prend_3_arguments(self):
        tree = ast.parse(FICHIER_VORONOI.read_text(encoding="utf-8"))
        func = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "voronoi")
        self.assertEqual([a.arg for a in func.args.args], ["liste_germes", "x", "y"])

    def test_voronoi_retourne_le_germe_le_plus_proche(self):
        voronoi = charger_fonction_voronoi()

        def germe(x, y):
            return types.SimpleNamespace(position=types.SimpleNamespace(x=x, y=y))

        g1 = germe(1, 1)
        g2 = germe(10, 10)

        x_screen = 1 * 20 + 150
        y_screen = 800 - (1 * 20 + 150)

        self.assertIs(voronoi([g1, g2], x_screen, y_screen), g1)
