import pygame

class Clickable(pygame.Surface):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        
        self.width = width
        self.height = height

        super().__init__((self.width, self.height))

        self.__current_frame_click = False
        self.__previous_frame_click = False

        self.is_pressed = False

    def mouse_hover(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height
    
    def on_hover(self):
        raise NotImplementedError

    def on_click(self):
        raise NotImplementedError
    
    def on_unclick(self):
        raise NotImplementedError

    def update(self):
        self.__current_frame_click = pygame.mouse.get_pressed()[0]
        self.is_pressed = self.__current_frame_click and not self.__previous_frame_click
        self.__previous_frame_click = self.__current_frame_click

        if self.mouse_hover():
            self.on_hover()
            if self.is_pressed:
                self.on_click()
        else:
            self.on_unclick()

    def draw(self, target):
        target.blit(self, (self.x, self.y, self.width, self.height))