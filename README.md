# Projet 2048 : Moteur et IA Avancées (MCTS, UCT, NMCS)

Ce dépôt contient une plateforme complète de recherche et de jeu pour le **2048**, incluant un moteur de jeu, une interface graphique interactive et une suite d'algorithmes d'Intelligence Artificielle basés sur les algos MCTS.

FICHIERS IMPORTANTS A REGARDER POUR EVALATION :
- `README.md` : Documentation du projet.
- `analyse.ipynb` : Notebook d'analyse des résultats de benchmark.
- `benchmark.py` : Script pour exécuter les benchmarks et générer des rapports de

## Structure du Projet

Le projet est divisé en modules spécialisés pour garantir une séparation claire entre la logique de jeu, les algorithmes et les outils d'évaluation :

1.  **`game_2048.py`** : Noyau logique optimisé. Gère les fusions et l'état du plateau via des tuples 1D immuables pour maximiser la vitesse des simulations et la mise en cache.

2.  **`utils.py`** : Bibliothèque de **Rollouts** (Simulations). Propose trois stratégies :
    * **Brute** : Simulation aléatoire complète jusqu'au Game Over.
    * **Heuristique** : Simulation courte (20 coups) évaluant la survie par le nombre de cases vides.
    * **Expert** : Évaluation pondérée combinant monotonie, bonus de coin et fluidité des tuiles.

3.  **`UCT_MCTS.py`** : Implémentation du *Monte Carlo Tree Search* utilisant la formule **UCB1** pour équilibrer l'exploration de nouvelles branches et l'exploitation des chemins connus.

4.  **`NMCS.py`** : IA *Nested Monte Carlo Search* optimisée. Inclut la mémorisation (cache d'états) et l'élagage de branches pour une exécution en temps réel.

5.  **`monte_carlo_classique.py`** : IA "Flat" Monte Carlo effectuant des statistiques directes sur les coups immédiats.

6. **`NRPA.py`** : Implémentation de l'algorithme Nested Rollout Policy Adaptation, une approche d'apprentissage par renforcement pour améliorer les politiques de simulation.

7. **`expectimax.py`** : Implémentation de l'algorithme Expectimax avec une heuristique d'évaluation avancée pour guider les simulations.

8.  **`benchmark.py`** : Outil de test automatisé. Permet de comparer les IA, de mesurer la variance des scores et d'exporter les logs en `.txt`.

9.  **`interface_graphique.py`** : Moteur de rendu Tkinter pour jouer manuellement ou visualiser l'IA.

---

## Instructions d'Exécution

## Configuration du Benchmark (Arguments CLI)

Le script `benchmark.py` utilise un système d'arguments pour piloter les tests. Voici les détails des paramètres principaux :

### 1. Algorithmes (`--method`)
* **`normal` (Flat Monte Carlo)** : Évaluation statistique brute de chaque coup immédiat.
* **`MCTS` (Monte Carlo Tree Search)** : Recherche arborescente équilibrée par la formule UCB1.
* **`NMCS` (Nested Monte Carlo)** : Recherche récursive où chaque simulation est guidée par une IA de niveau inférieur.
* **`expectimax`** : Recherche arborescente avec évaluation heuristique des états.
* **`nrpa`** : Algorithme d'apprentissage par renforcement pour optimiser les politiques de simulation.

### 2. Puissance de Calcul (`--power`)
L'argument `--power` définit le budget de réflexion par coup, mais son impact varie selon la méthode :
* **Flat MC** : Nombre de simulations par direction (ex: `100` power = 400 simulations totales).
* **MCTS** : Nombre d'itérations totales dans l'arbre (plus il est élevé, plus l'arbre est précis).
* **NMCS** : Nombre de tentatives par étage récursif (Attention : la complexité est exponentielle).
* **Expectimax** : Profondeur de recherche (ex: `2` pour explorer 2 coups à l'avance).
* **NRPA** : Nombre d'itérations d'adaptation de la politique utilisé afin de déterminer les meilleures séquences de coups.

### 3. Stratégies de Simulation (`--rollout`)
* **`brute`** : Joue au hasard jusqu'à la fin de la partie. Retourne le score final.
* **`heuristique`** : Simule jusqu'à `--prof`. Retourne le nombre de **cases vides** (priorité à la survie).
* **`expert`** : Simule jusqu'à `--prof`. Retourne une note pondérée (Monotonie, Coins, Espace).

### 4. Paramètres Avancés
* **`--games`** : Nombre de parties à lancer pour moyenner les résultats.
* **`--prof`** : Horizon de simulation (nombre de coups projetés dans le futur) pour le rollout version heuristique.
* **`--level`** : Profondeur de récursion pour le **NMCS** et le **Expectimax** (recommandé : 1 ou 2).
* **`--max_moves`** : Sécurité pour arrêter une partie si l'IA est trop performante et refuse de perdre.

---

### Demonstration visuelle des algos IA pour le jeu 2048

**Demonstration FlatMC** : `python monte_carlo_classique.py`
**Demonstration MCTS** : `python UCB_MCTS.py`
**Demonstration NMCS** : `python NMCS.py`
**Demonstration Expectimax** : `python expectimax.py`
**Demonstration NRPA** : `python NRPA.py`


## Mode Benchmark (Analyse de Performance)
Utilisez benchmark.py pour realiser les experiences (Benchmarks sauvegardes dans 'results').



### Exemples de commandes types

| Objectif | Commande |
| :--- | :--- |
| **Analyse FlatMC** | `python benchmark.py --method normal --games 10 --power 100 --rollout heuristique --prof 20 --max_moves 1000` |
| **Analyse MCTS** | `python benchmark.py --method MCTS --games 10 --power 300 --rollout heuristique --prof 20 --max_moves 1000` |
| **Analyse NMCS** | `python benchmark.py --method NMCS --games 10 --level 2 --power 5 --rollout heuristique --prof 20 --max_moves 1000` |
| **Analyse Expectimax** | `python benchmark.py --method expectimax --games 10 --prof 2` |
| **Analyse NRPA** | `python benchmark.py --method nrpa --games 10 --level 2` |



## Gestion des Résultats et Analyse

### Dossier `results/`
Ce dossier fait office de base de données pour l'historique des tests.Chaque exécution de `benchmark.py` génère un rapport textuel horodaté (ex: `results_20260331_134607_normal_heuristique_prof20.txt`).

Chaque fichier de log contient :
* **Configuration détaillée** : Méthode, puissance (`power`), type de rollout et limite de coups.
* **Performances Brutes** : Score moyen, meilleur score et tuile maximale atteinte.
* **Statistiques de Fiabilité** : L'écart-type permettant de mesurer la stabilité de l'IA sur plusieurs parties.
* **Métriques d'Efficacité** : Temps moyen par partie et ratio **Score/Temps**.

### 2. Notebook d'Analyse (`analyse.ipynb`)
Le projet inclut un Jupyter Notebook pour l'exploitation visuelle des données stockées dans le dossier `results/`.