import pygame

__fonts = {} # Private dict to act as a cache for fonts

def get_text(text: str, color: tuple[int], font_name: str, size: int, antialias=False) -> pygame.Surface:
    """ Creates a pygame surface with give text parameters. """
    if not (font_name, size) in __fonts:
        __fonts[(font_name, size)] = pygame.font.SysFont(font_name, size)
    
    font = __fonts[(font_name, size)]
    return font.render(text, antialias, color)
