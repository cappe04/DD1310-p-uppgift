import pygame

from app.gui.clickable import Clickable
from app.gui.text import get_text
from app.config import *

class Button(Clickable):

    hover_scaleup = 2

    def __init__(self, center, text, on_click, fg=WHITE, bg=GRAY, font=("Consolas", 20), padding=10, width=None, height=None):
        self.text = get_text(text, fg, *font)

        self.fg = fg
        self.bg = bg
        self.padding = padding

        width = width or (self.text.get_width() + self.padding * 2)
        height = height or (self.text.get_height() + self.padding * 2)

        x, y = center

        super().__init__(x - width / 2, y - height / 2, width, height)

        self.fill(self.bg)
        self.blit(self.text, (self.padding, self.padding, self.text.get_width(), self.text.get_height()))

        self.on_click = on_click

    def on_unclick(self):
        pass

    def on_hover(self):
        pass
    
    def draw(self, target):
        hover = self.mouse_hover()
        x = self.x - hover * self.hover_scaleup
        y = self.y - hover * self.hover_scaleup
        width = self.width + hover * self.hover_scaleup * 2
        height = self.height + hover * self.hover_scaleup * 2
        
        target.blit(pygame.transform.scale(self, (width, height)), (x, y))