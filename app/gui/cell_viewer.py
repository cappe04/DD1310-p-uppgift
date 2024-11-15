import math

import pygame

from app.config import *

class CellViewer(pygame.Surface):
    
    def __init__(self, width, height, cell_size):
        super().__init__((width, height))

        self.width, self.height = width, height
        self.cell_size = cell_size

        self.viewbox_pos = [0, 0]
        self.zoom_factor = 1

        self.fill(DARK_GRAY)


    def viewbox_cells(self):
        x0 = math.floor(self.viewbox_pos[0] / self.cell_size)
        x1 = math.floor((self.viewbox_pos[0] + self.width) / self.cell_size)

        y0 = math.floor(self.viewbox_pos[1] / self.cell_size)
        y1 = math.floor((self.viewbox_pos[1] + self.height) / self.cell_size)
        
        for y in range(y0, y1):
            for x in range(x0, x1):
                yield (x, y)

    def move(self, dx, dy):
        self.viewbox_pos[0] += dx
        self.viewbox_pos[1] += dy

    def zoom(self, zoom_factor):
        self.zoom_factor += zoom_factor
        self.zoom_factor = min(max(self.zoom_factor, VIEW_MIN_ZOOM), VIEW_MAX_ZOOM)

    def draw_view(self, game_board):
        cell_size = self.cell_size * self.zoom_factor
        self.fill(DARK_GRAY)
        for x, y in self.viewbox_cells():
            if game_board[x, y]:
                screen_x = x * cell_size - self.viewbox_pos[0]
                screen_y = y * cell_size - self.viewbox_pos[1]
                pygame.draw.rect(self, WHITE, (screen_x, screen_y, cell_size, cell_size))


