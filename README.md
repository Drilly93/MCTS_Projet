# 🎮 Projet 2048 : Moteur et IA Avancées (MCTS, UCT, NMCS)

Ce dépôt contient une plateforme complète de recherche et de jeu pour le **2048**, incluant un moteur de jeu haute performance, une interface graphique interactive et une suite d'algorithmes d'Intelligence Artificielle basés sur la recherche arborescente stochastique.

## 📊 Performances Records
*Tests réalisés sur un échantillon de 100 parties par algorithme (Moyenne des scores) :*

| Algorithme | Score Moyen | Statut |
| :--- | :--- | :--- |
| **NMCS (Niveau 2 + Heuristique Expert)** | **71 336** | 🏆 Champion (Tuile 4096+) |
| **Flat Monte Carlo** | **34 192** | Stable (Tuile 2048) |
| **UCT MCTS** | **22 580** | Exploration (Tuile 2048) |

---

## 🏗️ Structure du Projet

Le projet est divisé en modules spécialisés pour garantir une séparation claire entre la logique de jeu, les algorithmes et les outils d'évaluation :

1.  **`game_2048.py`** : Noyau logique optimisé. Gère les fusions et l'état du plateau via des tuples 1D immuables pour maximiser la vitesse des simulations et la mise en cache.
2.  **`utils.py`** : Bibliothèque de **Rollouts** (Simulations). Propose trois stratégies :
    * **Brute** : Simulation aléatoire complète jusqu'au Game Over.
    * **Heuristique** : Simulation courte (20 coups) évaluant la survie par le nombre de cases vides.
    * **Expert** : Évaluation pondérée combinant monotonie, bonus de coin et fluidité des tuiles.
3.  **`UCT_MCTS.py`** : Implémentation du *Monte Carlo Tree Search* utilisant la formule **UCB1** pour équilibrer l'exploration de nouvelles branches et l'exploitation des chemins connus.
4.  **`NMCS.py`** : IA *Nested Monte Carlo Search* optimisée. Inclut la mémoïisation (cache d'états) et l'élagage de branches pour une exécution en temps réel.
5.  **`monte_carlo_classique.py`** : IA "Flat" Monte Carlo effectuant des statistiques directes sur les coups immédiats.
6.  **`benchmark.py`** : Outil de test automatisé. Permet de comparer les IA, de mesurer la variance des scores et d'exporter les logs en `.txt`.
7.  **`interface_graphique.py`** : Moteur de rendu Tkinter pour jouer manuellement ou visualiser l'IA.

---

## 🚀 Instructions d'Exécution

### 1. Mode Benchmark (Analyse de Performance)
Utilisez cet outil pour générer des données statistiques sur l'efficacité des algorithmes.
```bash
# Tester le MCTS avec rollout heuristique (20 parties, 200 itérations par coup)
python benchmark.py --method MCTS --rollout heuristique --games 20 --power 300

# Tester le NMCS niveau 2
python benchmark.py --method NMCS --power 2 --games 5