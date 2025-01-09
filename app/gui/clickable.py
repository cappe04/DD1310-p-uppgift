import pygame

from app.gui.widget import Widget, WidgetEventArgs


class Clickable(Widget):
    """ To be inherited, used for widgets that needs to be clicked. """
    
    def __init__(self, parent, position, is_center, width, height):
        super().__init__(parent, position, is_center, width, height)


        self.is_pressed = False
        self.__previous_frame_click = False

        self.is_clicked = False

    def mouse_hover(self) -> bool:
        """ Returns True if mouse if hovering over widget, False if not. """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.global_x < mouse_x < self.global_x + self.width and self.global_y < mouse_y < self.global_y + self.height
    
    def _on_hover(self):
        """ Callback when Widget is hoverd over, to be inherited. """
        raise NotImplementedError

    def _on_click(self):
        """ Callback when widget is clicked, to be inherited. """
        raise NotImplementedError
    
    def _on_unclick(self):
        """ Callback when user clickes somewhere that is not in widget, to be inherited. """
        raise NotImplementedError

    def update(self, e: WidgetEventArgs):
        """ Updates the widget. """
        self.is_pressed = pygame.mouse.get_pressed()[0]
        # To isolate the first click
        self.is_clicked = self.is_pressed and not self.__previous_frame_click
        self.__previous_frame_click = self.is_pressed

        if self.mouse_hover():
            self._on_hover()
            if self.is_clicked:
                self._on_click()
        elif self.is_clicked:
            self._on_unclick()