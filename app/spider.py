"""Spider enemy — bounces diagonally in the player zone, eats mushrooms."""

import random

import pygame
from app import settings
from app.sprite_loader import load_composite

SPIDER_COLOR = (150, 0, 200)

_ZONE_TOP = settings.ROWS - settings.PLAYER_ZONE_ROWS
_ZONE_BOT = settings.ROWS - 1


class Spider(pygame.sprite.Sprite):
    """
    Spawns on one side of the screen and moves diagonally within the player
    zone. Exits off the left or right edge when it wanders out of bounds.
    Score for a kill depends on how close it is to the player.
    """

    def __init__(self) -> None:
        super().__init__()
        side = random.choice([0, settings.COLS - 1])
        self.col = side
        self.row = _ZONE_TOP
        self._dx = 1 if side == 0 else -1   # moves toward the opposite edge
        self._dy = random.choice([-1, 1])

        self._step_interval = max(1, settings.FPS // settings.SPIDER_STEPS)
        self._step_timer = 0

        self.image = load_composite("spider", fallback_color=SPIDER_COLOR)
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
        self.row += self._dy

        # Exit screen from the sides
        if self.col < 0 or self.col >= settings.COLS:
            self.kill()
            return

        # Bounce off top and bottom of the player zone
        if self.row < _ZONE_TOP:
            self.row = _ZONE_TOP
            self._dy = 1
        elif self.row > _ZONE_BOT:
            self.row = _ZONE_BOT
            self._dy = -1

        # Occasional random vertical direction flip for erratic feel
        if random.random() < 0.15:
            self._dy *= -1

        self.rect.topleft = (self.col * settings.CELL_SIZE, self.row * settings.CELL_SIZE)

    def score_for_kill(self, player_rect: pygame.Rect) -> int:
        """Return 300 / 600 / 900 based on distance to the player."""
        dx = self.rect.centerx - player_rect.centerx
        dy = self.rect.centery - player_rect.centery
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < settings.SPIDER_CLOSE_PX:
            return settings.SPIDER_SCORE_CLOSE
        if dist < settings.SPIDER_MID_PX:
            return settings.SPIDER_SCORE_MID
        return settings.SPIDER_SCORE_FAR
