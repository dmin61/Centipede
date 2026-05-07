"""Tests for multi-wave level progression."""

import pygame
import pytest

from app import settings
from app.game import Game, GameState
from app.centipede import Centipede


@pytest.fixture(autouse=True)
def init_pygame() -> None:
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def game(monkeypatch: pytest.MonkeyPatch) -> Game:
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")
    pygame.display.init()
    return Game()


# ------------------------------------------------------------------
# Centipede speed scaling
# ------------------------------------------------------------------

def test_centipede_steps_increase_per_level(game: Game) -> None:
    level1_steps = game._centipede_steps()
    game.level = 2
    assert game._centipede_steps() > level1_steps


def test_centipede_steps_capped_at_max(game: Game) -> None:
    game.level = 999
    assert game._centipede_steps() == settings.CENTIPEDE_MAX_STEPS


def test_centipede_start_row_increases_per_level(game: Game) -> None:
    game.level = 1
    row1 = game._centipede_start_row()
    game.level = 2
    assert game._centipede_start_row() > row1


def test_centipede_start_row_capped_at_max(game: Game) -> None:
    game.level = 999
    assert game._centipede_start_row() == settings.CENTIPEDE_MAX_START_ROW


# ------------------------------------------------------------------
# Wave clear transitions
# ------------------------------------------------------------------

def test_clearing_centipede_enters_level_clear_state(game: Game) -> None:
    game._on_centipede_cleared()
    assert game.state == GameState.LEVEL_CLEAR


def test_clearing_centipede_sets_timer(game: Game) -> None:
    game._on_centipede_cleared()
    assert game._timer == settings.LEVEL_CLEAR_FRAMES


def test_level_clear_advances_level(game: Game) -> None:
    game._on_centipede_cleared()
    game._timer = 1
    game._update_timed(settings.LEVEL_CLEAR_FRAMES, game._on_next_wave)
    assert game.level == 2
    assert game.state == GameState.PLAYING


def test_clearing_max_level_triggers_win(game: Game) -> None:
    game.level = settings.MAX_LEVEL
    game._on_centipede_cleared()
    assert game.state == GameState.WIN


# ------------------------------------------------------------------
# Centipede step-rate timer
# ------------------------------------------------------------------

def test_centipede_does_not_move_before_interval(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    pygame.display.init()
    c = Centipede(steps_per_second=1)  # 1 step/sec → moves every 60 frames
    initial_col = c.segments[0].col
    c.update({})  # one frame — should not move yet
    assert c.segments[0].col == initial_col


def test_centipede_moves_after_interval(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    pygame.display.init()
    c = Centipede(steps_per_second=settings.FPS)  # 60 steps/sec → moves every frame
    initial_col = c.segments[0].col
    c.update({})
    assert c.segments[0].col != initial_col
