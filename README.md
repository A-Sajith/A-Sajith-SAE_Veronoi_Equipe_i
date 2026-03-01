# SAÉ S6 — Diagrammes de Voronoï

## Aperçu du résultat — Phase 1

![Aperçu du diagramme de Voronoï (phase 1)](https://github.com/user-attachments/assets/abe65b09-890e-4fd5-a8fb-5752af209d3e)

Application permettant de générer un **diagramme de Voronoï** à partir d’une liste de points du plan, de le visualiser, et d’exporter le rendu en **SVG** et/ou **image**.

## Structure du dépôt

- `phase1/` — Implémentation « équipe » (à réaliser **sans IA** selon les consignes)
- `phase2/` — Implémentations produites avec des IAs génératrices + tests + bonnes pratiques
  - `ClaudeAI/Voronoi/` — Application web via serveur HTTP (stdlib uniquement)
  - `IA_Chatgpt5.2/` — Application desktop (Python + Qt/PySide6) packagée en module
  - `Perplexity/` — Application desktop (Tkinter)
  - deepseek
- `phase3_individuel/` — Analyses individuelles des risques liés à l’usage d’IAs génératrices

## Format des fichiers de points (consigne)

Le sujet demande un fichier texte contenant **une paire `x,y` par ligne** (virgule comme séparateur) :

```txt
2,4
5.3,4.5
18,29
12.5,23.7
```

Les implémentations de la phase 2 respectent ce format.

> Note : l’implémentation de la phase 1 présente dans ce dépôt lit actuellement un fichier JSON (`pointplan.json`).

---

# Phase 1 — Implémentation “équipe” (sans IA)

Emplacement : `phase1/voronoi.py`

## Fonctionnement

- Approche « raster » : chaque pixel de la fenêtre est colorié par le **germe le plus proche** (distance euclidienne) → cela forme bien les cellules de Voronoï.
- Affichage via **Pygame**.

## Lancer

Depuis la racine `A-Sajith-SAE_Veronoi_Equipe_i/` :

```bash
python phase1/voronoi.py
```

Entrée actuelle : `phase1/pointplan.json`.

Dépendances (à installer dans un environnement Python) : `pygame`, `numpy`.

---

# Phase 2 — Implémentations générées avec IAs (au moins 4 requis par la consigne)

> Consigne : utiliser au moins **4** IAs génératrices et conserver les prompts + mesurer le temps de corrections.
>
> Dans ce dépôt, 3 implémentations IA sont présentes (ClaudeAI, ChatGPT5.2, Perplexity). 

## 1) ClaudeAI — Serveur HTTP + UI web (stdlib uniquement)

Emplacement : `phase2/ClaudeAI/Voronoi/`

- Démarrer le serveur :

```bash
python main.py
# ou
python main.py --port 9000
```

- Ouvrir ensuite : `http://localhost:8765` (ou le port choisi)
- Tests :

```bash
python run_tests.py
```

Un lien de prompt ClaudeAI est référencé dans `phase2/ClaudeAI/Voronoi/README.md`.

## 2) ChatGPT5.2 — Application desktop Qt (PySide6) + pytest

Emplacement : `phase2/IA_Chatgpt5.2/`

Prérequis : Python >= 3.12.

Installation (exemple avec venv déjà créé) :

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip install -e .
```

Lancer :

```powershell
.\.venv\Scripts\python.exe -m voronoi_app
```

Tests :

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## 3) Perplexity — Application desktop Tkinter + pytest

Emplacement : `phase2/Perplexity/`

Installation :

```bash
python -m pip install -r requirements.txt
```

Lancer :

```bash
python main.py
```

Tests :

```bash
pytest
```

---

# Phase 3 — Risques (analyses individuelles)

Emplacement : `phase3_individuel/`
Les 6 themes choisis sont :
environnement 
coût économique, souveraineté et géopolitique
légalité et responsabilité 
conséquences sur les personnes travaillant avec l'IA
qualité du logiciel et de la maintenance
réputation et appropriation du produit par le public

## Équipe du projet

- Rania Bousfiha
- Royston Gnanapragasam
- Sajith Abdoul
- Lucas Ferard
- Ciffedinne Mahdjoub 
- Ryan Agin
