"""Tests for UI screens and GameState transitions (title, pause, game over, win)."""

import pygame
import pytest

from app import settings
from app.game import Game, GameState
from app.screens import draw_game_over, draw_pause, draw_title, draw_win


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def init_pygame(monkeypatch: pytest.MonkeyPatch) -> pytest.Generator[None, None, None]:
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")
    pygame.init()
    pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    yield
    pygame.quit()


@pytest.fixture
def game() -> Game:
    return Game()


@pytest.fixture
def screen() -> pygame.Surface:
    return pygame.display.get_surface()


@pytest.fixture
def fonts() -> tuple[pygame.font.Font, pygame.font.Font]:
    large = pygame.font.SysFont("monospace", 48, bold=True)
    small = pygame.font.SysFont("monospace", 20, bold=True)
    return large, small


@pytest.fixture
def background() -> pygame.Surface:
    surf = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    surf.fill(settings.BLACK)
    return surf


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------

def test_game_starts_at_title(game: Game) -> None:
    assert game.state == GameState.TITLE


def test_reset_returns_to_title(game: Game) -> None:
    game.state = GameState.GAME_OVER
    game._reset()
    assert game.state == GameState.TITLE


# ---------------------------------------------------------------------------
# TITLE → PLAYING
# ---------------------------------------------------------------------------

def test_space_on_title_starts_game(game: Game) -> None:
    assert game.state == GameState.TITLE
    # Simulate SPACE keydown
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
    pygame.event.post(event)
    game._handle_events()
    assert game.state == GameState.PLAYING


def test_other_keys_do_not_start_game(game: Game) -> None:
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode="")
    pygame.event.post(event)
    game._handle_events()
    assert game.state == GameState.TITLE


# ---------------------------------------------------------------------------
# PLAYING ↔ PAUSED
# ---------------------------------------------------------------------------

def test_p_key_pauses_game(game: Game) -> None:
    game.state = GameState.PLAYING
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p, mod=0, unicode="p")
    pygame.event.post(event)
    game._handle_events()
    assert game.state == GameState.PAUSED


def test_p_key_resumes_from_pause(game: Game) -> None:
    game.state = GameState.PAUSED
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p, mod=0, unicode="p")
    pygame.event.post(event)
    game._handle_events()
    assert game.state == GameState.PLAYING


def test_paused_game_does_not_update(game: Game) -> None:
    game.state = GameState.PAUSED
    score_before = game.score
    game._update()
    assert game.score == score_before  # nothing changed


def test_title_game_does_not_update(game: Game) -> None:
    game.state = GameState.TITLE
    score_before = game.score
    game._update()
    assert game.score == score_before


# ---------------------------------------------------------------------------
# Screen drawing functions do not raise
# ---------------------------------------------------------------------------

def test_draw_title_does_not_raise(
    screen: pygame.Surface,
    background: pygame.Surface,
    fonts: tuple[pygame.font.Font, pygame.font.Font],
) -> None:
    large, small = fonts
    draw_title(screen, background, large, small)


def test_draw_pause_does_not_raise(
    screen: pygame.Surface,
    fonts: tuple[pygame.font.Font, pygame.font.Font],
) -> None:
    large, small = fonts
    draw_pause(screen, large, small)


def test_draw_game_over_does_not_raise(
    screen: pygame.Surface,
    background: pygame.Surface,
    fonts: tuple[pygame.font.Font, pygame.font.Font],
) -> None:
    large, small = fonts
    draw_game_over(screen, background, large, small, score=1234)


def test_draw_win_does_not_raise(
    screen: pygame.Surface,
    background: pygame.Surface,
    fonts: tuple[pygame.font.Font, pygame.font.Font],
) -> None:
    large, small = fonts
    draw_win(screen, background, large, small, score=9999)
