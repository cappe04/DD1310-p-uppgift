# File for contstants and also types

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
CELL_SIZE = 20

GAME_TICK = 10 # TICKS / s

VIEW_SPEED = 50
VIEW_ZOOM = 1
VIEW_MIN_ZOOM = 0.1
VIEW_MAX_ZOOM = 5


# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DARK_DARK_GRAY = (30, 30, 30)
DARK_GRAY = (50, 50, 50)
GRAY = (90, 90, 90)
LIGHT_GRAY = (200, 200, 200)

# --- Types for typing ---
type Color = tuple[int]
type Font = tuple[str, int]
type Position = tuple[int, int]
