import time
import argparse
import numpy as np
from game_2048 import Fast2048

# Importez ici vos différentes méthodes
from monte_carlo_classique import flat_monte_carlo
from UCT_MCTS import mcts_ucb_search
#from nmcs_2048 import nmcs_search 

def run_benchmark(ai_function, num_games=10, name="Méthode Inconnue", max_moves=500):
    scores = []
    max_tiles = []
    durations = []

    print(f"\n--- Benchmark : {name} (Limite: {max_moves} coups/partie) ---")

    for i in range(num_games):
        start_time = time.time()
        game = Fast2048()
        move_count = 0 # Initialisation du compteur
        
        # On ajoute la condition move_count < max_moves
        while not game.is_game_over() and move_count < max_moves:
            move = ai_function(game.board)
            
            if move is not None:
                game.play_move(move)
                move_count += 1 # Incrémentation
            else:
                break
        
        end_time = time.time()
        score = game.score
        max_tile = max(game.board)
        duration = end_time - start_time
        
        scores.append(score)
        max_tiles.append(max_tile)
        durations.append(duration)
        
        status = "Terminé" if game.is_game_over() else f"Stoppé à {max_moves} coups"
        print(f"Partie {i+1}/{num_games} | {status} | Score: {game.score} | Tuile Max: {max(game.board)}")
        
    # Statistiques
    print("\n" + "="*40)
    print(f"RÉSULTATS FINAUX : {name}")
    print("="*40)
    print(f"Nombre de parties     : {num_games}")
    print(f"Moyenne des scores    : {np.mean(scores):.2f}")
    print(f"Variance des scores   : {np.var(scores):.2f}")
    print(f"Écart-type            : {np.std(scores):.2f}")
    print(f"Meilleur score        : {np.max(scores)}")
    print(f"Pire score            : {np.min(scores)}")
    print(f"Tuile max atteinte    : {max(max_tiles)}")
    print(f"Temps moyen / partie  : {np.mean(durations):.2f}s")
    print("="*40 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark d'IA pour 2048")
    
    # Argument pour le nom de la méthode
    parser.add_argument("--method", type=str, required=True, 
                        choices=["normal", "MCTS", "NMCS"],
                        help="L'algorithme à tester (normal, MCTS, NMCS)")
    
    # Argument pour le nombre de parties
    parser.add_argument("--games", type=int, default=10, 
                        help="Nombre de parties à simuler (défaut: 10)")

    # Argument pour la puissance de calcul (itérations)
    parser.add_argument("--power", type=int, default=100, 
                        help="Nombre d'itérations ou simulations par coup (défaut: 100)")

    parser.add_argument("--max_moves", type=int, default=1000, 
                        help="Limite de coups par partie (défaut: 1000)")
    args = parser.parse_args()
    
    # Sélection de la fonction correspondante
    if args.method == "normal":
        # Remplacez par votre fonction Flat Monte Carlo
        from monte_carlo_classique import flat_monte_carlo
        ai_func = lambda board: flat_monte_carlo(board, simulations_per_move=args.power)
        method_name = f"Flat Monte Carlo ({args.power} sim)"
        
    elif args.method == "MCTS":
        # Remplacez par votre fonction MCTS UCB
        from UCT_MCTS import mcts_ucb_search
        ai_func = lambda board: mcts_ucb_search(board, iterations=args.power)
        method_name = f"MCTS UCB ({args.power} iter)"
        
    elif args.method == "NMCS":
        # Remplacez par votre fonction Nested Monte Carlo
        # Note : ici power pourrait correspondre au niveau (1, 2 ou 3)
        from nmcs_2048 import nmcs_search
        ai_func = lambda board: nmcs_search(board, level=args.power)
        method_name = f"NMCS (Niveau {args.power})"

    # Lancement du test
    run_benchmark(ai_func, num_games=args.games, name=method_name, max_moves=args.max_moves)