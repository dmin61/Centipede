"""Main game loop and state management."""

import random
import pygame
from app import settings
from app.player import Player
from app.bullet import Bullet
from app.centipede import Centipede
from app.mushroom import Mushroom


def build_mushroom_field() -> pygame.sprite.Group:
    """
    Scatter mushrooms randomly, avoiding the top two rows and player zone.
    Returns a sprite group of Mushroom objects.
    """
    group: pygame.sprite.Group = pygame.sprite.Group()
    occupied: set[tuple[int, int]] = set()
    player_zone_start = settings.ROWS - settings.PLAYER_ZONE_ROWS

    while len(occupied) < settings.MUSHROOM_COUNT:
        col = random.randint(0, settings.COLS - 1)
        row = random.randint(2, player_zone_start - 1)
        if (col, row) not in occupied:
            occupied.add((col, row))
            group.add(Mushroom(col, row))

    return group


def mushroom_index(mushrooms: pygame.sprite.Group) -> dict[int, set[int]]:
    """Build a row → set-of-cols lookup for fast centipede collision checks."""
    index: dict[int, set[int]] = {}
    for m in mushrooms:
        index.setdefault(m.row, set()).add(m.col)  # type: ignore[attr-defined]
    return index


class Game:
    """Owns the pygame window, clock, and all game objects."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20, bold=True)

        self._reset()

    def _reset(self) -> None:
        """Initialize / restart all game objects."""
        self.score = 0
        self.player = Player()
        self.mushrooms = build_mushroom_field()
        self.centipede = Centipede()
        self.bullets: pygame.sprite.Group = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group(
            self.mushrooms,
            *self.centipede.all_sprites,
            self.player,
        )

        self._shoot_cooldown = 0  # frames remaining before next shot allowed
        self._game_over = False
        self._won = False

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start and maintain the game loop until the window is closed."""
        while True:
            self._handle_events()
            if not self._game_over:
                self._update()
            self._draw()
            self.clock.tick(settings.FPS)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self._game_over:
                    self._reset()

    def _update(self) -> None:
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Shooting — one bullet on screen at a time, with cooldown
        if keys[pygame.K_SPACE] and self._shoot_cooldown == 0 and len(self.bullets) == 0:
            bullet = self.player.shoot()
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            self._shoot_cooldown = 10  # frames

        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1

        self.bullets.update()

        # Bullet vs mushroom
        hits = pygame.sprite.groupcollide(self.bullets, self.mushrooms, True, False)
        for mushroom_list in hits.values():
            for mushroom in mushroom_list:
                mushroom.hit()
                self.score += 1

        # Bullet vs centipede
        for bullet in list(self.bullets):
            for seg in list(self.centipede.segments):
                if bullet.rect.colliderect(seg.rect):
                    bullet.kill()
                    self.bullets.remove(bullet)
                    self.centipede.remove_segment(seg)
                    self.score += 10
                    break

        # Centipede movement
        m_index = mushroom_index(self.mushrooms)
        self.centipede.update(m_index)

        # Centipede reaches player zone → game over
        player_zone_top = (settings.ROWS - settings.PLAYER_ZONE_ROWS) * settings.CELL_SIZE
        for seg in self.centipede.segments:
            if seg.rect.top >= player_zone_top:
                self._game_over = True
                return

        if self.centipede.is_defeated:
            self._game_over = True
            self._won = True

    def _draw(self) -> None:
        self.screen.fill(settings.BLACK)
        self.mushrooms.draw(self.screen)
        self.centipede.all_sprites.draw(self.screen)
        self.bullets.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)

        score_surf = self.font.render(f"SCORE: {self.score}", True, settings.WHITE)
        self.screen.blit(score_surf, (10, 10))

        if self._game_over:
            msg = "YOU WIN!" if self._won else "GAME OVER"
            color = settings.GREEN if self._won else settings.RED
            over_surf = self.font.render(f"{msg}  |  R to restart", True, color)
            self.screen.blit(
                over_surf,
                (settings.SCREEN_WIDTH // 2 - over_surf.get_width() // 2,
                 settings.SCREEN_HEIGHT // 2),
            )

        pygame.display.flip()
