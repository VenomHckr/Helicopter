from utils import randbool
from utils import randcell
from random import randint as rand

CELL_TYPES = "🟩🌲🌊🏥💒🔥"
TREE_BONUS = 100
UPGRADE_COST = 5000
LIFE_COST = 10000

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generate_forest(3, 10)  
        self.generate_river(15)
        self.generate_river(15)
        self.generate_river(15)
        self.generate_upgrade_shop()
        self.generate_hospital()
        

    def check_bounds(self, x, y):
        return 0 <= x < self.h and 0 <= y < self.w
  # рисуем карту  
    def print_map(self, helico, clouds):
        print("⬛" * (self.w + 2))
        for ri in range(self.h):
            print ("⬛" , end = "")
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if(helico.x == ri and helico.y == ci):
                    print ("🚁", end ="")
                elif self.cells[ri][ci] == 5:
                    print("🔥", end="")
                elif (clouds.cells[ri][ci] == 1):
                    print("⚪", end="")
                elif (clouds.cells[ri][ci] == 2):
                    print("🔴", end = "")    
                elif (cell >= 0 and cell < len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end="")
            print("⬛") 
        print("⬛" * (self.w + 2))                     
   # это речка 
    def generate_river(self, river_length):
        print(f"Начало генерации реки длиной {river_length}")
        rx, ry = randcell(self.w, self.h)
        self.cells[rx][ry] = 2
        count = 1
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
        direction_idx = rand(0, 3)
        dx, dy = directions[direction_idx]
        while count < river_length:
            nx, ny = rx + dx, ry + dy
            if self.check_bounds(nx, ny) and self.cells[nx][ny] != 2:
                self.cells[nx][ny] = 2
                rx, ry = nx, ny
                count += 1
            else:
                direction_idx = (direction_idx + 1) % 4  
                dx, dy = directions[direction_idx]
   # лес   
    def generate_forest(self, r, mxr): 
        for ri in range(self.h):
            for ci in range(self.w):
                if randbool(r, mxr):
                    self.cells[ri][ci] = 1
   
    def generate_tree(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if (self.cells[cx][cy] == 0):
            self.cells[cx] [cy] = 1
   # магазин 
    def generate_upgrade_shop(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] = 4
   # больница            
    def generate_hospital(self):
        attempts = 0
        while attempts < 100:
            c = randcell(self.w, self.h)    
            cx, cy = c[0], c[1]
            if self.cells[cx][cy] != 4:
                self.cells[cx][cy] = 3
                return
            attempts += 1
        for i in range(self.h):
            for j in range(self.w):
                if self.cells[i][j] != 4:
                    self.cells[i][j] = 3
                    return
        print("Не удалось разместить госпиталь!")

    # пожар        
    def add_fire(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells [cx][cy] == 1:
            self.cells [cx] [cy] = 5
    
    def update_fires(self):
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == 5:
                    self.cells[ri][ci] = 0
        for i in range(15):
            self.add_fire()
            
   #  количество активных пожаров 
    def count_active_fires(self):
        count = 0
        for ri in range(self.h):
            for ci in range(self.w):
                if self.cells[ri][ci] == 5:  
                    count += 1
        return count

    #  состояние вертолета
    def process_helicopter(self, helico, clouds):
        c = self.cells[helico.x][helico.y]
        d = clouds.cells[helico.x][helico.y]
        if (c == 2):
            helico.tank = helico.mxtank
        if (c == 5 and helico.tank > 0):
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.x] [helico.y] = 1
        if (c == 4 and helico.score >= UPGRADE_COST):
            helico.mxtank += 1
            helico.score -= UPGRADE_COST
        if (c == 3 and helico.score >= LIFE_COST):
            helico.lives += 10
            helico.score -= LIFE_COST
        if (d == 2):
            helico.lives -= 1
            if (helico.lives == 0):
                helico.game_over()

    def export_data(self):
        return {"cells": self.cells}

    def import_data(self, data):
        self.cells = data.get("cells", [[0 for i in range(self.w)] for j in range(self.h)])
