from utils import randcell
import os 

class Helicopter:
    def __init__(self, w, h):
        rc = randcell(w, h)
        self.x = rc[0]  # Строка
        self.y = rc[1]  # Столбец
        self.w = w
        self.h = h
        self.tank = 0
        self.mxtank = 1
        self.score = 0
        self.lives = 20

    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < self.h and 0 <= ny < self.w:
            self.x, self.y = nx, ny

    def print_stats(self):
        stats = f"🧺 {self.tank}/{self.mxtank} | 🏆 {self.score} | 💛 {self.lives}"
        print(stats)

    def game_over(self):
        os.system("cls" if os.name == 'nt' else 'clear')
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("X                                 X")
        print(f"X GAME OVER, YOUR SCORE IS {self.score}  X")
        print("X                                 X")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        exit(0)

    def export_data(self):
        return {
            "x": self.x,
            "y": self.y,
            "tank": self.tank,
            "mxtank": self.mxtank,
            "score": self.score,
            "lives": self.lives
        }
    
    def import_data(self, data):
        self.x = data.get("x", 0)
        self.y = data.get("y", 0)
        self.tank = data.get("tank", 0)
        self.mxtank = data.get("mxtank", 1)
        self.score = data.get("score", 0)
        self.lives = data.get("lives", 20)