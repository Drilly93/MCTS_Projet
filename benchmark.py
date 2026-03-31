import time
import argparse
import numpy as np
from game_2048 import Fast2048
from utils import rollout_brute, rollout_heuristique, rollout_expert
import datetime

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

    stats = {
        'moyenne': np.mean(scores),
        'std': np.std(scores),
        'best': np.max(scores),
        'max_tile': np.max(max_tiles),
        'avg_time': np.mean(durations)
    }

    return stats


def save_results(args, stats):
    """Enregistre les paramètres et les résultats dans un fichier texte."""
    # Création d'un nom de fichier unique basé sur la date et l'heure
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results_{timestamp}_{args.method}_{args.rollout}.txt"
    filename = f"results/{filename}"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("="*50 + "\n")
        f.write(f"BENCHMARK 2048 - {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("="*50 + "\n\n")
        
        # Section Arguments du Parser
        f.write("--- CONFIGURATION ---\n")
        f.write(f"Méthode utilisée : {args.method}\n")
        f.write(f"Type de Rollout  : {args.rollout}\n")
        f.write(f"Nombre de parties: {args.games}\n")
        f.write(f"Puissance (Iter) : {args.power}\n")
        f.write(f"Limite de coups  : {args.max_moves}\n\n")
        
        # Section Statistiques
        f.write("--- RÉSULTATS ---\n")
        f.write(f"Score Moyen      : {stats['moyenne']:.2f}\n")
        f.write(f"Écart-type       : {stats['std']:.2f}\n")
        f.write(f"Meilleur Score   : {stats['best']}\n")
        f.write(f"Tuile Max        : {stats['max_tile']}\n")
        f.write(f"Temps Moyen/Partie: {stats['avg_time']:.2f}s\n")
        f.write(f"Score/Temps      : {stats['moyenne']/stats['avg_time']:.2f}\n")
        f.write("\n" + "="*50 + "\n")
    
    print(f"\n[INFO] Résultats enregistrés dans : {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark d'IA pour 2048")
    
    # Choix de l'algorithme
    parser.add_argument("--method", type=str, required=True, 
                        choices=["normal", "MCTS", "NMCS"],
                        help="Algorithme : normal (Flat MC), MCTS, NMCS")
    
    # Choix du type de rollout
    parser.add_argument("--rollout", type=str, default="heuristique",
                        choices=["brute", "heuristique","expert"],
                        help="Type de simulation (brute ou heuristique)")
    
    parser.add_argument("--games", type=int, default=10, help="Nombre de parties")
    parser.add_argument("--power", type=int, default=100, help="Itérations ou simulations")
    parser.add_argument("--max_moves", type=int, default=1000, help="Limite de coups")
    parser.add_argument("--prof", type=int, default=20, help="Profondeur de la simulation")
    parser.add_argument("--level", type=int, default=2, help="Niveau pour NMCS (si applicable)")
    args = parser.parse_args()
    
    
    # Choix de la fonction de rollout
    if args.rollout == "brute":
        rollout_func = rollout_brute
    elif args.rollout == "heuristique":
        # On peut fixer la profondeur ici ou ajouter un argument au parser si besoin
        rollout_func = lambda b: rollout_heuristique(b, profondeur_max=args.prof)
        args.rollout += f"_prof{args.prof}"
    else:  # expert
        rollout_func = lambda b: rollout_expert(b, profondeur_max=args.prof)
        args.rollout += f"_prof{args.prof}"

        
    # Sélection de la fonction et injection des paramètres
    if args.method == "normal":
        from monte_carlo_classique import flat_monte_carlo
        ai_func = lambda board: flat_monte_carlo(board, simulations_per_move=args.power, rollout_method=rollout_func)
        method_name = f"Flat MC ({args.power} sim, rollout: {args.rollout})"
        
    elif args.method == "MCTS":
        from UCT_MCTS import mcts_ucb_search
        ai_func = lambda board: mcts_ucb_search(board, iterations=args.power, rollout_method=rollout_func)
        method_name = f"MCTS UCB ({args.power} iter, rollout: {args.rollout})"
        
    elif args.method == "NMCS":
        from NMCS import nmcs
        # Pour NMCS, le rollout est souvent intrinsèque au niveau, 
        # mais on peut passer l'argument si votre fonction le supporte
        ai_func = lambda board: nmcs(board, level=args.level, rollout_method=rollout_func,simulations_per_move=args.power)[0]
        method_name = f"NMCS (Niveau {args.level}, {args.power} sim, rollout: {args.rollout})"
        args.method += f"_{args.level}"
    results_stats = run_benchmark(ai_func, num_games=args.games, name=method_name, max_moves=args.max_moves)
    save_results(args, results_stats)