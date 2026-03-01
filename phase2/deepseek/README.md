# Voronoï — Deepseek (GUI + SciPy)

Ce dossier contient une application graphique (Tkinter) qui :
- importe un fichier de points ;
- calcule un diagramme de Voronoï via **SciPy** ;
- affiche le résultat avec **Matplotlib** ;
- exporte le diagramme (SVG / image) via Matplotlib.

Le code est organisé en package Python `deepseek/` (GUI, parsing, algo, export, modèle) + tests.

## Prérequis

- Python 3.10+ (recommandé)
- Tkinter (inclus avec la plupart des installations Python sous Windows)
- Dépendances Python (voir `requirements.txt`) :
  - `numpy`
  - `scipy`
  - `matplotlib`

## Installation

Depuis `phase2/deepseek/` :

```bash
python -m pip install -r requirements.txt
```

## Lancer l’application

Option A — depuis `phase2/deepseek/` :

```bash
python app.py
```

Option B — depuis `phase2/` (exécution en module) :

```bash
python -m deepseek.app
```

> Si tu exécutes depuis un autre dossier, assure-toi que `phase2/` est dans le `PYTHONPATH`.

## Lancer les tests

Les tests sont écrits avec `unittest` (pas besoin de dépendance supplémentaire).

Depuis `phase2/` :

```bash
python -m unittest discover -s deepseek/tests
```

## Dépannage

### `ModuleNotFoundError: No module named 'deepseek'`

Ça arrive si tu lances l’application / les tests depuis un répertoire où `phase2/` n’est pas dans le chemin des imports.

Solutions simples :
- Lancer l’app depuis `phase2/deepseek/` avec `python app.py` (le script ajoute automatiquement `phase2/` au `sys.path`).
- Ou lancer depuis `phase2/` avec `python -m deepseek.app`.
- Pour les tests, rester dans `phase2/` et utiliser la commande `unittest` ci-dessus.

## Format de fichier de points

Le parseur utilisé s’appelle `SimplePointParser` ; le format attendu est un fichier texte avec **une paire de coordonnées par ligne**, séparées par une virgule :

```txt
2,4
5.3,4.5
-10,20.5
0,0
```





