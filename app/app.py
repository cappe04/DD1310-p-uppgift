import pygame

from app.config import *
from app.gui.cell_viewer import CellViewer
from app.gui.button import Button
from app.game_board import GameBoard
import app.template_loader as template_loader

# ---------------------------------------------
# TODO: add border option so it loops around
# TODO: add target simulations, pause after X generations
# TODO: add steps per tick
# TODO: add widgets
# TODO: add mouse checks in cell_viewer
# ---------------------------------------------
# TODO: add change in simulation speed
# ---------------------------------------------

class App:
    def __init__(self):
        
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()

        self.is_running = True

        # widgets
        self.cell_viewer = CellViewer(WINDOW_WIDTH * 0.7, WINDOW_HEIGHT, CELL_SIZE)
        self.load_button = Button((WINDOW_WIDTH * 0.85, WINDOW_HEIGHT * 0.8), "Load Figure", self.ask_open_file)
        self.clear_button = Button((WINDOW_WIDTH * 0.85, WINDOW_HEIGHT * 0.4), "Clear Screen", lambda: ...)
        self.next_button = Button((WINDOW_WIDTH * 0.85, WINDOW_HEIGHT * 0.7), "Next Frame", lambda: ...)
        self.pause_button = Button((WINDOW_WIDTH * 0.85, WINDOW_HEIGHT * 0.6), "Pause", lambda: ...)
        
        
        self.game_board = GameBoard()

        self.delta_time = self.clock.tick() * 0.001

        self.s_per_tick = 1 / GAME_TICK
        self.s_since_last_tick = 0
        self.steps_per_tick = 4

        self.simulation_paused = True

    def mainloop(self):
        while self.is_running:
            
            self.display.fill(WHITE)

            self.handle_events()

            # Update game board
            self.s_since_last_tick += self.delta_time
            if self.s_per_tick < self.s_since_last_tick:
                if not self.simulation_paused:
                    self.tick()
                self.s_since_last_tick = 0

            self.load_button.update()
            self.clear_button.update()
            self.pause_button.update()
            self.next_button.update()

            self.cell_viewer.draw_view(self.game_board)
            self.display.blit(self.cell_viewer, (0, 0, self.cell_viewer.width, self.cell_viewer.height))

            self.load_button.draw(self.display)
            self.clear_button.draw(self.display)
            self.pause_button.draw(self.display)
            self.next_button.draw(self.display)

            self.delta_time = self.clock.tick() * 0.001
            pygame.display.flip()

    def tick(self):
        for _ in range(self.steps_per_tick):
            self.game_board.step()

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.tick()
                    if event.key == pygame.K_SPACE:
                        self.simulation_paused = not self.simulation_paused
                    if event.key == pygame.K_l:
                        self.ask_open_file()
                    if event.key == pygame.K_r:
                        self.cell_viewer.zoom_factor = 1
                        self.cell_viewer.viewbox_pos.x = 0
                        self.cell_viewer.viewbox_pos.y = 0
                    if event.key == pygame.K_p:
                        print(self.cell_viewer.viewbox_pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cell_viewer.toggle_cell(self.game_board)


        keys = pygame.key.get_pressed()
        move_speed = VIEW_SPEED * self.delta_time
        zoom_speed = VIEW_ZOOM * self.delta_time
        if keys[pygame.K_w]:
            self.cell_viewer.move(0, -move_speed)
        if keys[pygame.K_s]:
            self.cell_viewer.move(0, move_speed)
        if keys[pygame.K_a]:
            self.cell_viewer.move(-move_speed, 0)
        if keys[pygame.K_d]:
            self.cell_viewer.move(move_speed, 0)
        if keys[pygame.K_UP]:
            self.cell_viewer.zoom(zoom_speed)
        if keys[pygame.K_DOWN]:
            self.cell_viewer.zoom(-zoom_speed)

    def ask_open_file(self):
        def callback(coords):
            for x, y in coords:
                self.game_board.toggle_cell(x + int(self.cell_viewer.viewbox_pos.x), y + int(self.cell_viewer.viewbox_pos.y))

        template_loader.on_file_opened(callback)