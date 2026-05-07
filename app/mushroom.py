"""Mushroom obstacle — takes multiple hits to destroy."""

import pygame
from app import settings
from app.sprite_loader import load_composite


class Mushroom(pygame.sprite.Sprite):
    """A single mushroom on the grid."""

    def __init__(self, col: int, row: int) -> None:
        super().__init__()
        self.col = col
        self.row = row
        self.hp = settings.MUSHROOM_HP
        self.is_poisoned = False

        # Load once; _draw() copies this and applies tinting per frame
        self._base_sprite = load_composite("mushroom", glob_pattern="0__*.png")

        self.image = self._base_sprite.copy()
        self.rect = self.image.get_rect(
            topleft=(col * settings.CELL_SIZE, row * settings.CELL_SIZE)
        )
        self._draw()

    def _draw(self) -> None:
        """Regenerate self.image with current damage and poison state."""
        self.image = self._base_sprite.copy()

        # Darken as HP falls: 0 damage → no overlay; near death → heavy black overlay
        damage_ratio = 1 - (self.hp / settings.MUSHROOM_HP)
        damage_alpha = int(180 * damage_ratio)
        if damage_alpha > 0:
            overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, damage_alpha))
            self.image.blit(overlay, (0, 0))

        if self.is_poisoned:
            poison_overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            poison_overlay.fill((180, 0, 180, 110))
            self.image.blit(poison_overlay, (0, 0))

    def hit(self) -> bool:
        """
        Apply one bullet hit.
        Returns True if the mushroom is destroyed.
        """
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
            return True
        self._draw()
        return False

    def poison(self) -> None:
        """Mark this mushroom as poisoned; centipede frenzies on contact."""
        self.is_poisoned = True
        self._draw()
