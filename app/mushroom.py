"""Mushroom obstacle — takes multiple hits to destroy."""

import pygame
from app import settings


class Mushroom(pygame.sprite.Sprite):
    """A single mushroom on the grid."""

    def __init__(self, col: int, row: int) -> None:
        super().__init__()
        self.col = col
        self.row = row
        self.hp = settings.MUSHROOM_HP
        self.image = pygame.Surface((settings.CELL_SIZE, settings.CELL_SIZE))
        self.rect = self.image.get_rect(
            topleft=(col * settings.CELL_SIZE, row * settings.CELL_SIZE)
        )
        self._draw()

    def _draw(self) -> None:
        """Redraw the mushroom to reflect current HP (color fades as damaged)."""
        ratio = self.hp / settings.MUSHROOM_HP
        r = int(settings.BROWN[0] * ratio)
        g = int(settings.BROWN[1] * ratio)
        b = int(settings.BROWN[2] * ratio)
        self.image.fill((r, g, b))

    def hit(self) -> bool:
        """
        Apply one hit to this mushroom.
        Returns True if the mushroom is destroyed.
        """
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
            return True
        self._draw()
        return False
