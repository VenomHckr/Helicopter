from utils import randbool

class Clouds:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]

    def update(self, r=1, mxr=10, g=1, mxg=10):
        for i in range(self.h):
            for j in range(self.w):
                if randbool(r, mxr):
                    self.cells[i][j] = 2 if randbool(g, mxg) else 1
                else:
                    self.cells[i][j] = 0

    def export_data(self):
        return {"cells": self.cells}
    
    def import_data(self, data):
        try:
            self.cells = data.get("cells", [[0 for i in range(self.w)] for j in range(self.h)])
        except:
            self.cells = [[0 for i in range(self.w)] for j in range(self.h)]