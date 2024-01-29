import tkinter as tk
from tkinter import PhotoImage
import numpy as np
import threading
import time
import random
from PIL import Image, ImageTk

# Constants
INITIAL_POPULATION = 0.2
SIZE_W = 200
SIZE_H = 200
CELL_SIZE = 2  # I assume square cells

class Game(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game of Life")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.bind("<Escape>", self.quit)

        self.canvas = tk.Canvas(self.root, width=SIZE_W * CELL_SIZE, height=SIZE_H * CELL_SIZE, bg="white")
        self.canvas.pack()

        self.grid = np.random.choice([0, 1], size=(SIZE_H, SIZE_W), p=[1-INITIAL_POPULATION, INITIAL_POPULATION])
        self.next_grid = np.zeros((SIZE_H, SIZE_W), dtype=int)

        self.lock = threading.Lock()
        self.running = True
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

        self.root.mainloop()

    def draw_grid(self):
        image = Image.new("RGB", (SIZE_W * CELL_SIZE, SIZE_H * CELL_SIZE), "white")
        pixels = image.load()

        for i in range(SIZE_H):
            for j in range(SIZE_W):
                if self.grid[i, j] == 1:
                    for x in range(CELL_SIZE):
                        for y in range(CELL_SIZE):
                            pixels[j * CELL_SIZE + x, i * CELL_SIZE + y] = (0, 0, 0)  # Fill cell with black

        self.photo_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)

    def update_loop(self):
        while self.running:
            self.update_grid()
            self.draw_grid()
            time.sleep(0.1)  # simulation speed 

    def update_grid(self):
        # added NumPy for efficient grid updates
        for i in range(SIZE_H):
            for j in range(SIZE_W):
                self.next_grid[i, j] = self.next_state(i, j)
        self.grid, self.next_grid = self.next_grid.copy(), self.grid

    def next_state(self, i, j):
        # Calculate the next state for cell (i, j) based on the Game of Life rules
        neighbors = np.sum(self.grid[max(i-1,0):min(i+2,SIZE_H), max(j-1,0):min(j+2,SIZE_W)]) - self.grid[i, j]
        return 1 if neighbors == 3 or (self.grid[i, j] == 1 and neighbors == 2) else 0

    def quit(self, any=None):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    Game()
