# Projet 2048 - Moteur et Intelligence Artificielle (MCTS)

Ce dépôt contient une implémentation complète du jeu 2048 en Python, incluant un moteur de jeu optimisé, une interface graphique et un solveur basé sur l'algorithme de Monte Carlo.

## Structure du Projet

Le projet est divisé en trois modules interdépendants :

1. **game_2048.py** : Le noyau logique. Il gère l'état du plateau (stocké en tuple 1D pour la performance), les fusions de tuiles et la détection de fin de partie.
2. **interface_graphique.py** : Module de rendu utilisant la bibliothèque Tkinter. Permet le jeu manuel ou la visualisation de l'IA en temps réel.
3. **monte_carlo_classique.py** : Implémentation de l'IA. Utilise des simulations de type "Flat Monte Carlo" pour évaluer la qualité des coups possibles.

## Prérequis

- Python 3.6 ou version supérieure.
- La bibliothèque standard `tkinter` (généralement incluse avec l'installation de Python).

## Instructions d'Exécution


### Mode Automatique (IA)
Pour lancer l'intelligence artificielle et observer ses décisions :
```bash
python monte_carlo_classique.py
```

### Mode Manuel 

Pour jouer manuellement au 2048 :
```bash
python interface_graphique.py
```


SCORE : 
- 2048 avec MCTS : 34 192
- 2048 avec UCT_MCTS : 22 580
- 2048 avec NMCTS : 71 336