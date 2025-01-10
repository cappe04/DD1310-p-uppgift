import pygame

from app.app import App

def run(board_size: tuple[int, int] | None = None):
    pygame.init()
    pygame.font.init()

    app = App(board_size)
    app.mainloop()
    
