from app.gui.clickable import Clickable
from app.config import *

import pygame

class Checkbox(Clickable):
    def __init__(self, x, y, width=10, height=10, checked=False):
        super().__init__(x - width / 2, y - height / 2)

        self.checked = checked

    def on_click(self):
        self.checked = not self.checked
    
    def on_unclick(self):
        pass
    
    def on_hover(self):
        pass

    def draw(self, target):
        self.fill(WHITE)
        if self.checked:
            pygame.draw.line(self, BLACK, (1, 1), (self.width - 1, self.height - 1))
            pygame.draw.line(self, BLACK, (self.width - 1, 1), (0, self.height - 1))
        super().draw(target)