import math
import random
from game_2048 import Fast2048
from interface_graphique import GUI2048
import time
import numpy as np

class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move  # Le mouvement qui a mené à ce plateau
        self.children = {} # Dictionnaire {direction: MCTSNode}
        self.visits = 0
        self.score_sum = 0
        self.untried_moves = Fast2048.get_valid_moves(board)

    def ucb_value(self, exploration_constant=1000):
        """Calcule la valeur UCB1 du nœud."""
        if self.visits == 0:
            return float('inf')  # Priorité aux nœuds non visités
        
        exploitation = self.score_sum / self.visits
        exploration = exploration_constant * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + exploration

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def get_best_child(self, exploration_constant=1000):
        """Sélectionne l'enfant avec la meilleure valeur UCB."""
        return max(self.children.values(), key=lambda node: node.ucb_value(exploration_constant))

def mcts_ucb_search(root_board, iterations=100):
    root_node = MCTSNode(root_board)

    for _ in range(iterations):
        node = root_node
        
        # 1. SÉLECTION (Selection)
        # On descend dans l'arbre tant que les nœuds sont totalement explorés
        while node.is_fully_expanded() and node.children:
            node = node.get_best_child()

        # 2. EXPANSION (Expansion)
        # Si le nœud n'est pas terminal, on crée un nouvel enfant
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            node.untried_moves.remove(move)
            
            # Simuler le coup + ajout d'une tuile pour le nouvel état
            next_state, _ = Fast2048.get_next_state(node.board, move)
            if next_state:
                next_state = Fast2048.add_random_tile(next_state)
                child_node = MCTSNode(next_state, parent=node, move=move)
                node.children[move] = child_node
                node = child_node

        # 3. SIMULATION (Rollout)
        # On joue au hasard depuis cet état jusqu'à la fin
        rollout_board = node.board
        sim_score = 0
        while True:
            valid_moves = Fast2048.get_valid_moves(rollout_board)
            if not valid_moves:
                break
            move = random.choice(valid_moves)
            rollout_board, gained = Fast2048.get_next_state(rollout_board, move)
            rollout_board = Fast2048.add_random_tile(rollout_board)
            sim_score += gained

        # 4. RÉTROPROPAGATION (Backpropagation)
        # On remonte l'arbre pour mettre à jour les visites et scores
        while node is not None:
            node.visits += 1
            node.score_sum += sim_score
            node = node.parent

    # Choix final : le mouvement le plus visité depuis la racine
    if not root_node.children:
        valid = Fast2048.get_valid_moves(root_board)
        return random.choice(valid) if valid else None
        
    best_move = max(root_node.children.items(), key=lambda item: item[1].visits)[0]
    return best_move




if __name__ == "__main__":
    print("Démarrage de l'IA MCTS avec UCB...")
    app = GUI2048(ai_function=lambda board: mcts_ucb_search(board, iterations=50), delay_ms=10)
    app.mainloop()