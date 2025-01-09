from app.gui.widget import Widget, WidgetEventArgs
from app.config import *
import pygame


class Frame(Widget):
    """ Frame widget class. Used as a container for other widgets. """
    def __init__(self, parent: Widget, position: Position, is_center: bool, width: int, height: int, bg=DARK_DARK_GRAY):
        super().__init__(parent, position, is_center, width, height)

        self.width = width
        self.height = height

        self.bg = bg

    def update(self, e: WidgetEventArgs):
        """ Updates Frame widget and all it's children. """
        for child in self.get_children():
            child.update(e)

    def draw(self, target):
        """ Draws Frame widget and all it's children. """
        pygame.draw.rect(target, self.bg, (self.global_x, self.global_y, self.width, self.height))

        for child in self.get_children():
            child.draw(target)