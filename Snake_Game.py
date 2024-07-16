import tkinter as tk
import random
import time

# Constants
GRID_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
MOVE_INTERVAL = 200  # in milliseconds
BONUS_APPLE_TIME_LIMIT = 5  # Time limit for bonus apple appearance (in seconds)

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")

        self.canvas = tk.Canvas(master, width=GRID_WIDTH * GRID_SIZE, height=GRID_HEIGHT * GRID_SIZE, bg="black")
        self.canvas.pack()

        self.snake = [(0, 0)]
        self.direction = (0, 1)  # Initial direction: right
        self.arrow_keys = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}  # Arrow key directions
        self.apple = self.generate_apple()
        self.apple_id = None
        self.score = 0
        self.high_score = self.load_high_score()  # Load high score from file
        self.game_over = False
        self.bonus_apple = None
        self.bonus_apple_count=0
        self.bonus_apple_visible = False
        self.bonus_apple_timer = None

        self.draw_snake()
        self.draw_apple()
        self.draw_score()

        self.master.bind("<KeyPress>", self.on_key_press)

        self.move_snake()

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x1, y1 = segment[0] * GRID_SIZE, segment[1] * GRID_SIZE
            x2, y2 = x1 + GRID_SIZE, y1 + GRID_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white", tags="snake")

    def draw_apple(self):
        x1, y1 = self.apple[0] * GRID_SIZE, self.apple[1] * GRID_SIZE
        x2, y2 = x1 + GRID_SIZE, y1 + GRID_SIZE
        self.apple_id = self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="white", tags="apple")

    def draw_bonus_apple(self):
        self.bonus_apple = self.generate_apple()
        x1, y1 = self.bonus_apple[0] * GRID_SIZE, self.bonus_apple[1] * GRID_SIZE
        x2, y2 = x1 + GRID_SIZE, y1 + GRID_SIZE
        self.bonus_apple_id = self.canvas.create_oval(x1, y1, x2, y2, fill="green", outline="white", tags="bonus_apple")
        self.bonus_apple_visible = True
        self.bonus_apple_timer = self.master.after(BONUS_APPLE_TIME_LIMIT * 1000, self.remove_bonus_apple)

    def remove_bonus_apple(self):
        self.canvas.delete(self.bonus_apple_id)
        self.bonus_apple_visible = False
        self.bonus_apple_timer = None

    def generate_apple(self):
        while True:
            apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if apple not in self.snake:
                return apple

    def move_snake(self):
        if not self.game_over:
            self.check_collision()

            head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
            self.snake.insert(0, head)

            if head == self.apple:
                self.score += 1
                self.remove_apple()
                self.apple = self.generate_apple()
                self.draw_apple()
                self.draw_score()
                self.check_for_bonus_apple()

            elif head == self.bonus_apple:
                self.score += 3  # Bonus for eating the green apple
                self.remove_bonus_apple()
                self.draw_score()

            else:
                self.snake.pop()

            self.draw_snake()

            self.master.after(MOVE_INTERVAL, self.move_snake)

    def check_collision(self):
        head = self.snake[0]
        # Check wall collision
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            self.end_game()
        # Check self collision
        if head in self.snake[1:]:
            self.end_game()

    def end_game(self):
        self.game_over = True
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()  # Save high score to file
        self.canvas.create_text(GRID_WIDTH * GRID_SIZE // 2, GRID_HEIGHT * GRID_SIZE // 2,
                                text=f"Game Over! Score: {self.score}\nHigh Score: {self.high_score}\nPress Enter to play again.", fill="white", font=("Helvetica", 24, "bold"))

    def on_key_press(self, event):
        key = event.keysym
        if not self.game_over:
            if key in self.arrow_keys:
                new_direction = self.arrow_keys[key]
                # Ensure snake cannot reverse its current direction
                if (self.direction[0] + new_direction[0], self.direction[1] + new_direction[1]) != (0, 0):
                    self.direction = new_direction
        else:
            if key == "Return":
                self.start_new_game()

    def start_new_game(self):
        self.canvas.delete("all")
        self.bonus_apple_count=0
        self.snake = [(0, 0)]
        self.direction = (0, 1)
        self.apple = self.generate_apple()
        self.score = 0
        self.game_over = False
        self.bonus_apple_visible = False
        self.draw_snake()
        self.draw_apple()
        self.draw_score()
        self.move_snake()

    def remove_apple(self):
        self.canvas.delete(self.apple_id)

    def draw_score(self):
        self.canvas.delete("score")
        self.canvas.create_text(GRID_WIDTH * GRID_SIZE - 10, 10, text=f"Score: {self.score}", fill="white", anchor=tk.NE, font=("Helvetica", 12), tags="score")
        self.canvas.create_text(GRID_WIDTH * GRID_SIZE - 10, 30, text=f"High Score: {self.high_score}", fill="white", anchor=tk.NE, font=("Helvetica", 12), tags="score")

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))

    def check_for_bonus_apple(self):
        self.bonus_apple_count += 1
        if self.bonus_apple_count % 5 == 0:
            self.draw_bonus_apple()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
