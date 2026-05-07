"""Flea enemy — drops straight down, planting mushrooms as it falls."""

import random

import pygame
from app import settings
from app.sprite_loader import load_composite

FLEA_COLOR = (220, 220, 50)
FLEA_HIT_COLOR = (180, 180, 30)  # dimmer after first hit


class Flea(pygame.sprite.Sprite):
    """
    Spawns at the top of the screen and falls straight down.
    Requires two hits to destroy.
    Occasionally plants a mushroom at its current position.
    """

    def __init__(self, col: int) -> None:
        super().__init__()
        self.col = col
        self.row = 0
        self.hp = settings.FLEA_HP

        self._step_interval = max(1, settings.FPS // settings.FLEA_STEPS)
        self._step_timer = 0

        self.image = load_composite("flea", fallback_color=FLEA_COLOR)
        self.rect = self.image.get_rect(
            topleft=(col * settings.CELL_SIZE, 0)
        )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def update(self) -> tuple[int, int] | None:  # type: ignore[override]
        """
        Move down one grid row when the step timer fires.

        Returns:
            (col, row) where a mushroom should be planted, or None.
            The caller is responsible for checking whether the cell is empty.
        """
        self._step_timer += 1
        if self._step_timer < self._step_interval:
            return None
        self._step_timer = 0

        self.row += 1
        self.rect.topleft = (self.col * settings.CELL_SIZE, self.row * settings.CELL_SIZE)

        if self.row >= settings.ROWS:
            self.kill()
            return None

        if random.random() < settings.FLEA_DROP_CHANCE:
            return (self.col, self.row)
        return None

    def hit(self) -> bool:
        """
        Apply one bullet hit.
        Returns True if the flea is destroyed.
        """
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
            return True
        self.image.fill(FLEA_HIT_COLOR)  # dim the rect (no art file yet for hit state)
        return False
