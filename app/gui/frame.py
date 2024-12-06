from app.gui.widget import Widget, WidgetEventArgs
from app.config import *
import pygame


class Frame(Widget):
    def __init__(self, parent, position, is_center, width, height, bg=DARK_DARK_GRAY):
        super().__init__(parent, position, is_center, width, height)

        self.width = width
        self.height = height

        self.bg = bg

    def update(self, e: WidgetEventArgs):
        for child in self.get_children():
            child.update(e)

    def draw(self, target):

        pygame.draw.rect(target, self.bg, (self.global_x, self.global_y, self.width, self.height))

        for child in self.get_children():
            child.draw(target)