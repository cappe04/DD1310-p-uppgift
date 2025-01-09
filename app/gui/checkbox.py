from app.gui.clickable import Clickable
from app.config import *

import pygame

class Checkbox(Clickable):
    """ Checkbox widget class. """
    def __init__(self, parent, position, is_center, width=10, height=10, checked=False):
        super().__init__(parent, position, is_center, width, height)

        self.checked = checked

        self.surface = pygame.Surface((width, height))

    def _on_click(self):
        """ Checks the box. """
        self.checked = not self.checked
    
    def _on_unclick(self):
        """ Inherited from Clickable, not used. """
        pass
    
    def _on_hover(self):
        """ Inherited from Clickable, not used. """
        pass

    def draw(self, target):
        """ Draws the widget.  """
        self.surface.fill(WHITE)
        if self.checked:
            pygame.draw.line(self.surface, BLACK, (1, 1), (self.width - 2, self.height - 2), width=2)
            pygame.draw.line(self.surface, BLACK, (self.width - 2, 1), (1, self.height - 2), width=2)
        target.blit(self.surface, (self.global_x, self.global_y))