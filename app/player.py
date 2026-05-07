"""Player-controlled gun at the bottom of the screen."""

import pygame
from app import settings
from app.bullet import Bullet


class Player(pygame.sprite.Sprite):
    """The player's shooter. Moves in a restricted zone near the bottom."""

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((settings.CELL_SIZE, settings.CELL_SIZE))
        self.image.fill(settings.GREEN)
        start_x = (settings.COLS // 2) * settings.CELL_SIZE
        start_y = (settings.ROWS - 2) * settings.CELL_SIZE
        self.rect = self.image.get_rect(topleft=(start_x, start_y))

        # vertical boundary of the player zone
        self._zone_top = (settings.ROWS - settings.PLAYER_ZONE_ROWS) * settings.CELL_SIZE

    def update(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Move the player based on held keys, clamped to the player zone."""
        if keys[pygame.K_LEFT]:
            self.rect.x -= settings.PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += settings.PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= settings.PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += settings.PLAYER_SPEED

        self.rect.clamp_ip(
            pygame.Rect(
                0,
                self._zone_top,
                settings.SCREEN_WIDTH - settings.CELL_SIZE,
                settings.SCREEN_HEIGHT - settings.CELL_SIZE,
            )
        )

    def shoot(self) -> Bullet:
        """Create and return a bullet fired from the player's current position."""
        return Bullet(self.rect.centerx, self.rect.top)
