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
CENTIPEDE_LENGTH = 12
CENTIPEDE_BASE_STEPS = 8        # grid steps per second at level 1
CENTIPEDE_STEPS_INCREMENT = 1   # extra steps/sec gained each level (gentler curve)
CENTIPEDE_MAX_STEPS = 24        # cap — one step every 2.5 frames at 60fps
CENTIPEDE_START_ROW_INCREMENT = 2   # rows further down the centipede starts each level
CENTIPEDE_MAX_START_ROW = 10        # never starts below this row

# ---------------------------------------------------------------------------
# Level progression
# ---------------------------------------------------------------------------
MAX_LEVEL = 10
LEVEL_CLEAR_FRAMES = 90  # 1.5 seconds at 60 fps before next wave spawns

# ---------------------------------------------------------------------------
# Player lives
# ---------------------------------------------------------------------------
PLAYER_LIVES = 3
DEATH_FLASH_FRAMES = 60   # 1 second at 60 fps before respawn

# ---------------------------------------------------------------------------
# Flea
# ---------------------------------------------------------------------------
FLEA_STEPS = 12                # grid steps per second downward
FLEA_HP = 2                    # hits to kill
FLEA_SCORE = 200
FLEA_DROP_CHANCE = 0.30        # probability of dropping a mushroom each step
FLEA_MIN_ZONE_MUSHROOMS = 5   # spawn flea when player zone has fewer than this

# ---------------------------------------------------------------------------
# Spider
# ---------------------------------------------------------------------------
SPIDER_STEPS = 8               # grid steps per second (diagonal)
SPIDER_SPAWN_INTERVAL = 480    # frames between spawn attempts (~8 sec)
SPIDER_SCORE_FAR = 300
SPIDER_SCORE_MID = 600
SPIDER_SCORE_CLOSE = 900
SPIDER_CLOSE_PX = 100          # pixel distance thresholds for score tiers
SPIDER_MID_PX = 200

# ---------------------------------------------------------------------------
# Scorpion
# ---------------------------------------------------------------------------
SCORPION_STEPS = 6             # grid steps per second
SCORPION_SPAWN_INTERVAL = 720  # frames between spawn attempts (~12 sec)
SCORPION_SCORE = 1000

# ---------------------------------------------------------------------------
# Mushroom field
# ---------------------------------------------------------------------------
MUSHROOM_COUNT = 30
MUSHROOM_HP = 4           # hits to destroy a mushroom
