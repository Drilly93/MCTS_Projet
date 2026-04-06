import time
from game_2048 import Fast2048
from utils import evalutation_smart


def expectimax(state, depth, is_player):
    """Fonction récursive de l'arbre Expectimax."""
    if depth == 0:
        return evalutation_smart(state)
        
    if is_player:
        valid_moves = Fast2048.get_valid_moves(state)
        if not valid_moves:
            return evalutation_smart(state)
            
        max_score = float('-inf')
        for move in valid_moves:
            next_state, _ = Fast2048.get_next_state(state, move)
            score = expectimax(next_state, depth, False)
            if score > max_score:
                max_score = score
        return max_score
        
    else:
        empty_indices = [i for i, val in enumerate(state) if val == 0]
        if not empty_indices:
            return evalutation_smart(state)
            
        expected_score = 0
        prob_empty = 1.0 / len(empty_indices)
        
        for idx in empty_indices:
            state_list = list(state)
            
            # L'environnement a 90% de chance d'ajouter un 2
            state_list[idx] = 2
            expected_score += 0.9 * prob_empty * expectimax(tuple(state_list), depth - 1, True)
            
            # L'environnement a 10% de chance d'ajouter un 4
            state_list[idx] = 4
            expected_score += 0.1 * prob_empty * expectimax(tuple(state_list), depth - 1, True)
            
        return expected_score

def expectimax_search(board, depth=3):
    """
    Fonction enveloppe pour lancer la recherche Expectimax.
    """
    valid_moves = Fast2048.get_valid_moves(board)
    if not valid_moves:
        return None
    if len(valid_moves) == 1:
        return valid_moves[0]
        
    best_move = valid_moves[0]
    best_score = float('-inf')
    
    for move in valid_moves:
        next_state, _ = Fast2048.get_next_state(board, move)
        # On évalue ce coup en simulant le tour de l'environnement
        score = expectimax(next_state, depth, False)
        
        if score > best_score:
            best_score = score
            best_move = move
            
    return best_move

if __name__ == "__main__":
    from interface_graphique import GUI2048
    
    print("Démarrage d'une partie avec l'IA Expectimax (Profondeur 3)...")
    
    # Profondeur 3 est un bon compromis vitesse/intelligence
    PROFONDEUR = 3 
    
    fonction_ia = lambda board: expectimax_search(board, depth=PROFONDEUR)
    
    app = GUI2048(ai_function=fonction_ia, delay_ms=0)
    app.after(100, app.ai_loop)
    app.mainloop()