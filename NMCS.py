import random
from game_2048 import Fast2048
from interface_graphique import GUI2048



def rollout_aleatoire(board, profondeur_max=10):
    """
    Joue des coups aléatoires jusqu'à la profondeur max.
    Renvoie le score basé sur les cases vides et les pénalités.
    """
    sim_board = board
    coups_joues = 0
    game_over_premature = False
    score_simulation = 0
    
    while coups_joues < profondeur_max:
        valid_moves = Fast2048.get_valid_moves(sim_board)
        
        if not valid_moves:
            score_simulation -= 1000 
            game_over_premature = True
            break 
            
        random_move = random.choice(valid_moves)
        sim_board, _ = Fast2048.get_next_state(sim_board, random_move)
        sim_board = Fast2048.add_random_tile(sim_board)
        coups_joues += 1

    if not game_over_premature:
        cases_vides = sim_board.count(0)
        score_simulation += (cases_vides * 10)
        
    return score_simulation




def nmcs(board, level, simulations_per_move=10):
    """
    Algorithme NMCS classique.
    Renvoie un tuple : (Meilleur_Coup, Meilleur_Score_Moyen)
    """
    valid_moves = Fast2048.get_valid_moves(board)
    
    # Condition d'arrêt si le plateau est mort
    if not valid_moves:
        return None, -1000

    best_move = valid_moves[0]
    best_avg_score = float('-inf')

    # On évalue chaque branche possible
    for move in valid_moves:
        total_score_branche = 0
        
        # On lance plusieurs simulations pour lisser le hasard de la nouvelle tuile
        for _ in range(simulations_per_move):
            # 1. On applique notre coup et on génère la tuile aléatoire
            sim_board, _ = Fast2048.get_next_state(board, move)
            sim_board = Fast2048.add_random_tile(sim_board)
            
            # 2. L'ÉVALUATION (La magie récursive est ici)
            if level == 0:
                # Si on est au niveau 0, on fait un simple rollout aléatoire
                score = rollout_aleatoire(sim_board)
            else:
                # Si on est au niveau > 0, on demande au niveau inférieur d'évaluer ce plateau !
                _, score = nmcs(sim_board, level - 1, simulations_per_move)
                
            total_score_branche += score
            
        # 3. Moyenne de la branche
        avg_score = total_score_branche / simulations_per_move
        
        # 4. Mise à jour du meilleur coup
        if avg_score > best_avg_score:
            best_avg_score = avg_score
            best_move = move

    return best_move, best_avg_score


def IA_NMCS_Level_1(board):
    """Lance un NMCS de niveau 1"""
    # Level 1 : Regarde 1 coup en avance avec l'arbre, puis fait 10 rollouts par branche.
    meilleur_coup, score = nmcs(board, level=1, simulations_per_move=15)
    return meilleur_coup
 
def IA_NMCS_Level_2(board):
    """Lance un NMCS de niveau 2"""
    meilleur_coup, score = nmcs(board, level=2, simulations_per_move=5)
    return meilleur_coup

if __name__ == "__main__":
    print("Démarrage de l'IA NMCS (Level 1)...")
    app = GUI2048(ai_function=IA_NMCS_Level_2, delay_ms=0)
    app.mainloop()