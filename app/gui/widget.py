

class WidgetEventArgs:
    def __init__(self, keylogger):
        self.keylogger = keylogger


class Widget:

    parent_widgets = {}

    def __init__(self, parent, position, is_center, width, height):
        self.parent = parent
        self.width = width
        self.height = height

        self.update_position(position, is_center)

        if parent is None:
            return
        
        if not parent in self.parent_widgets.keys():
            self.parent_widgets[parent] = []

        self.parent_widgets[parent].append(self)

    def update_position(self, position, is_center):
        self.x, self.y = position if not is_center else (position[0] - self.width / 2, position[1] - self.height / 2)

        self.global_x, self.global_y = self.x, self.y

        if not self.parent is None:
            self.global_x, self.global_y = self.parent.global_x + self.x, self.parent.global_y + self.y

        if self.is_parent():
            for child in self.get_children():
                child.update_position((child.x, child.y), False)
        

    def is_parent(self):
        return self in self.parent_widgets.keys()

    def get_children(self):
        return self.parent_widgets.get(self, [])
    
    def update(self, e: WidgetEventArgs):
        raise NotImplementedError
    
    def draw(self, target):
        raise NotImplementedError


# class Frame(Widget):
#     def __init__(self, parent, position, is_center, width, height):
#         super().__init__(parent, position, is_center, width, height)

# class Button(Widget):
#     def __init__(self, parent, position, is_center, width, height):
#         super().__init__(parent, position, is_center, width, height)


# frame = Frame(None, (10, 10), False, 90, 90)
# button = Button(frame, (45, 45), True, 30, 20)

