import pygame
from app.config import Position

class WidgetEventArgs:
    """ Contains data that is passed to each widget each frame """
    def __init__(self, keylogger):
        self.keylogger = keylogger


class Widget:
    """
    A class to be inherited for all widgets.
    """

    parent_widgets = {}

    def __init__(self, parent, position: Position, is_center: bool, width: int, height: int):
        """ Creates widget instance, may take parent widget as either a Wiget or None """
        self.parent = parent
        self.width = width
        self.height = height

        self.update_position(position, is_center)

        if parent is None:
            return
        
        if not parent in self.parent_widgets.keys():
            self.parent_widgets[parent] = []

        self.parent_widgets[parent].append(self)

    def update_position(self, position: tuple, is_center: bool):
        """ Updates position of widget and all it's children. """
        self.x, self.y = position if not is_center else (position[0] - self.width / 2, position[1] - self.height / 2)

        self.global_x, self.global_y = self.x, self.y

        if not self.parent is None:
            self.global_x, self.global_y = self.parent.global_x + self.x, self.parent.global_y + self.y

        if self.is_parent():
            for child in self.get_children():
                child.update_position((child.x, child.y), False)
        

    def is_parent(self) -> bool:
        """ Checks if widget is parent """
        return self in self.parent_widgets.keys()

    def get_children(self):
        """ Returns a list of widgets children """
        return self.parent_widgets.get(self, [])
    
    def update(self, e: WidgetEventArgs):
        """ Updates widget, to be overriden. """
        raise NotImplementedError
    
    def draw(self, target: pygame.Surface):
        """ Draws widget, to be overriden. """
        raise NotImplementedError
