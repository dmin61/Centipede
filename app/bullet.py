"""Player bullet — travels straight up until it hits something."""

import pygame
from app import settings
from app.sprite_loader import load_single

_BULLET_SIZE = (8, 18)


class Bullet(pygame.sprite.Sprite):
    """A single bullet fired by the player."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        # bolt1.png is 48×32 landscape; rotate 90° to make it portrait (vertical bolt)
        self.image = load_single("bullet/bolt1.png", size=_BULLET_SIZE, rotate=90)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self) -> None:
        """Move bullet upward each frame; remove if it leaves the screen."""
        self.rect.y -= settings.BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()
