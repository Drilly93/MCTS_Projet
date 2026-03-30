from game_2048 import Fast2048
from interface_graphique import GUI2048
import random 



def flat_monte_carlo(board, simulations_per_move=40):
    """
    Évalue chaque coup possible en simulant des parties aléatoires jusqu'à la fin.
    Retourne la direction (0, 1, 2, 3) qui donne le meilleur score moyen.
    """
    valid_moves = Fast2048.get_valid_moves(board)
    if not valid_moves:
        return None

    best_move = None
    best_avg_score = -1

    # On teste chaque direction possible
    for move in valid_moves:
        total_score = 0
        
        # On lance N simulations pour cette direction
        for _ in range(simulations_per_move):
            # 1. On applique le coup évalué depuis le vrai plateau
            sim_board, gained_score = Fast2048.get_next_state(board, move)
            sim_board = Fast2048.add_random_tile(sim_board)
            sim_score = gained_score
            
            # 2. Phase de "Rollout" : on joue au hasard jusqu'au Game Over
            while True:
                sim_valid_moves = Fast2048.get_valid_moves(sim_board)
                if not sim_valid_moves:
                    break # Fin de la partie simulée
                
                random_move = random.choice(sim_valid_moves)
                sim_board, step_score = Fast2048.get_next_state(sim_board, random_move)
                sim_board = Fast2048.add_random_tile(sim_board)
                sim_score += step_score
                
            total_score += sim_score
            
        # 3. Calcul de la moyenne pour ce coup
        avg_score = total_score / simulations_per_move
        
        # 4. Mise à jour du meilleur coup
        if avg_score > best_avg_score:
            best_avg_score = avg_score
            best_move = move
            
    return best_move


def flat_monte_carlo_compte_tuile(board, simulations_per_move=40):
    """
    Évalue chaque coup possible en simulant des parties aléatoires jusqu'à la fin.
    Retourne la direction (0, 1, 2, 3) qui donne le meilleur score moyen.
    compte les tuiles pour déterminer le score 
    """
    valid_moves = Fast2048.get_valid_moves(board)
    if not valid_moves:
        return None

    best_move = None
    best_avg_score = -100000000000

    # On teste chaque direction possible
    for move in valid_moves:
        total_score = 0
        
        # On lance N simulations pour cette direction
        for _ in range(simulations_per_move):
            # 1. On applique le coup évalué depuis le vrai plateau
            sim_board, gained_score = Fast2048.get_next_state(board, move)
            sim_board = Fast2048.add_random_tile(sim_board)
            
            
            # 2. Phase de "Rollout" : Profondeur limitée + Pénalité de mort
            profondeur_max = 40
            coups_joues = 0
            game_over_premature = False
            
            while coups_joues < profondeur_max:
                sim_valid_moves = Fast2048.get_valid_moves(sim_board)
                
                if not sim_valid_moves:

                    total_score -= 1000 
                    game_over_premature = True
                    break 
                
                random_move = random.choice(sim_valid_moves)
                sim_board, _ = Fast2048.get_next_state(sim_board, random_move)
                sim_board = Fast2048.add_random_tile(sim_board)
                
                coups_joues += 1

            if not game_over_premature:
                cases_vides = sim_board.count(0)
                total_score += (cases_vides * 10)

        # 3. Calcul de la moyenne pour ce coup
        avg_score = total_score / simulations_per_move
        
        # 4. Mise à jour du meilleur coup
        if avg_score > best_avg_score:
            best_avg_score = avg_score
            best_move = move
            
    return best_move




if __name__ == "__main__":
    print("Démarrage de l'IA Monte Carlo...")
    
    # On passe notre algorithme à l'interface graphique.
    # Un délai de 10ms permet de voir les coups s'enchaîner rapidement.
    app = GUI2048(ai_function=lambda board: flat_monte_carlo_compte_tuile(board, simulations_per_move=5), delay_ms=10)
    app.mainloop()