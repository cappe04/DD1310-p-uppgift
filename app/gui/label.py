import pygame
from app.config import *
from app.gui.widget import Widget
from app.gui.text import get_text

class Label(Widget):
    """ Label Widget class for creating text on screen. """
    def __init__(self, parent: Widget, position: Position, is_center: bool, text: str, color: Color, font: Font, padding=0, bg=BLACK):
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
        """ Not needed for Label as it's static. """
        pass

    def draw(self, target):
        """ Draws the label on the screen. """
        target.blit(self.surface, (self.global_x, self.global_y))