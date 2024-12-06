import pygame
from app.config import *
from app.gui.widget import Widget
from app.gui.text import get_text

class Label(Widget):
    def __init__(self, parent, position, is_center, text, color, font, padding=0, bg=BLACK):
        self.bg = bg
        self.padding = padding

        self.text = get_text(text, color, *font)
        width = self.text.get_width() + padding * 2
        height = self.text.get_height() + padding * 2

        super().__init__(parent, position, is_center, width, height)

        self.surface = pygame.Surface((width, height))
        self.surface.fill(self.bg)
        self.surface.blit(self.text, (self.padding, self.padding))

    def update(self, e):
        pass

    def draw(self, target):
        target.blit(self.surface, (self.global_x, self.global_y))