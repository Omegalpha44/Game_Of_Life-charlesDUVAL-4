import tkinter as tk 
import random
import time
import ctypes
'''
Game of Life game using tkinter for its display.
required : tkinter and python3
'''

# Get the screen size
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# constants. Change it to define the default parameters of the game
SIZE_W = int(screen_width / 20) * 10 # wideness of the grid 
SIZE_H = int(screen_height / 20) * 10# height of the grid
nb_cells = 30
W_CELLS = int(SIZE_W // nb_cells) # width of a cell
H_CELLS = int(SIZE_H // nb_cells) # height of a cell
INITIAL_POPULATION = 0.1 # initial population of the grid


# Game class

class Game(object):
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Game of Life")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.bind("<Escape>", self.quit)

        self.canvas = tk.Canvas(self.root, width=SIZE_W, height=SIZE_H, bg="white")
        self.canvas.pack()

        self.grid = [[0 for _ in range(SIZE_W)] for _ in range(SIZE_H)]
        self.next_grid = [[0 for _ in range(SIZE_W)] for _ in range(SIZE_H)]
        
        self.init_grid()
        self.draw_grid()
    
    def init_grid(self):
        for i in range(SIZE_H):
            for j in range(SIZE_W):
                if random.random() < INITIAL_POPULATION:
                    self.grid[i][j] = 1
                else:
                    self.grid[i][j] = 0
    
    def draw_grid(self):
        # cleanse the board
        self.canvas.delete("all")
        # draw the grid
        for i in range(SIZE_H):
            for j in range(SIZE_W):
                if self.grid[i][j] == 1:
                    self.canvas.create_rectangle(j*W_CELLS, i*H_CELLS, j*W_CELLS+W_CELLS, i*H_CELLS+H_CELLS, fill="black")
                else:
                    self.canvas.create_rectangle(j*W_CELLS, i*H_CELLS, j*W_CELLS+W_CELLS, i*H_CELLS+H_CELLS, fill="white")
        self.canvas.update()

    def update(self):
        """update the grid"""
        for i in range(SIZE_H):
            for j in range(SIZE_W):
                self.next_grid[i][j] = self.next_state(i, j) 
        self.grid = self.next_grid

    def next_state(self, i, j):
        """return the next state of the cell at position (i, j)"""
        nb_neighbors = self.count_neighbors(i, j)
        if self.grid[i][j] == 1:
            if nb_neighbors == 2 or nb_neighbors == 3:
                return 1
            else:
                return 0
        else:
            if nb_neighbors == 3:
                return 1
            else:
                return 0

    def count_neighbors(self, i, j):
        """return the number of neighbors of the cell at position (i, j)"""
        nb_neighbors = 0
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if (di != 0 or dj != 0) and self.grid[(i+di)%SIZE_H][(j+dj)%SIZE_W] == 1:
                    nb_neighbors += 1
        return nb_neighbors

    def quit(self, any=None):
        self.root.destroy()



if __name__ == "__main__":
    game = Game()
    while True:
        game.update()
        game.draw_grid()