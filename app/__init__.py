import pygame

from app.app import App

def run(game_size: tuple[int, int] | None = None):
    pygame.init()
    pygame.font.init()

    app = App(game_size)
    app.mainloop()
    
