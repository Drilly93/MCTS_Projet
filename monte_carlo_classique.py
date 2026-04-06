from game_2048 import Fast2048
from interface_graphique import GUI2048
from utils import rollout_brute, rollout_heuristique
import random 



def flat_monte_carlo(board, simulations_per_move=40, rollout_method=rollout_brute):
    valid_moves = Fast2048.get_valid_moves(board)
    if not valid_moves:
        return None

    best_move = None
    best_avg_score = -float('inf')

    for move in valid_moves:
        total_score = 0
        
        for _ in range(simulations_per_move):
            # Premier coup forcé
            sim_board, first_gain = Fast2048.get_next_state(board, move)
            if sim_board is None: continue
            sim_board = Fast2048.add_random_tile(sim_board)
            
            res = rollout_method(sim_board)
            total_score += res
            
        avg_score = total_score / simulations_per_move
        
        if avg_score > best_avg_score:
            best_avg_score = avg_score
            best_move = move
            
    return best_move


if __name__ == "__main__":
    print("Démarrage de l'IA Monte Carlo...")
    r_func = lambda b: rollout_heuristique(b, profondeur_max=50)
    app = GUI2048(ai_function=lambda board: flat_monte_carlo(board, rollout_method=r_func,simulations_per_move=30), delay_ms=0)
    
    app.mainloop()