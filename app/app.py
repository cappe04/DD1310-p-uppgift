import pygame

from app.config import *
# from app.gui.cell_viewer import CellViewer
# from app.gui.button import Button
# from app.gui.entry import Entry, LabelEntry

from app.game_board import GameBoard
from app.gui.widget import WidgetEventArgs
import app.template_loader as template_loader

from app.gui import Button, LabelEntry, Entry, Text, CellViewer, Frame, Label, Checkbox

# ---------------------------------------------
# TODO: add target simulations, pause after X generations
# TODO: add steps per tick
# TODO: add widgets
# TODO: koordinater ska ligga i tillåtet intevall?? alltså alla??

# ---------------------------------------------
# TODO: add change in simulation speed
# ---------------------------------------------

class App:
    def __init__(self):
        
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()

        self.is_running = True
        
        self.game_board = GameBoard()

        # widgets
        self.cell_viewer = CellViewer(WINDOW_WIDTH * 0.7, WINDOW_HEIGHT, CELL_SIZE)

        self.side_panel = Frame(None, (WINDOW_WIDTH * 0.7, 0), False, WINDOW_WIDTH * 0.3, WINDOW_HEIGHT, bg=DARK_DARK_GRAY)

        self.header_label = Label(self.side_panel, (self.side_panel.width / 2, WINDOW_HEIGHT * 0.08), True, "Game of Life", WHITE, ("Consolas", 30), bg=DARK_DARK_GRAY)

        self.step_entry = LabelEntry(self.side_panel, (self.side_panel.width / 2, WINDOW_HEIGHT * 0.39), True, "Steps:", bg=DARK_DARK_GRAY, text="0001")
        self.target_entry = LabelEntry(self.side_panel, (self.side_panel.width / 2, WINDOW_HEIGHT * 0.22), True, "Target:", bg=DARK_DARK_GRAY, text="0000")

        self.pause_button = Button(self.side_panel, (self.side_panel.width / 2, WINDOW_HEIGHT * 0.26), True, "Pause / Play", self.pause_simulation)
        self.next_button = Button(self.side_panel, (self.side_panel.width / 2, WINDOW_HEIGHT * 0.43), True, "Next Frame", self.tick)
        self.clear_button = Button(self.side_panel, (self.side_panel.width / 2, WINDOW_HEIGHT * 0.7), True, "Clear Screen", self.game_board.clear_board)
        self.load_button = Button(self.side_panel, (self.side_panel.width / 2, WINDOW_HEIGHT * 0.8), True, "Load Figure", self.ask_open_file)
        

        # self.bounds_checkbox = Checkbox(self.side_panel, (self.side_panel.width / 2, WINDOW_HEIGHT * 0.9), True)
        

        self.delta_time = self.clock.tick() * 0.001

        self.s_per_tick = 1 / GAME_TICK
        self.s_since_last_tick = 0
        self.steps_per_tick = self.step_entry.entry.get_numeric()
        self.step_target = 0

        self.step_entry.entry.on_unclick = self.update_steps_per_tick
        self.target_entry.entry.on_unclick = self.update_target_steps

        self.simulation_paused = True

        self.keylogger = set()

    def mainloop(self):
        while self.is_running:
            
            self.display.fill(WHITE)

            event_args = self.handle_events()

            # Update game board
            self.s_since_last_tick += self.delta_time
            if self.s_per_tick < self.s_since_last_tick:
                if not self.simulation_paused:
                    self.tick()
                self.s_since_last_tick = 0

            self.side_panel.update(event_args)

            self.cell_viewer.draw_view(self.game_board)
            self.display.blit(self.cell_viewer, (0, 0, self.cell_viewer.width, self.cell_viewer.height))

            self.side_panel.draw(self.display)

            self.delta_time = self.clock.tick() * 0.001
            pygame.display.flip()

    def tick(self):
        steps = self.steps_per_tick
        if self.game_board.generations < self.step_target and self.step_target - self.game_board.generations <= self.steps_per_tick:
            steps = self.step_target - self.game_board.generations
            self.simulation_paused = True

        for _ in range(steps):
            self.game_board.step()

    def handle_events(self):
        keylogger = set()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.tick()
                if event.key == pygame.K_SPACE:
                    self.pause_simulation()
                if event.key == pygame.K_l:
                    self.ask_open_file()
                if event.key == pygame.K_r:
                    self.cell_viewer.zoom_factor = 1
                    self.cell_viewer.viewbox_pos.x = 0
                    self.cell_viewer.viewbox_pos.y = 0

                keylogger.add(event.key)

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

        return WidgetEventArgs(keylogger)

    def ask_open_file(self):
        def callback(coords):
            if coords is None:
                return
            
            for x, y in coords:
                self.game_board.toggle_cell(x + int(self.cell_viewer.viewbox_pos.x), y + int(self.cell_viewer.viewbox_pos.y))

        template_loader.on_file_opened(callback)

    def pause_simulation(self):
        self.simulation_paused = not self.simulation_paused

    def update_steps_per_tick(self):
        steps_per_tick = self.step_entry.entry.get_numeric()
        self.steps_per_tick = max(steps_per_tick, 1)

    def update_target_steps(self):
        target = self.target_entry.entry.get_numeric()
        self.step_target = target