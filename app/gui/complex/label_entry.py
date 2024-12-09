from app.config import *
from app.gui.frame import Frame
from app.gui.label import Label
from app.gui.widget import Widget
from app.gui.entry import Entry


class LabelEntry(Widget):
    def __init__(self, parent, position, is_center, label, font=("Consolas", 20), bg=GRAY, **entry_options):

        self.frame = Frame(None, (0, 0), False, 0, 0, bg)

        self.label = Label(self.frame, (0, 0), False, label, WHITE, font, padding=5, bg=bg)
        self.entry = Entry(self.frame, (self.label.width, 0), False, font=font, bg=bg, height=self.label.height, **entry_options)

        self.frame.width = self.label.width + self.entry.width
        self.frame.height = self.label.height + self.entry.height

        super().__init__(parent, position, is_center, self.frame.width, self.frame.height)

        self.frame.update_position((self.global_x, self.global_y), False)

    def update(self, e):
        self.frame.update(e)

    def draw(self, target):
        self.frame.draw(target)