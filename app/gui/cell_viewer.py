import math, collections
from types import SimpleNamespace

import pygame


from app.config import *
import app.gui.text as text


class CellViewer(pygame.Surface):
    
    def __init__(self, width, height, cell_size):
        super().__init__((width, height))

        self.width, self.height = width, height
        self.__cell_size = cell_size
        self.cell_size = self.__cell_size

        self.viewbox_pos = SimpleNamespace(x=0, y=0)
        self.zoom_factor = 1

        self.fill(DARK_GRAY)

    def viewbox_cells(self):
        x0 = math.floor(self.viewbox_pos.x - self.width / 2 / self.cell_size)
        x1 = math.floor(self.viewbox_pos.x + self.width / 2 / self.cell_size)

        y0 = math.floor(self.viewbox_pos.y - self.height / 2 / self.cell_size)
        y1 = math.floor(self.viewbox_pos.y + self.height / 2 / self.cell_size)
        
        for y in range(y0, y1):
            for x in range(x0, x1):
                yield (x, y)

    def move(self, dx, dy):
        self.viewbox_pos.x += dx
        self.viewbox_pos.y += dy

    def zoom(self, zoom_factor):
        self.zoom_factor += zoom_factor
        self.zoom_factor = min(max(self.zoom_factor, VIEW_MIN_ZOOM), VIEW_MAX_ZOOM)

        self.cell_size = self.__cell_size * self.zoom_factor

    def draw_view(self, game_board):
        self.fill(DARK_GRAY)

        for x, y in self.viewbox_cells():
            if game_board[x, y]:
                screen_x, screen_y = self.transform_to_screen(x, y)
                pygame.draw.rect(self, LIGHT_GRAY, (screen_x, screen_y, self.cell_size, self.cell_size))

        self.draw_cursor_highlight()

        pos_text = text.get_text(f"{self.viewbox_pos.x:.1f}, {self.viewbox_pos.y:.1f}", WHITE, "Consolas", 20)
        self.blit(pos_text, (0, 0, pos_text.get_width(), pos_text.get_height()))

        gen_text = text.get_text(f"Generation: {game_board.generations}", WHITE, "Consolas", 20)
        self.blit(gen_text, (self.width * 0.2, 0, gen_text.get_width(), gen_text.get_height()))

        # Marker
        pygame.draw.line(self, WHITE, (self.width / 2 - 5, self.height / 2), (self.width / 2 + 5, self.height / 2))
        pygame.draw.line(self, WHITE, (self.width / 2, self.height / 2 - 5), (self.width / 2, self.height / 2 + 5))

    def transform_to_screen(self, cell_x, cell_y):
        screen_x = (cell_x - self.viewbox_pos.x) * self.cell_size + self.width // 2
        screen_y = (cell_y - self.viewbox_pos.y) * self.cell_size + self.height // 2
        return screen_x, screen_y
    
    def transform_to_cell(self, screen_x, screen_y):
        cell_x = math.floor((screen_x - self.width / 2 + self.viewbox_pos.x * self.cell_size) // self.cell_size)
        cell_y = math.floor((screen_y - self.height / 2 + self.viewbox_pos.y * self.cell_size) // self.cell_size)
        return cell_x, cell_y

    def draw_cursor_highlight(self):
        mouse = pygame.mouse.get_pos()

        cell = self.transform_to_cell(*mouse)
        screen_pos = self.transform_to_screen(*cell)

        pygame.draw.rect(self, (0, 0, 0, 0), (*screen_pos, self.cell_size, self.cell_size), width=2)

    def toggle_cell(self, game_board):
        mouse = pygame.mouse.get_pos()
    
        cell = self.transform_to_cell(*mouse)

        game_board.toggle_cell(*cell)
        


