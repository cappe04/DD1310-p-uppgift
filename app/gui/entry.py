import pygame

from app.gui.clickable import Clickable
from app.gui.label import Label
from app.gui.frame import Frame
from app.gui.text import get_text
from app.config import *
from app.gui.widget import Widget


class Entry(Clickable):

    inner_padding = 2
    outer_padding = 5

    def __init__(self, parent, position, is_center, font=("Consolas", 20), bg=GRAY, text="0000", max_length=4, width=None, height=None):
        self.font = font
        self.max_length = max_length
        self.message = text
        self.bg = bg

        self.text = get_text(self.message, BLACK, *self.font)
        width = width or (self.text.get_width() + self.outer_padding * 2 + self.inner_padding * 2)
        height = height or (self.text.get_height() + self.outer_padding * 2 + self.inner_padding * 2)

        super().__init__(parent, position, is_center, width, height)

        self.selected = False

        self.surface = pygame.Surface((width, height))

        self.surface.fill(bg)
        self.update_text()

    def update_text(self):
        pygame.draw.rect(self.surface, WHITE if self.selected else LIGHT_GRAY, 
                         (self.outer_padding, self.outer_padding, self.width - self.outer_padding * 2, self.height - self.outer_padding * 2))
        self.text = get_text(self.message, BLACK, *self.font)
        self.surface.blit(self.text, (self.width / 2 - self.text.get_width() / 2, self.height / 2 - self.text.get_height() / 2))

    def message_append(self, char):
        message = self.message.lstrip("0")
        if len(message) >= self.max_length:
            return
        
        message += char
        self.message = f"{message:{"0"}>{self.max_length}}"

    def message_pop(self):
        self.message = f"{self.message[:-1]:{"0"}>{self.max_length}}"

    def _on_click(self):
        self.selected = True
        self.message = "0000"
        self.update_text()
        pygame.draw.rect(self.surface, WHITE, (1, 1, self.width-2, self.height-2), width=1)

    def _on_unclick(self):
        self.selected = False
        self.update_text()
        pygame.draw.rect(self.surface, self.bg, (1, 1, self.width-2, self.height-2), width=1)
        self.on_unclick()

    def _on_hover(self):
        pass

    def update(self, e):
        super().update(e)

        if not self.selected:
            return
        
        for key in e.keylogger:
            if key == pygame.K_BACKSPACE:
                self.message_pop()

            if pygame.K_0 <= key <= pygame.K_9:
                self.message_append(chr(key))

        self.update_text()

    def get_numeric(self):
        value = self.message.lstrip("0")
        value = "0" if value == "" else value
        return int(value)
    
    def get_str(self):
        return self.message.lstrip("0")

    def draw(self, target):
        draw_surface = self.surface
            

        target.blit(draw_surface, (self.global_x, self.global_y))

    def on_unclick(self):
        """ Overideable funtion for handling events """
        pass