# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:27:04 2024

@author: mohit
"""

import pygame
import random
import tkinter as tk
from tkinter import font as tkFont

# Constants for Pygame
TILE_SIZE = 20
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MAZE_ROWS = WINDOW_HEIGHT // TILE_SIZE
MAZE_COLS = WINDOW_WIDTH // TILE_SIZE

class Maze:
    def init(self):
        self.grid = [[1 for _ in range(MAZE_COLS)] for _ in range(MAZE_ROWS)]
        self.generate_maze(0, 0)
        self.end_x, self.end_y = MAZE_COLS - 2, MAZE_ROWS - 2

    def generate_maze(self, x, y):
        self.grid[y][x] = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = x + dx * 2, y + dy * 2
            if 0 <= new_x < MAZE_COLS and 0 <= new_y < MAZE_ROWS and self.grid[new_y][new_x] == 1:
                self.grid[y + dy][x + dx] = 0
                self.generate_maze(new_x, new_y)

    def draw(self, window):
        for row in range(MAZE_ROWS):
            for col in range(MAZE_COLS):
                color = (255, 0, 0) if (row, col) == (self.end_y, self.end_x) else ((255, 255, 255) if self.grid[row][col] == 1 else (0, 0, 0))
                pygame.draw.rect(window, color, pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def is_walkable(self, x, y):
        return self.grid[y][x] == 0

class Player:
    def init(self, start_x, start_y):
        self.pos_x = start_x
        self.pos_y = start_y

    def move(self, delta_x, delta_y, maze):
        new_x, new_y = self.pos_x + delta_x, self.pos_y + delta_y
        if 0 <= new_x < MAZE_COLS and 0 <= new_y < MAZE_ROWS and maze.is_walkable(new_x, new_y):
            self.pos_x = new_x
            self.pos_y = new_y

    def draw(self, window):
        pygame.draw.rect(window, (0, 255, 0), pygame.Rect(self.pos_x * TILE_SIZE, self.pos_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def show_winner():
    winner_window = tk.Tk()
    winner_window.title("You Win!")
    winner_window.geometry("400x300")
    winner_window.configure(bg="#ffcc66")

    title_font = tkFont.Font(family="Helvetica", size=24, weight="bold")
    title_label = tk.Label(winner_window, text="Congratulations!", font=title_font, fg="#3333cc", bg="#ffcc66")
    title_label.pack(pady=20)

    subtitle_font = tkFont.Font(family="Helvetica", size=16)
    subtitle_label = tk.Label(winner_window, text="You completed the maze!", font=subtitle_font, fg="#555555", bg="#ffcc66")
    subtitle_label.pack(pady=10)

    def play_again():
        winner_window.destroy()
        main_game()  # Restart the game

    def quit_game():
        winner_window.destroy()

    play_again_button = tk.Button(winner_window, text="Play Again", command=play_again, font=subtitle_font, bg="#3399ff", fg="white", padx=10, pady=5)
    play_again_button.pack(pady=10)

    quit_button = tk.Button(winner_window, text="Quit", command=quit_game, font=subtitle_font, bg="#cc3333", fg="white", padx=10, pady=5)
    quit_button.pack(pady=10)

    winner_window.mainloop()

def main_game():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Maze Adventure Game")

    maze = Maze()
    player = Player(1, 1)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(0, -1, maze)
        if keys[pygame.K_DOWN]:
            player.move(0, 1, maze)
        if keys[pygame.K_LEFT]:
            player.move(-1, 0, maze)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0, maze)

        if (player.pos_x, player.pos_y) == (maze.end_x, maze.end_y):
            pygame.quit()
            show_winner()
            break

        window.fill((0, 0, 0))
        maze.draw(window)
        player.draw(window)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def start_screen():
    start_window = tk.Tk()
    start_window.title("Welcome to Maze Adventure!")
    start_window.geometry("400x300")
    start_window.configure(bg="#6699ff")

    title_font = tkFont.Font(family="Helvetica", size=24, weight="bold")
    title_label = tk.Label(start_window, text="Maze Adventure", font=title_font, fg="white", bg="#6699ff")
    title_label.pack(pady=20)

    subtitle_font = tkFont.Font(family="Helvetica", size=14)
    subtitle_label = tk.Label(start_window, text="Guide your player through the maze!\nUse arrow keys to move.", font=subtitle_font, fg="white", bg="#6699ff")
    subtitle_label.pack(pady=10)

    def start_game():
        start_window.destroy()
        main_game()

    start_button = tk.Button(start_window, text="Start Game", command=start_game, font=subtitle_font, bg="#ffcc33", fg="black", padx=10, pady=5)
    start_button.pack(pady=20)

    start_window.mainloop()

if name == "main":
    start_screen()