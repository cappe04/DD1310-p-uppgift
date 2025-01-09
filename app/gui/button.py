import pygame

from app.gui.clickable import Clickable
from app.gui.text import get_text
from app.config import *


class Button(Clickable):
    
    """ Button widget class """

    hover_scaleup = 2

    def __init__(self, parent, position, is_center, text, on_click, fg=WHITE, bg=GRAY, font=("Consolas", 20), padding=10, width=None, height=None):
        self.text = get_text(text, fg, *font)

        self.fg = fg
        self.bg = bg
        self.padding = padding

        width = width or (self.text.get_width() + self.padding * 2)
        height = height or (self.text.get_height() + self.padding * 2)

        super().__init__(parent, position, is_center, width, height)

        self.surface = pygame.Surface((width, height))

        self.surface.fill(self.bg)
        self.surface.blit(self.text, (self.padding, self.padding, self.text.get_width(), self.text.get_height()))

        self._on_click = on_click

    def _on_unclick(self):
        pass

    def _on_hover(self):
        pass
    
    def draw(self, target):
        hover = self.mouse_hover()
        x = self.global_x - hover * self.hover_scaleup
        y = self.global_y - hover * self.hover_scaleup
        width = self.width + hover * self.hover_scaleup * 2
        height = self.height + hover * self.hover_scaleup * 2
        

        draw_surface = pygame.transform.scale(self.surface, (width, height))
        if hover:
            pygame.draw.rect(draw_surface, self.fg, (2, 2, width-4, height-4), width=2)

        if self.is_pressed and hover:
            pygame.draw.rect(draw_surface, self.bg, (0, 0, width, height))


        target.blit(draw_surface, (x, y))