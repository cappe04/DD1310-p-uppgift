import pygame

from app.gui.clickable import Clickable
from app.gui.text import get_text
from app.config import *
from app.gui.widgets import widget


@widget(layer="entry")
class Entry(Clickable):

    inner_padding = 2
    outer_padding = 5

    def __init__(self, center, font=("Consolas", 20), bg=GRAY, text="0000", max_length=4, width=None, height=None):
        self.font = font
        self.max_length = max_length
        self.message = text

        self.text = get_text(self.message, BLACK, *self.font)
        width = width or (self.text.get_width() + self.outer_padding * 2 + self.inner_padding * 2)
        height = height or (self.text.get_height() + self.outer_padding * 2 + self.inner_padding * 2)

        x, y = center

        super().__init__(x - width / 2, y - height / 2, width, height)

        self.selected = False

        self.fill(bg)
        self.update_text()

    def update_text(self):
        pygame.draw.rect(self, WHITE if self.selected else LIGHT_GRAY, 
                         (self.outer_padding, self.outer_padding, self.width - self.outer_padding * 2, self.height - self.outer_padding * 2))
        self.text = get_text(self.message, BLACK, *self.font)
        self.blit(self.text, (self.width / 2 - self.text.get_width() / 2, self.height / 2 - self.text.get_height() / 2))

    def message_append(self, char):
        message = self.message.lstrip("0")
        if len(message) >= self.max_length:
            return
        
        message += char
        self.message = f"{message:{"0"}>{self.max_length}}"

    def message_pop(self):
        self.message = f"{self.message[:-1]:{"0"}>{self.max_length}}"

    def on_click(self):
        self.selected = True
        self.update_text()

    def on_unclick(self):
        self.selected = False
        self.update_text()

    def on_hover(self):
        pass

    def update(self, keylogger):
        super().update()

        if not self.selected:
            return
        
        for key in keylogger:
            if key == pygame.K_BACKSPACE:
                self.message_pop()

            if pygame.K_0 <= key <= pygame.K_9:
                self.message_append(chr(key))

        self.update_text()


@widget(layer="label_entry")
class LabelEntry:
    def __init__(self, center, text, font, start_text="0000", bg=GRAY, padding=10, **entry_options):
        self.text = get_text(text, WHITE, *font)
        
        self.padding = padding
        self.center = center

        label_width = self.text.get_width() + padding * 2
        label_height = self.text.get_height() + padding * 2

        self.entry = Entry((0, 0), text=start_text, height=label_height, **entry_options)

        self.width = label_width + self.entry.width
        self.height = label_height

        self.entry.x = center[0] - self.width / 2 + label_width
        self.entry.y = center[1] - self.height / 2

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(bg)

    def update(self, keylogger):
        self.entry.update(keylogger)

    def draw(self, target):
        self.surface.blit(self.text, (self.padding, self.padding))
        target.blit(self.surface, (self.center[0] - self.width / 2, self.center[1] - self.height / 2))
        self.entry.draw(target)



        


