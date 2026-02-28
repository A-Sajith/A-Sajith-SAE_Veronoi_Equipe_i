# Voronoi App

Application desktop (Python + Qt) qui :
- Importe un fichier texte contenant une coordonnée par ligne au format `x,y` (espaces tolérés, décimaux supportés).
- Calcule et affiche le diagramme de Voronoï.
- Assigne une couleur distincte à chaque point et affiche une liste de points avec une pastille de couleur.
- Exporte le rendu en **SVG** et en **PNG**.

## Prérequis
- Windows + Python 3.12+

## Installation
Dans un terminal PowerShell à la racine du projet :

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip install -e .
```

## Lancer l’application

```powershell
.\.venv\Scripts\python.exe -m voronoi_app
```

Ou via le script :

```powershell
.\.venv\Scripts\voronoi-app.exe
```

## Lancer les tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```
