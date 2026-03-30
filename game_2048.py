import random

class Fast2048:
    # Constantes pour les directions
    UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

    # Pré-calcul des indices du tableau 1D
    LINES = {
        UP:    [[0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15]],
        RIGHT: [[3, 2, 1, 0], [7, 6, 5, 4], [11, 10, 9, 8], [15, 14, 13, 12]],
        DOWN:  [[12, 8, 4, 0], [13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3]],
        LEFT:  [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    }

    def __init__(self):
        """Initialise une nouvelle partie (état réel)."""
        self.board = self.get_initial_board()
        self.score = 0

    def play_move(self, direction):
        """Applique un coup sur le jeu RÉEL et génère une nouvelle tuile."""
        next_board, gained_score = self.get_next_state(self.board, direction)
        if next_board is not None:
            self.board = self.add_random_tile(next_board)
            self.score += gained_score
            return True
        return False

    def is_game_over(self):
        """Vérifie si la partie actuelle est terminée."""
        return len(self.get_valid_moves(self.board)) == 0

    # ==========================================
    # MÉTHODES STATIQUES (Pour les simulations MCTS)
    # Ne modifient jamais self.board
    # ==========================================

    @staticmethod
    def get_initial_board():
        board = tuple(0 for _ in range(16))
        board = Fast2048.add_random_tile(board)
        return Fast2048.add_random_tile(board)

    @staticmethod
    def add_random_tile(board):
        empty_indices = [i for i, v in enumerate(board) if v == 0]
        if not empty_indices:
            return board
        
        idx = random.choice(empty_indices)
        val = 4 if random.random() < 0.1 else 2
        
        new_board = list(board)
        new_board[idx] = val
        return tuple(new_board)
    
    @staticmethod
    def count_tuiles(board):
        """
        Retourne le nombre de tuiles présentes sur le plateau (de 0 à 16).
        Moins il y a de tuiles, meilleur est le plateau.
        """
        # On compte les cases vides (0) et on soustrait à la taille totale (16)
        return 16 - board.count(0)
    
    @staticmethod
    def merge_line(line):
        non_zeros = [v for v in line if v != 0]
        new_line = []
        score = 0
        i = 0
        while i < len(non_zeros):
            if i + 1 < len(non_zeros) and non_zeros[i] == non_zeros[i+1]:
                new_line.append(non_zeros[i] * 2)
                score += non_zeros[i] * 2
                i += 2
            else:
                new_line.append(non_zeros[i])
                i += 1
        return new_line + [0] * (4 - len(new_line)), score

    @classmethod
    def get_next_state(cls, board, direction):
        """Simule un coup sans toucher au jeu actuel."""
        new_board = list(board)
        total_score = 0
        moved = False

        for line_indices in cls.LINES[direction]:
            line = [board[i] for i in line_indices]
            merged_line, score = cls.merge_line(line)
            
            if merged_line != line:
                moved = True
                total_score += score
                for idx, val in zip(line_indices, merged_line):
                    new_board[idx] = val

        if not moved:
            return None, 0
            
        return tuple(new_board), total_score

    @classmethod
    def get_valid_moves(cls, board):
        """Retourne les mouvements possibles pour un plateau donné."""
        valid_moves = []
        for direction in (cls.UP, cls.RIGHT, cls.DOWN, cls.LEFT):
            next_board, _ = cls.get_next_state(board, direction)
            if next_board is not None:
                valid_moves.append(direction)
        return valid_moves