# Voronoï — Perplexity (Tkinter)

Application desktop (Python + **Tkinter**) qui :
- importe un fichier texte contenant une coordonnée par ligne au format `x,y` ;
- calcule un diagramme de Voronoï ;
- affiche les arêtes du diagramme et les points sources ;
- exporte le rendu en **SVG** et en **PNG**.

## Prérequis

- Python 3.10+ (recommandé)

Dépendances (voir `requirements.txt`) :
- `numpy`
- `scipy`
- `Pillow`
- `pytest` (tests)

## Installation

Depuis `phase2/Perplexity/` :

```bash
python -m pip install -r requirements.txt
```

## Lancer l’application

Depuis `phase2/Perplexity/` :

```bash
python main.py
```

Dans l’interface :
1. **Importer points** → choisir un fichier `.txt`
2. **Calculer Voronoi**
3. Optionnel : **Exporter SVG** / **Exporter PNG**

## Lancer les tests

Depuis `phase2/Perplexity/` :

```bash
pytest
```

## Format de fichier accepté

Un fichier texte `.txt` avec une paire de coordonnées par ligne :

```txt
2,4
5.3,4.5
-10,20.5
0,0
```

Règles (implémentées dans `voronoi/parsing.py`) :
- séparateur : virgule `,`
- espaces tolérés autour des valeurs
- nombres entiers ou décimaux (point `.`)
- lignes vides ignorées
- lignes commentées possibles si elles commencent par `#`
- erreur bloquante si une ligne n’est pas au format attendu (`PointFileFormatError`)

## Exports

- **SVG** : export des arêtes (lignes noires) + points sources (cercles rouges)
- **PNG** : export raster (lignes noires + points rouges)

## Structure

```
phase2/Perplexity/
├── main.py
├── requirements.txt
├── points_test.txt
├── ui/
│   └── main_window.py
├── voronoi/
│   ├── controller.py
│   ├── domain.py
│   ├── generator.py
│   ├── parsing.py
│   ├── svg_export.py
│   └── image_export.py
└── tests/
    ├── test_flow.py
    ├── test_generator.py
    ├── test_image_export.py
    ├── test_parsing.py
    └── test_svg_export.py
```

## Notes sur l’algorithme

- Pour **3 points ou plus**, la génération utilise `scipy.spatial.Voronoi`.
- Des **points auxiliaires** (4 coins autour du nuage de points) sont ajoutés pour aider à obtenir des arêtes finies.
- Cas particuliers :
  - **0 point** → diagramme vide
  - **1 point** → 1 cellule sans arêtes
  - **2 points** → bissectrice (représentée par 2 segments)
- Si SciPy échoue, un **fallback** simple génère des segments approximatifs.

## Lien du prompt
https://www.perplexity.ai/search/je-suis-etudiante-en-3e-annee-KjaMUmFyR82LVzyqtXeZmw?sm=d
