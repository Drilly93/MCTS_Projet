import tkinter as tk

from game_2048 import Fast2048 

COLORS = {
    0: ("#cdc1b4", "#776e65"), 2: ("#eee4da", "#776e65"), 4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"), 16: ("#f59563", "#f9f6f2"), 32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"), 128: ("#edcf72", "#f9f6f2"), 256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"), 1024: ("#edc53f", "#f9f6f2"), 2048: ("#edc22e", "#f9f6f2"),
    4096: ("#3c3a32", "#f9f6f2"), 8192: ("#3c3a32", "#f9f6f2")
}

class GUI2048(tk.Tk):
    def __init__(self, ai_function=None, delay_ms=100):
        super().__init__()
        self.title("2048 - MCTS Engine")
        self.ai_function = ai_function
        self.delay_ms = delay_ms
        
        # Instanciation de notre nouvelle classe moteur
        self.game = Fast2048()
        
        self.grid_cells = []
        self.init_ui()
        self.update_ui()
        
        if self.ai_function is None:
            self.bind("<Key>", self.handle_keypress)
        else:
            self.after(self.delay_ms, self.ai_loop)

    def init_ui(self):
        background = tk.Frame(self, bg="#bbada0", width=400, height=400)
        background.grid()
        for i in range(4):
            row_cells = []
            for j in range(4):
                cell = tk.Frame(background, bg="#cdc1b4", width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                cell.grid_propagate(False) 
                
                label = tk.Label(master=cell, text="", bg="#cdc1b4", justify=tk.CENTER, font=("Helvetica", 24, "bold"))
                label.place(relx=0.5, rely=0.5, anchor="center")
                row_cells.append(label)
            self.grid_cells.append(row_cells)

    def update_ui(self):
        # On lit le tuple depuis l'objet self.game
        for i in range(4):
            for j in range(4):
                val = self.game.board[i * 4 + j]
                bg_color, fg_color = COLORS.get(val, COLORS[8192])
                self.grid_cells[i][j].configure(text=str(val) if val > 0 else "", bg=bg_color, fg=fg_color)
                self.grid_cells[i][j].master.configure(bg=bg_color)
        self.update_idletasks()

    def ai_loop(self):
        if self.game.is_game_over():
            print(f"Game Over ! Score final : {self.game.score}")
            return
            
        # L'IA reçoit une copie du plateau 
        best_move = self.ai_function(self.game.board)
        
        # On applique le coup au vrai jeu
        if self.game.play_move(best_move):
            self.update_ui()
            self.after(self.delay_ms, self.ai_loop)
        else:
            print("L'IA a renvoyé un coup invalide !")

    def handle_keypress(self, event):
        key_mapping = {'Up': Fast2048.UP, 'Right': Fast2048.RIGHT, 'Down': Fast2048.DOWN, 'Left': Fast2048.LEFT}
        if event.keysym in key_mapping:
            move = key_mapping[event.keysym]
            if self.game.play_move(move):
                self.update_ui()
                if self.game.is_game_over():
                    print(f"Game Over ! Score final : {self.game.score}")
if __name__ == "__main__":
    app = GUI2048()
    app.mainloop()