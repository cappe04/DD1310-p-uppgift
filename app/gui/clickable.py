import pygame

from app.gui.widget import Widget, WidgetEventArgs


class Clickable(Widget):
    def __init__(self, parent, position, is_center, width, height):
        super().__init__(parent, position, is_center, width, height)


        self.is_pressed = False
        self.__previous_frame_click = False

        self.is_clicked = False

    def mouse_hover(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.global_x < mouse_x < self.global_x + self.width and self.global_y < mouse_y < self.global_y + self.height
    
    def _on_hover(self):
        raise NotImplementedError

    def _on_click(self):
        raise NotImplementedError
    
    def _on_unclick(self):
        raise NotImplementedError

    def update(self, e: WidgetEventArgs):
        self.is_pressed = pygame.mouse.get_pressed()[0]
        self.is_clicked = self.is_pressed and not self.__previous_frame_click
        self.__previous_frame_click = self.is_pressed

        if self.mouse_hover():
            self._on_hover()
            if self.is_clicked:
                self._on_click()
        elif self.is_clicked:
            self._on_unclick()