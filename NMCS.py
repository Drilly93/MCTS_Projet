import random
from game_2048 import Fast2048
from interface_graphique import GUI2048
from utils import rollout_brute, rollout_heuristique

# Dictionnaire global pour stocker les résultats déjà calculés
nmcs_cache = {} # Clé : (board_tuple, level) -> Valeur : (best_move, best_avg_score)

def nmcs(board, level, simulations_per_move=10, rollout_method=rollout_brute):
    # Transformation du board en tuple pour qu'il soit "hashable" (utilisable comme clé de cache)
    board_tuple = tuple(board)
    state_key = (board_tuple, level)
    
    # 1. OPTIMISATION : CACHE (Mémorisation)
    if state_key in nmcs_cache:
        return nmcs_cache[state_key]

    valid_moves = Fast2048.get_valid_moves(board)
    if not valid_moves:
        return None, -1000

    best_move = valid_moves[0]
    best_avg_score = float('-inf')

    for move in valid_moves:
        total_score_branche = 0
        
        # 2. OPTIMISATION : RÉDUCTION DES SIMULATIONS
        # On fait moins de simulations en profondeur pour gagner un temps fou
        current_sims = simulations_per_move if level > 1 else max(1, simulations_per_move // 2)
        
        for i in range(current_sims):
            sim_board, _ = Fast2048.get_next_state(board, move)
            if sim_board is None: continue
            sim_board = Fast2048.add_random_tile(sim_board)
            
            if level == 0:
                score = rollout_method(sim_board)
            else:
                _, score = nmcs(sim_board, level - 1, simulations_per_move, rollout_method)
            
            total_score_branche += score

            # 3. OPTIMISATION : ÉLAGAGE (Pruning)
            # Si après quelques sims le score est déjà catastrophique, on arrête cette branche
            if i > 1 and (total_score_branche / (i+1)) < (best_avg_score * 0.7):
                break
            
        avg_score = total_score_branche / current_sims
        
        if avg_score > best_avg_score:
            best_avg_score = avg_score
            best_move = move

    # Sauvegarde dans le cache avant de renvoyer
    nmcs_cache[state_key] = (best_move, best_avg_score)
    
    # # Limite la taille du cache pour éviter de saturer la RAM (optionnel)
    # if len(nmcs_cache) > 10000:
    #     nmcs_cache.clear()

    return best_move, best_avg_score

if __name__ == "__main__":
    # Nettoyage du cache au début
    nmcs_cache.clear()
    
    print("Démarrage de l'IA NMCS Optimisée (Level 2)...")
    
    # Heuristique courte pour le niveau 0
    r_func = lambda b: rollout_heuristique(b, profondeur_max=15)
    
    # Note : simulations_per_move=3 est un bon compromis pour du Level 2 fluide
    app = GUI2048(
        ai_function=lambda board: nmcs(board, level=2, simulations_per_move=4, rollout_method=r_func)[0], 
        delay_ms=0
    )
    app.mainloop()