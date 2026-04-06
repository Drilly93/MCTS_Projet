import math
import random
from game_2048 import Fast2048
from utils import rollout_heuristique, evalutation_smart, rollout_brute, rollout_expert

def get_action_probabilities(state, valid_moves, policy):
    """Calcule les probabilités softmax des coups valides selon la politique."""
    weights = [policy.get((state, m), 0.0) for m in valid_moves]
    
    max_w = max(weights) if weights else 0.0
    exps = [math.exp(w - max_w) for w in weights]
    
    sum_exps = sum(exps)
    if sum_exps == 0:
        return [1.0 / len(valid_moves)] * len(valid_moves)
        
    return [e / sum_exps for e in exps]

def choose_move_softmax(state, valid_moves, policy):
    """Sélectionne un coup aléatoirement en respectant les probabilités de la politique."""
    probs = get_action_probabilities(state, valid_moves, policy)
    r = random.random()
    cumulative = 0.0
    for m, p in zip(valid_moves, probs):
        cumulative += p
        if r <= cumulative:
            return m
    return valid_moves[-1]

def rollout_nrpa(board, policy, profondeur_max=20):
    """
    Joue une simulation guidée par la politique.
    Retourne le score (utilisant l'heuristique de utils.py) et la séquence de coups.
    """
    sim_board = board
    coups_joues = 0
    sequence = []
    
    while coups_joues < profondeur_max:
        valid_moves = Fast2048.get_valid_moves(sim_board)
        if not valid_moves:
            break
            
        board_tuple = tuple(sim_board)
        move = choose_move_softmax(board_tuple, valid_moves, policy)
        sequence.append((board_tuple, move))
        
        sim_board, _ = Fast2048.get_next_state(sim_board, move)
        sim_board = Fast2048.add_random_tile(sim_board)
        coups_joues += 1
        
    score_final = rollout_brute(sim_board)
    return score_final, sequence

def adapt(policy, sequence, alpha=1.0):
    """
    Met à jour la politique (poids) en favorisant les coups de la meilleure séquence.
    """
    new_policy = policy.copy()
    for state, move in sequence:
        valid_moves = Fast2048.get_valid_moves(state)
        if not valid_moves:
            continue
            
        probs = get_action_probabilities(state, valid_moves, policy)
        
        for m, p in zip(valid_moves, probs):
            new_policy[(state, m)] = new_policy.get((state, m), 0.0) - alpha * p
            
        new_policy[(state, move)] = new_policy.get((state, move), 0.0) + alpha
        
    return new_policy

def nrpa_core(level, board, policy, iterations, profondeur_max):
    """Fonction récursive principale du NRPA."""
    if level == 0:
        return rollout_nrpa(board, policy, profondeur_max)
        
    best_score = float('-inf')
    best_seq = []
    
    for _ in range(iterations):
        score, seq = nrpa_core(level - 1, board, policy, iterations, profondeur_max)
        
        if score > best_score:
            best_score = score
            best_seq = seq
            
        if best_seq:
            policy = adapt(policy, best_seq)
            
    return best_score, best_seq

def nrpa_search(board, level=2, iterations=10, profondeur_max=20):
    """
    Fonction enveloppe appelée par l'interface ou le benchmark.
    """
    valid_moves = Fast2048.get_valid_moves(board)
    if not valid_moves:
        return None
    if len(valid_moves) == 1:
        return valid_moves[0]
        
    initial_policy = {}
    
    best_score, best_seq = nrpa_core(level, board, initial_policy, iterations, profondeur_max)
    
    if best_seq and len(best_seq) > 0:
        return best_seq[0][1]
        
    return random.choice(valid_moves)

if __name__ == "__main__":
    from interface_graphique import GUI2048
    
    print("Démarrage d'une partie complète avec l'IA NRPA...")
    NIVEAU = 3
    ITERATIONS = 10
    PROFONDEUR = 20
    fonction_ia = lambda board: nrpa_search(
        board, 
        level=NIVEAU, 
        iterations=ITERATIONS, 
        profondeur_max=PROFONDEUR
    )
    
    app = GUI2048(ai_function=fonction_ia, delay_ms=10)
    app.after(100, app.ai_loop) 
    app.mainloop()