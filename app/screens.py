"""
Full-screen and overlay drawing routines.
Each function takes the surface(s) and font(s) it needs — no game state.
"""

import pygame
from app import settings

_CX = settings.SCREEN_WIDTH // 2
_CY = settings.SCREEN_HEIGHT // 2


def _centered(surf: pygame.Surface, y: int) -> tuple[int, int]:
    return (_CX - surf.get_width() // 2, y)


def _dark_overlay(screen: pygame.Surface, alpha: int = 170) -> None:
    overlay = pygame.Surface(
        (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA
    )
    overlay.fill((0, 0, 0, alpha))
    screen.blit(overlay, (0, 0))


def _blink_visible() -> bool:
    """True for the first half of every 700 ms — used for flashing prompts."""
    return (pygame.time.get_ticks() // 700) % 2 == 0


# ---------------------------------------------------------------------------
# Title screen
# ---------------------------------------------------------------------------

def draw_title(
    screen: pygame.Surface,
    background: pygame.Surface,
    font_large: pygame.font.Font,
    font: pygame.font.Font,
    high_score: int = 0,
) -> None:
    """Starting screen shown before the first game begins."""
    screen.blit(background, (0, 0))
    _dark_overlay(screen, alpha=120)

    title = font_large.render("CENTIPEDE", True, settings.GREEN)
    screen.blit(title, _centered(title, _CY - 160))

    pygame.draw.line(
        screen, settings.GREEN,
        (_CX - 160, _CY - 75), (_CX + 160, _CY - 75), 2
    )

    hs_color = settings.YELLOW if high_score > 0 else (100, 100, 100)
    hs_surf = font.render(f"HIGH SCORE:  {high_score}", True, hs_color)
    screen.blit(hs_surf, _centered(hs_surf, _CY - 45))

    if _blink_visible():
        prompt = font.render("PRESS SPACE TO START", True, settings.WHITE)
        screen.blit(prompt, _centered(prompt, _CY + 20))

    hint1 = font.render("ARROWS  move  |  SPACE  fire", True, (130, 130, 130))
    hint2 = font.render("P  pause  |  M  mute", True, (130, 130, 130))
    screen.blit(hint1, _centered(hint1, settings.SCREEN_HEIGHT - 70))
    screen.blit(hint2, _centered(hint2, settings.SCREEN_HEIGHT - 44))


# ---------------------------------------------------------------------------
# Pause overlay
# ---------------------------------------------------------------------------

def draw_pause(
    screen: pygame.Surface,
    font_large: pygame.font.Font,
    font: pygame.font.Font,
) -> None:
    """Semi-transparent overlay drawn on top of the frozen game frame."""
    _dark_overlay(screen, alpha=160)

    paused = font_large.render("PAUSED", True, settings.WHITE)
    screen.blit(paused, _centered(paused, _CY - 50))

    if _blink_visible():
        resume = font.render("P  to resume", True, settings.WHITE)
        screen.blit(resume, _centered(resume, _CY + 20))


# ---------------------------------------------------------------------------
# Game Over screen
# ---------------------------------------------------------------------------

def draw_game_over(
    screen: pygame.Surface,
    background: pygame.Surface,
    font_large: pygame.font.Font,
    font: pygame.font.Font,
    score: int,
    high_score: int = 0,
    new_record: bool = False,
) -> None:
    """Full game-over screen with final score and best score."""
    screen.blit(background, (0, 0))
    _dark_overlay(screen, alpha=190)

    title = font_large.render("GAME  OVER", True, settings.RED)
    screen.blit(title, _centered(title, _CY - 140))

    pygame.draw.line(
        screen, settings.RED,
        (_CX - 180, _CY - 60), (_CX + 180, _CY - 60), 2
    )

    if new_record:
        record_surf = font.render("NEW  HIGH  SCORE!", True, settings.YELLOW)
        screen.blit(record_surf, _centered(record_surf, _CY - 30))
        score_surf = font.render(f"{score}", True, settings.YELLOW)
        screen.blit(score_surf, _centered(score_surf, _CY + 10))
    else:
        score_surf = font.render(f"SCORE:  {score}", True, settings.WHITE)
        screen.blit(score_surf, _centered(score_surf, _CY - 30))
        best_surf = font.render(f"BEST:   {high_score}", True, (160, 160, 160))
        screen.blit(best_surf, _centered(best_surf, _CY + 10))

    if _blink_visible():
        restart = font.render("R  to restart", True, settings.YELLOW)
        screen.blit(restart, _centered(restart, _CY + 70))


# ---------------------------------------------------------------------------
# Win screen
# ---------------------------------------------------------------------------

def draw_win(
    screen: pygame.Surface,
    background: pygame.Surface,
    font_large: pygame.font.Font,
    font: pygame.font.Font,
    score: int,
    high_score: int = 0,
    new_record: bool = False,
) -> None:
    """Full win screen shown after clearing all levels."""
    screen.blit(background, (0, 0))
    _dark_overlay(screen, alpha=160)

    title = font_large.render("YOU  WIN!", True, settings.GREEN)
    screen.blit(title, _centered(title, _CY - 150))

    pygame.draw.line(
        screen, settings.GREEN,
        (_CX - 160, _CY - 65), (_CX + 160, _CY - 65), 2
    )

    cleared = font.render("ALL 10 LEVELS CLEARED", True, settings.GREEN)
    screen.blit(cleared, _centered(cleared, _CY - 35))

    score_color = settings.YELLOW if new_record else settings.WHITE
    score_surf = font.render(f"FINAL SCORE:  {score}", True, score_color)
    screen.blit(score_surf, _centered(score_surf, _CY + 5))

    if new_record:
        record_surf = font.render("NEW  HIGH  SCORE!", True, settings.YELLOW)
        screen.blit(record_surf, _centered(record_surf, _CY + 35))
    else:
        best_surf = font.render(f"BEST:         {high_score}", True, (160, 160, 160))
        screen.blit(best_surf, _centered(best_surf, _CY + 35))

    if _blink_visible():
        restart = font.render("R  to restart", True, settings.YELLOW)
        screen.blit(restart, _centered(restart, _CY + 90))
