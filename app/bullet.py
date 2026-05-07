"""Player bullet — travels straight up until it hits something."""

import pygame
from app import settings


class Bullet(pygame.sprite.Sprite):
    """A single bullet fired by the player."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(settings.YELLOW)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self) -> None:
        """Move bullet upward each frame; remove if it leaves the screen."""
        self.rect.y -= settings.BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()
