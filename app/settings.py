"""Game-wide constants. Change values here to tune gameplay."""

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
TITLE = "Centipede"
FPS = 60

# ---------------------------------------------------------------------------
# Colors (RGB)
# ---------------------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (220, 220, 0)
BROWN = (139, 90, 43)

# ---------------------------------------------------------------------------
# Grid
# ---------------------------------------------------------------------------
CELL_SIZE = 20  # pixels per grid cell; all entities snap to this grid
COLS = SCREEN_WIDTH // CELL_SIZE   # 30
ROWS = SCREEN_HEIGHT // CELL_SIZE  # 40

# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------
PLAYER_SPEED = 4          # pixels per frame
PLAYER_ZONE_ROWS = 5      # rows from bottom the player can occupy
BULLET_SPEED = 10         # pixels per frame upward

# ---------------------------------------------------------------------------
# Centipede
# ---------------------------------------------------------------------------
CENTIPEDE_LENGTH = 12     # number of segments
CENTIPEDE_SPEED = 2       # pixels per frame horizontal
CENTIPEDE_DROP = CELL_SIZE  # pixels to drop when hitting a wall

# ---------------------------------------------------------------------------
# Mushroom field
# ---------------------------------------------------------------------------
MUSHROOM_COUNT = 30
MUSHROOM_HP = 4           # hits to destroy a mushroom
