import math, collections
from types import SimpleNamespace

import pygame


from app.config import *
import app.gui.text as text


class CellViewer(pygame.Surface):
    """
    Special "Widget" that draws the GameBoard, and interacts with it.
    """
    def __init__(self, width: int, height: int, cell_size: int):
        super().__init__((width, height))

        self.width, self.height = width, height
        self.__cell_size = cell_size
        self.cell_size = self.__cell_size

        self.viewbox_pos = SimpleNamespace(x=0, y=0)
        self.zoom_factor = 1

        self.fill(DARK_GRAY)

    def viewbox_cells(self):
        """ Generator that yields all cells visable in on the current screen. """
        x0 = math.floor(self.viewbox_pos.x - self.width / 2 / self.cell_size)
        x1 = math.floor(self.viewbox_pos.x + self.width / 2 / self.cell_size)

        y0 = math.floor(self.viewbox_pos.y - self.height / 2 / self.cell_size)
        y1 = math.floor(self.viewbox_pos.y + self.height / 2 / self.cell_size)
        
        for y in range(y0, y1):
            for x in range(x0, x1):
                yield (x, y)

    def move(self, dx: int, dy: int):
        """ Moves viewbox with given amount in pixels """
        self.viewbox_pos.x += dx
        self.viewbox_pos.y += dy

    def zoom(self, zoom_factor: float):
        """ Scales the viewbox area """
        self.zoom_factor += zoom_factor
        self.zoom_factor = min(max(self.zoom_factor, VIEW_MIN_ZOOM), VIEW_MAX_ZOOM)

        self.cell_size = self.__cell_size * self.zoom_factor

    def draw_view(self, game_board):
        """ 
        Draws the cells from the game_board that are visable in the viewbox area.

        game_board: GameBoard
        """
        self.fill(DARK_GRAY)

        for x, y in self.viewbox_cells():

            if not game_board.size is None:
                self.draw_border(game_board.size)

                if not (0 <= x < game_board.size[0] and 0 <= y < game_board.size[1]): # ta bort för cool effekt :)
                    continue

            if game_board[x, y]: # if cell is alive
                screen_x, screen_y = self.transform_to_screen(x, y)
                pygame.draw.rect(self, LIGHT_GRAY, (screen_x, screen_y, self.cell_size, self.cell_size))

        self.draw_cursor_highlight()

        # Draws the informative text in the top left.
        pos_text = text.get_text(f"{self.viewbox_pos.x:.1f}, {self.viewbox_pos.y:.1f}", WHITE, "Consolas", 20)
        self.blit(pos_text, (0, 0, pos_text.get_width(), pos_text.get_height()))

        gen_text = text.get_text(f"Generation: {game_board.generations}", WHITE, "Consolas", 20)
        self.blit(gen_text, (self.width * 0.2, 0, gen_text.get_width(), gen_text.get_height()))

        # Draw Center cursor
        pygame.draw.line(self, WHITE, (self.width / 2 - 5, self.height / 2), (self.width / 2 + 5, self.height / 2))
        pygame.draw.line(self, WHITE, (self.width / 2, self.height / 2 - 5), (self.width / 2, self.height / 2 + 5))

    def transform_to_screen(self, cell_x: int, cell_y: int):
        """ Transforms a given cell coordinate to a screen coordinate """
        screen_x = (cell_x - self.viewbox_pos.x) * self.cell_size + self.width // 2
        screen_y = (cell_y - self.viewbox_pos.y) * self.cell_size + self.height // 2
        return screen_x, screen_y
    
    def transform_to_cell(self, screen_x: int, screen_y: int):
        """ Transform a given screen coordinate to the corasponding cell """
        cell_x = math.floor((screen_x - self.width / 2 + self.viewbox_pos.x * self.cell_size) // self.cell_size)
        cell_y = math.floor((screen_y - self.height / 2 + self.viewbox_pos.y * self.cell_size) // self.cell_size)
        return cell_x, cell_y

    def draw_cursor_highlight(self):
        """ Draws marker that highlights the cell that is hovered over. """
        mouse = pygame.mouse.get_pos()
        if mouse[0] > self.width: return

        cell = self.transform_to_cell(*mouse)
        screen_pos = self.transform_to_screen(*cell)

        pygame.draw.rect(self, (0, 0, 0, 0), (*screen_pos, self.cell_size, self.cell_size), width=2)

    def draw_border(self, size: tuple[int, int]):
        """ Draws the border. """
        x0, y0 = self.transform_to_screen(0, 0)
        x1, y1 = self.transform_to_screen(*size)
        
        pygame.draw.rect(self, WHITE, (x0, y0, x1 - x0, y1 - y0), width=2)

    def toggle_cell(self, game_board):
        """
        Toggles the life of the cell that is clicked. 
        game_board: GameBoard
        """
        mouse = pygame.mouse.get_pos()
        if mouse[0] > self.width: return
    
        cell = self.transform_to_cell(*mouse)

        game_board.toggle_cell(*cell)
        


