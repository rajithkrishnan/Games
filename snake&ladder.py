import tkinter as tk
from tkinter import ttk
import random

class SnakeAndLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladder Game")
        self.board_size = 10
        self.cell_size = 60
        self.canvas_size = self.board_size * self.cell_size
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        self.player_positions = [0, 0]  # Start positions for two players
        self.current_player = 0
        self.consecutive_sixes = [0, 0]  # Track consecutive 6s for both players
        self.game_won = False

        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 64: 60, 87: 24, 95: 75, 98: 78}
        self.ladders = {9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

        self.player_names = ["Player 1", "Player 2"]
        self.player_colors = ["red", "blue"]
        self.create_board()
        self.create_players()
        self.create_controls()
        self.setup_player_info()

    def setup_player_info(self):
        self.player_setup_window = tk.Toplevel(self.root)
        self.player_setup_window.title("Setup Players")

        self.player_name_vars = [tk.StringVar() for _ in range(2)]
        self.player_color_vars = [tk.StringVar() for _ in range(2)]
        color_options = ["blue", "yellow", "purple", "orange"]

        for i in range(2):
            tk.Label(self.player_setup_window, text=f"Player {i + 1} Name:").grid(row=i, column=0)
            tk.Entry(self.player_setup_window, textvariable=self.player_name_vars[i]).grid(row=i, column=1)

            tk.Label(self.player_setup_window, text="Color:").grid(row=i, column=2)
            color_dropdown = ttk.Combobox(self.player_setup_window, textvariable=self.player_color_vars[i], values=color_options)
            color_dropdown.grid(row=i, column=3)
            color_dropdown.current(i)  # Set default color

        tk.Button(self.player_setup_window, text="Start Game", command=self.start_game).grid(row=2, columnspan=4)

    def start_game(self):
        for i in range(2):
            self.player_names[i] = self.player_name_vars[i].get()
            self.player_colors[i] = self.player_color_vars[i].get()

        self.player_setup_window.destroy()
        self.create_players()

    def create_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "white" if (row + col) % 2 == 0 else "lightgray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        
        # Draw snakes and ladders
        for start, end in self.snakes.items():
            self.draw_arrow(start, end, "red")

        for start, end in self.ladders.items():
            self.draw_arrow(start, end, "green")

    def draw_arrow(self, start, end, color):
        start_x, start_y = self.get_coordinates(start)
        end_x, end_y = self.get_coordinates(end)
        self.canvas.create_line(start_x + self.cell_size // 2, start_y + self.cell_size // 2,
                                end_x + self.cell_size // 2, end_y + self.cell_size // 2,
                                arrow=tk.LAST, fill=color, width=2)

    def create_players(self):
        self.player_tokens = []
        for i, color in enumerate(self.player_colors):
            token = self.canvas.create_oval(-self.cell_size, -self.cell_size, 0, 0, fill=color)
            self.player_tokens.append(token)

    def create_controls(self):
        self.roll_button = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=20)
        self.info_label = tk.Label(self.root, text=f"{self.player_names[0]}'s turn to roll.")
        self.info_label.pack()
        self.dice_label = tk.Label(self.root, text="Dice: ")
        self.dice_label.pack()

    def roll_dice(self):
        if self.game_won:
            return
        dice_roll = random.randint(1, 6)
        self.dice_label.config(text=f"Dice: {dice_roll}")
        self.info_label.config(text=f"{self.player_names[self.current_player]} rolled a {dice_roll}")

        if self.player_positions[self.current_player] == 0 and dice_roll != 6:
            self.info_label.config(text=f"{self.player_names[self.current_player]} needs a 6 to start. Rolled a {dice_roll}.")
            self.switch_player()
            return

        if dice_roll == 6:
            self.consecutive_sixes[self.current_player] += 1
            if self.consecutive_sixes[self.current_player] == 3:
                self.info_label.config(text=f"{self.player_names[self.current_player]} rolled three consecutive 6s and skips their turn.")
                self.consecutive_sixes[self.current_player] = 0
                self.switch_player()
                return
        else:
            self.consecutive_sixes[self.current_player] = 0

        self.move_player(dice_roll)
        self.update_player_position()

        if self.player_positions[self.current_player] == 100:
            self.info_label.config(text=f"{self.player_names[self.current_player]} wins!")
            self.game_won = True
        elif dice_roll != 6:
            self.switch_player()
        else:
            self.info_label.config(text=f"{self.player_names[self.current_player]} rolled a 6 and gets another turn!")

    def move_player(self, steps):
        pos = self.player_positions[self.current_player]
        for _ in range(steps):
            if pos < 100:
                pos += 1
                self.update_player_position(pos)
                self.root.update()
                self.root.after(200)  # Delay for visual movement effect

        pos = self.check_snakes_and_ladders(pos)
        self.player_positions[self.current_player] = pos

    def check_snakes_and_ladders(self, position):
        if position in self.snakes:
            return self.snakes[position]
        elif position in self.ladders:
            return self.ladders[position]
        return position

    def update_player_position(self, position=None):
        if position is None:
            position = self.player_positions[self.current_player]
        x, y = self.get_coordinates(position)
        self.canvas.coords(self.player_tokens[self.current_player], x, y, x + self.cell_size, y + self.cell_size)

    def get_coordinates(self, pos):
        row = (pos - 1) // self.board_size
        col = (pos - 1) % self.board_size
        if row % 2 == 0:
            x = col * self.cell_size
        else:
            x = (self.board_size - 1 - col) * self.cell_size
        y = (self.board_size - 1 - row) * self.cell_size
        return x, y

    def switch_player(self):
        self.current_player = (self.current_player + 1) % 2
        self.info_label.config(text=f"{self.player_names[self.current_player]}'s turn to roll.")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeAndLadderGame(root)
    root.mainloop()
