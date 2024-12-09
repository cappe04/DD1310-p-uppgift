from app.config import *
from app.gui.frame import Frame
from app.gui.label import Label
from app.gui.checkbox import Checkbox
from app.gui.widget import Widget

class BorderOptions(Widget):
    def __init__(self, position, is_center):
        
        self.frame = Frame(None, position, is_center, 0, 0)

        self.padding = 10

        self.checkbox = Checkbox(self.frame, (self.padding, self.padding), False)
        