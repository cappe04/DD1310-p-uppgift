import pygame

from app.app import App

def run():
    pygame.init()
    pygame.font.init()

    app = App()
    app.mainloop()
    
