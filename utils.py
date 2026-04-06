import random
import math
from game_2048 import Fast2048

def rollout_brute(board):
    """
    Simulation 'Brute' : joue au hasard jusqu'à la fin de la partie.
    Retourne le score cumulé des fusions réalisées.
    """
    sim_board = board
    score_cumule = 0
    
    while True:
        valid_moves = Fast2048.get_valid_moves(sim_board)
        
        if not valid_moves:
            return score_cumule # Retourne le score total de la simulation
            
        move = random.choice(valid_moves)
        sim_board, gained = Fast2048.get_next_state(sim_board, move)
        sim_board = Fast2048.add_random_tile(sim_board)
        
        score_cumule += gained



def rollout_heuristique(board, profondeur_max=20):
    """
    Simulation 'Heuristique' : s'arrête après X coups.
    Retourne une note basée sur la qualité du plateau (cases vides).
    """
    sim_board = board
    coups_joues = 0
    
    while coups_joues < profondeur_max:
        valid_moves = Fast2048.get_valid_moves(sim_board)
        
        if not valid_moves:
            return -1000 # Pénalité de mort si la grille est pleine
            
        move = random.choice(valid_moves)
        sim_board, _ = Fast2048.get_next_state(sim_board, move)
        sim_board = Fast2048.add_random_tile(sim_board)
        coups_joues += 1

    # Évaluation : nombre de cases vides (0)
    # Plus il y a d' vide, plus le coup est jugé bon
    cases_vides = list(sim_board).count(0)
    return cases_vides * 100


## --- OPTIONNEL ---
def rollout_expert(board, profondeur_max=15):
    """
    Simulation avancée : simule X coups puis évalue la structure du plateau.
    Combine survie, positionnement et organisation des tuiles.
    """
    sim_board = board
    coups_joues = 0
    
    #  Phase de projection (Future proche)
    while coups_joues < profondeur_max:
        valid_moves = Fast2048.get_valid_moves(sim_board)
        if not valid_moves:
            return -2000 # Pénalité de mort (plus forte que l'heuristique simple)
            
        move = random.choice(valid_moves)
        sim_board, _ = Fast2048.get_next_state(sim_board, move)
        sim_board = Fast2048.add_random_tile(sim_board)
        coups_joues += 1

    # 2. Analyse du plateau final
    score_final = 0
    
    # A. Bonus de cases vides (Fondamental pour la liberté de mouvement)
    empty_cells = list(sim_board).count(0)
    score_final += empty_cells * 150
    
    # B. Bonus de la plus grosse tuile (Récompense la progression)
    max_tile = max(sim_board)
    score_final += max_tile 

    # C. Bonus du Coin (Stratégie de haut niveau)
    # Les indices des coins sont 0, 3, 12, 15 pour une grille 4x4
    corners = [0, 3, 12, 15]
    if sim_board.index(max_tile) in corners:
        score_final += max_tile * 2 # On double la valeur si elle est bien placée
    else:
        score_final -= 500 # Malus si la grosse tuile se balade au milieu

    # D. Monotonie simplifiée (Bonus si les tuiles sont ordonnées)
    # On vérifie si les lignes et colonnes sont "fluides"
    monotony = 0
    for i in range(4):
        row = sim_board[i*4 : (i+1)*4]
        col = [sim_board[i + j*4] for j in range(4)]
        
        for line in [row, col]:
            for k in range(3):
                if line[k] >= line[k+1] and line[k] > 0:
                    monotony += 50 # Bonus d'ordre décroissant
                elif line[k] < line[k+1] and line[k+1] > 0:
                    monotony -= 50 # Malus de désordre

    score_final += monotony
    
    return score_final


def evalutation_smart(board):
    """Fonction d'évaluation heuristique très rapide, force à garder dans le coins en
    à droite la tuile avec la plus grande valeure puis par tuile decroissante comme un serpent."""

    WEIGHT_MATRIX = [
        32768, 16384, 8192, 4096,
        256,   512,   1024, 2048,
        128,   64,    32,   16,
        1,     2,     4,    8
    ]

    score = 0
    empty_cells = 0
    
    for i in range(16):
        val = board[i]
        if val == 0:
            empty_cells += 1
        else:
            score += val * WEIGHT_MATRIX[i]
    
    return score + (empty_cells * 100000)