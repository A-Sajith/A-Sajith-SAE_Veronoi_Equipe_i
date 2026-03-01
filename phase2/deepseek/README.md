# Voronoï — Deepseek (GUI + SciPy)

Ce dossier contient un lanceur d’application graphique qui :
- lit/importe un fichier de points ;
- calcule un diagramme de Voronoï via **SciPy** ;
- affiche le résultat avec **Matplotlib** ;
- permet l’export du diagramme (via un exporter Matplotlib).

> Remarque : dans l’état actuel du dépôt, seuls `app.py` et le fichier de dépendances sont présents dans ce dossier. Le lanceur importe des modules `deepseek.*` (GUI, parser, algo, export) qui doivent exister dans le projet pour que l’application démarre.

## Prérequis

- Python 3.10+ (recommandé)
- Dépendances Python (voir `requirements`) :
  - `numpy`
  - `scipy`
  - `matplotlib`

## Installation

Depuis `phase2/deepseek/` :

```bash
python -m pip install -r requirements
```

## Lancer l’application

Depuis `phase2/deepseek/` :

```bash
python app.py
```

## Lancer les tests

Les tests fournis ici sont des **tests structuraux** (ils vérifient la structure de `app.py` et la cohérence des dépendances), afin de rester exécutables même si les modules `deepseek.*` importés par `app.py` ne sont pas encore présents dans le dépôt.

Depuis `phase2/deepseek/` :

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Dépannage

### `ModuleNotFoundError: No module named 'deepseek'`

Le fichier `app.py` fait :
- un ajout de `phase2/` au `sys.path` ;
- puis des imports `from deepseek....`.

Pour que ça fonctionne, il faut que le package Python `deepseek` (avec ses sous-dossiers `gui/`, `io/`, `algorithm/`, etc.) soit présent dans le workspace, typiquement sous :
- `phase2/deepseek/` (en tant que package), ou
- `phase2/deepseek/` (en tant que namespace package) avec les sous-modules.

Si ces fichiers ne sont pas dans le dépôt, il faut les ajouter/coller avant d’exécuter `python app.py`.

## Format de fichier de points

Le parseur utilisé s’appelle `SimplePointParser` ; le format attendu est  un fichier texte avec **une paire de coordonnées par ligne**, par exemple :

```txt
2,4
5.3,4.5
-10,20.5
0,0
```



