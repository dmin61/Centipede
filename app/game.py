"""Main game loop and state management."""

import asyncio
import random
from enum import Enum, auto

import pygame

from app import settings
from app.centipede import Centipede
from app.flea import Flea
from app.mushroom import Mushroom
from app.player import Player
from app.scorpion import Scorpion
from app.spider import Spider
from app.high_score import load_high_score, save_high_score
from app.screens import draw_game_over, draw_pause, draw_title, draw_win
from app.sound import SoundManager
from app.sprite_loader import load_single


# ---------------------------------------------------------------------------
# Game state
# ---------------------------------------------------------------------------

class GameState(Enum):
    TITLE = auto()        # pre-game title screen
    PLAYING = auto()
    PAUSED = auto()       # game frozen, overlay visible
    DEAD = auto()         # brief flash between death and respawn
    LEVEL_CLEAR = auto()  # brief pause between waves
    GAME_OVER = auto()
    WIN = auto()


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def build_mushroom_field() -> pygame.sprite.Group:
    """Scatter mushrooms randomly, avoiding the top two rows and player zone."""
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


# ---------------------------------------------------------------------------
# Game class
# ---------------------------------------------------------------------------

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
        self.font_large = pygame.font.SysFont("monospace", 48, bold=True)
        self._background = load_single(
            "background/stage-back.png",
            size=(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
            fallback_color=settings.BLACK,
        )
        self.sounds = SoundManager()
        self.high_score = load_high_score()
        self._new_record = False
        self._reset()

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _reset(self) -> None:
        """Full game restart — resets score, lives, level, and all objects."""
        self.score = 0
        self.lives = settings.PLAYER_LIVES
        self.level = 1
        self.state = GameState.TITLE
        self._timer = 0
        self._new_record = False
        self.mushrooms = build_mushroom_field()
        self._init_round()

    def _init_round(self) -> None:
        """Spawn player, centipede, and enemies for the current level. Mushrooms persist."""
        self.player = Player()
        self.centipede = Centipede(
            steps_per_second=self._centipede_steps(),
            start_row=self._centipede_start_row(),
        )
        self.bullets: pygame.sprite.Group = pygame.sprite.Group()
        self._shoot_cooldown = 0

        # Enemy slots — at most one of each active at a time.
        # _enemy_sprites is a sprite group that owns all live enemy sprites so
        # that sprite.alive() returns True while the enemy is active, and False
        # once the enemy calls self.kill() (e.g. walking off-screen).
        self._enemy_sprites: pygame.sprite.Group = pygame.sprite.Group()

        self.flea: Flea | None = None
        self._flea_cooldown = 0         # frames to wait before re-checking spawn

        self.spider: Spider | None = None
        self._spider_timer = 0          # counts toward SPIDER_SPAWN_INTERVAL

        self.scorpion: Scorpion | None = None
        self._scorpion_timer = 0        # counts toward SCORPION_SPAWN_INTERVAL

    # ------------------------------------------------------------------
    # Level helpers
    # ------------------------------------------------------------------

    def _centipede_steps(self) -> int:
        raw = settings.CENTIPEDE_BASE_STEPS + (self.level - 1) * settings.CENTIPEDE_STEPS_INCREMENT
        return min(raw, settings.CENTIPEDE_MAX_STEPS)

    def _centipede_start_row(self) -> int:
        raw = (self.level - 1) * settings.CENTIPEDE_START_ROW_INCREMENT
        return min(raw, settings.CENTIPEDE_MAX_START_ROW)

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    async def run(self) -> None:
        """Start and maintain the game loop until the window is closed."""
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(settings.FPS)
            await asyncio.sleep(0)

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == GameState.TITLE:
                    self.state = GameState.PLAYING
                elif event.key == pygame.K_p and self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
                elif event.key == pygame.K_p and self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING
                elif event.key == pygame.K_r and self.state in (
                    GameState.GAME_OVER, GameState.WIN
                ):
                    self._reset()   # returns to TITLE
                elif event.key == pygame.K_m:
                    self.sounds.toggle_mute()

    # ------------------------------------------------------------------
    # Update dispatch
    # ------------------------------------------------------------------

    def _update(self) -> None:
        if self.state == GameState.PLAYING:
            self._update_playing()
        elif self.state == GameState.DEAD:
            self._update_timed(settings.DEATH_FLASH_FRAMES, self._on_respawn)
        elif self.state == GameState.LEVEL_CLEAR:
            self._update_timed(settings.LEVEL_CLEAR_FRAMES, self._on_next_wave)
        # TITLE, PAUSED, GAME_OVER, WIN: nothing to update

    def _update_timed(self, duration: int, callback: object) -> None:
        """Generic countdown — calls callback when _timer reaches zero."""
        self._timer -= 1
        if self._timer <= 0:
            callback()  # type: ignore[operator]

    def _on_respawn(self) -> None:
        self._init_round()
        self.state = GameState.PLAYING

    def _on_next_wave(self) -> None:
        self.level += 1
        self._init_round()
        self.state = GameState.PLAYING

    # ------------------------------------------------------------------
    # Main play update
    # ------------------------------------------------------------------

    def _update_playing(self) -> None:
        # Player movement
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Shooting — one bullet on screen at a time
        if keys[pygame.K_SPACE] and self._shoot_cooldown == 0 and len(self.bullets) == 0:
            self.bullets.add(self.player.shoot())
            self._shoot_cooldown = 10
            self.sounds.play("shoot")
        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1
        self.bullets.update()

        # Bullet vs mushroom
        hits = pygame.sprite.groupcollide(self.bullets, self.mushrooms, True, False)
        for mushroom_list in hits.values():
            for mushroom in mushroom_list:
                mushroom.hit()
                self.score += 1
                self.sounds.play("hit_mushroom")

        # Bullet vs centipede segments
        for bullet in list(self.bullets):
            for seg in list(self.centipede.segments):
                if bullet.rect.colliderect(seg.rect):
                    bullet.kill()
                    self.centipede.remove_segment(seg)
                    self.score += 10
                    self.sounds.play("kill_segment")
                    break

        # Bullet vs classic enemies
        self._check_bullet_enemy_collisions()

        # Spawn and update enemies
        self._spawn_enemies()
        self._update_enemies()

        # Centipede movement (pass poisoned mushroom positions for frenzy logic)
        self.centipede.update(
            mushroom_index(self.mushrooms),
            self._poisoned_positions(),
        )

        # Centipede reaches player zone → lose a life
        player_zone_top = (settings.ROWS - settings.PLAYER_ZONE_ROWS) * settings.CELL_SIZE
        for seg in self.centipede.segments:
            if seg.rect.top >= player_zone_top:
                self._on_player_death()
                return

        # Any enemy touches the player → lose a life
        if self._player_hit_by_enemy():
            return

        # All centipede segments destroyed → wave cleared
        if self.centipede.is_defeated:
            self._on_centipede_cleared()

    # ------------------------------------------------------------------
    # Death / level clear
    # ------------------------------------------------------------------

    def _on_player_death(self) -> None:
        self.lives -= 1
        self.sounds.play("death")
        if self.lives <= 0:
            self._update_high_score()
            self.state = GameState.GAME_OVER
            self.sounds.play("game_over")
        else:
            self.state = GameState.DEAD
            self._timer = settings.DEATH_FLASH_FRAMES

    def _on_centipede_cleared(self) -> None:
        self.score += 100 * self.level
        if self.level >= settings.MAX_LEVEL:
            self._update_high_score()
            self.state = GameState.WIN
            self.sounds.play("win")
        else:
            self.state = GameState.LEVEL_CLEAR
            self._timer = settings.LEVEL_CLEAR_FRAMES
            self.sounds.play("level_clear")

    def _update_high_score(self) -> None:
        """Update self.high_score and persist to disk if current score beats it."""
        if self.score > self.high_score:
            self.high_score = self.score
            self._new_record = True
            save_high_score(self.high_score)
        else:
            self._new_record = False

    # ------------------------------------------------------------------
    # Enemy helpers
    # ------------------------------------------------------------------

    def _spawn_enemies(self) -> None:
        # Flea: appears when player zone runs low on mushrooms
        if self.flea is None:
            if self._flea_cooldown > 0:
                self._flea_cooldown -= 1
            else:
                zone_row_start = settings.ROWS - settings.PLAYER_ZONE_ROWS
                zone_count = sum(
                    1 for m in self.mushrooms
                    if m.row >= zone_row_start  # type: ignore[attr-defined]
                )
                if zone_count < settings.FLEA_MIN_ZONE_MUSHROOMS:
                    self.flea = Flea(col=random.randint(0, settings.COLS - 1))
                    self._enemy_sprites.add(self.flea)

        # Spider: timer-based
        self._spider_timer += 1
        if self.spider is None and self._spider_timer >= settings.SPIDER_SPAWN_INTERVAL:
            self._spider_timer = 0
            self.spider = Spider()
            self._enemy_sprites.add(self.spider)

        # Scorpion: timer-based
        self._scorpion_timer += 1
        if self.scorpion is None and self._scorpion_timer >= settings.SCORPION_SPAWN_INTERVAL:
            self._scorpion_timer = 0
            self.scorpion = Scorpion()
            self._enemy_sprites.add(self.scorpion)

    def _update_enemies(self) -> None:
        """Move enemies and apply their effects on the mushroom field."""
        occupied = {(m.col, m.row) for m in self.mushrooms}  # type: ignore[attr-defined]

        if self.flea is not None:
            drop_pos = self.flea.update()
            if drop_pos is not None and drop_pos not in occupied:
                self.mushrooms.add(Mushroom(*drop_pos))
                occupied.add(drop_pos)
            if not self.flea.alive():
                self._flea_cooldown = 120
                self.flea = None

        if self.spider is not None:
            self.spider.update()
            # Spider eats any mushroom it overlaps
            for m in list(self.mushrooms):
                if self.spider.alive() and self.spider.rect.colliderect(m.rect):
                    m.kill()
            if not self.spider.alive():
                self.spider = None
                self._spider_timer = 0  # give full interval before next spawn

        if self.scorpion is not None:
            self.scorpion.update()
            # Scorpion poisons any mushroom it overlaps
            for m in self.mushrooms:
                if (
                    self.scorpion.alive()
                    and not m.is_poisoned  # type: ignore[attr-defined]
                    and self.scorpion.rect.colliderect(m.rect)
                ):
                    m.poison()  # type: ignore[attr-defined]
            if not self.scorpion.alive():
                self.scorpion = None
                self._scorpion_timer = 0  # give full interval before next spawn

    def _check_bullet_enemy_collisions(self) -> None:
        """One bullet can only kill one enemy per frame."""
        for bullet in list(self.bullets):
            if self.flea is not None and bullet.rect.colliderect(self.flea.rect):
                bullet.kill()
                if self.flea.hit():
                    self.score += settings.FLEA_SCORE
                    self.flea = None
                self.sounds.play("kill_enemy")
                continue

            if self.spider is not None and bullet.rect.colliderect(self.spider.rect):
                bullet.kill()
                self.score += self.spider.score_for_kill(self.player.rect)
                self.spider.kill()
                self.spider = None
                self.sounds.play("kill_enemy")
                continue

            if self.scorpion is not None and bullet.rect.colliderect(self.scorpion.rect):
                bullet.kill()
                self.score += settings.SCORPION_SCORE
                self.scorpion.kill()
                self.scorpion = None
                self.sounds.play("kill_enemy")
                continue

    def _player_hit_by_enemy(self) -> bool:
        """Return True and trigger death if any enemy touches the player."""
        for enemy in (self.flea, self.spider, self.scorpion):
            if enemy is not None and self.player.rect.colliderect(enemy.rect):
                self._on_player_death()
                return True
        return False

    def _poisoned_positions(self) -> set[tuple[int, int]]:
        return {
            (m.col, m.row)  # type: ignore[attr-defined]
            for m in self.mushrooms
            if m.is_poisoned  # type: ignore[attr-defined]
        }

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def _draw(self) -> None:
        if self.state == GameState.TITLE:
            draw_title(self.screen, self._background, self.font_large, self.font, self.high_score)
        elif self.state == GameState.DEAD:
            self._draw_death_flash()
        elif self.state == GameState.GAME_OVER:
            draw_game_over(
                self.screen, self._background, self.font_large, self.font,
                self.score, self.high_score, self._new_record,
            )
        elif self.state == GameState.WIN:
            draw_win(
                self.screen, self._background, self.font_large, self.font,
                self.score, self.high_score, self._new_record,
            )
        elif self.state == GameState.PAUSED:
            self._draw_game()
            draw_pause(self.screen, self.font_large, self.font)
        else:
            self._draw_game()
        pygame.display.flip()

    def _draw_game(self) -> None:
        self.screen.blit(self._background, (0, 0))
        self.mushrooms.draw(self.screen)
        self.centipede.all_sprites.draw(self.screen)
        self.bullets.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)

        for enemy in (self.flea, self.spider, self.scorpion):
            if enemy is not None:
                self.screen.blit(enemy.image, enemy.rect)

        self._draw_hud()

        if self.state == GameState.LEVEL_CLEAR:
            self._draw_overlay(f"LEVEL {self.level} CLEAR!", settings.YELLOW)

    def _draw_death_flash(self) -> None:
        color = settings.RED if (self._timer // 10) % 2 == 0 else settings.BLACK
        self.screen.fill(color)
        self._draw_hud()

    def _draw_hud(self) -> None:
        score_surf = self.font.render(f"SCORE: {self.score}", True, settings.WHITE)
        self.screen.blit(score_surf, (10, 10))

        level_surf = self.font.render(f"LEVEL {self.level}", True, settings.WHITE)
        self.screen.blit(
            level_surf,
            (settings.SCREEN_WIDTH // 2 - level_surf.get_width() // 2, 10),
        )

        lives_surf = self.font.render(f"LIVES: {self.lives}", True, settings.WHITE)
        self.screen.blit(
            lives_surf,
            (settings.SCREEN_WIDTH - lives_surf.get_width() - 10, 10),
        )

        if self.sounds.muted:
            mute_surf = self.font.render("MUTE", True, settings.YELLOW)
            self.screen.blit(mute_surf, (10, settings.SCREEN_HEIGHT - 30))

    def _draw_overlay(self, message: str, color: tuple[int, int, int]) -> None:
        surf = self.font.render(message, True, color)
        self.screen.blit(
            surf,
            (settings.SCREEN_WIDTH // 2 - surf.get_width() // 2,
             settings.SCREEN_HEIGHT // 2),
        )
