"""Scorpion enemy — crosses the screen horizontally, poisoning mushrooms."""

import random

import pygame
from app import settings
from app.sprite_loader import load_composite

SCORPION_COLOR = (200, 130, 0)


class Scorpion(pygame.sprite.Sprite):
    """
    Spawns off one edge of the screen and moves straight across.
    Any mushroom it overlaps is poisoned — a centipede touching a poisoned
    mushroom enters frenzy mode (dives straight down).
    """

    def __init__(self) -> None:
        super().__init__()
        # Spawn off-screen on a random side; pick a row in the mushroom field
        side = random.choice([-1, settings.COLS])   # -1 = off left, COLS = off right
        self.col = side
        self._dx = 1 if side < 0 else -1
        self.row = random.randint(2, settings.ROWS - settings.PLAYER_ZONE_ROWS - 1)

        self._step_interval = max(1, settings.FPS // settings.SCORPION_STEPS)
        self._step_timer = 0

        self.image = load_composite("scorpion", fallback_color=SCORPION_COLOR)
        self.rect = self.image.get_rect(
            topleft=(self.col * settings.CELL_SIZE, self.row * settings.CELL_SIZE)
        )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def update(self) -> None:  # type: ignore[override]
        self._step_timer += 1
        if self._step_timer < self._step_interval:
            return
        self._step_timer = 0

        self.col += self._dx
        self.rect.topleft = (self.col * settings.CELL_SIZE, self.row * settings.CELL_SIZE)

        # Exit when it has fully crossed the screen
        if self.col < 0 or self.col >= settings.COLS:
            self.kill()
