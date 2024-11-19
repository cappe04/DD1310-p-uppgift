import pygame

__fonts = {}

def get_text(text, color, font_name, size, antialias=False) -> pygame.Surface:
    if not (font_name, size) in __fonts:
        __fonts[(font_name, size)] = pygame.font.SysFont(font_name, size)

    font = __fonts[(font_name, size)]
    return font.render(text, antialias, color)
