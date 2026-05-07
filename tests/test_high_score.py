"""Tests for high score load/save and game integration."""

from pathlib import Path

import pygame
import pytest

from app import settings
from app.game import Game, GameState
from app.high_score import load_high_score, save_high_score


# ---------------------------------------------------------------------------
# Pure persistence tests (use tmp_path to avoid touching real data/)
# ---------------------------------------------------------------------------

def test_load_returns_zero_when_file_missing(tmp_path: Path) -> None:
    assert load_high_score(tmp_path / "hs.txt") == 0


def test_load_returns_zero_for_corrupt_file(tmp_path: Path) -> None:
    p = tmp_path / "hs.txt"
    p.write_text("not-a-number")
    assert load_high_score(p) == 0


def test_load_returns_zero_for_empty_file(tmp_path: Path) -> None:
    p = tmp_path / "hs.txt"
    p.write_text("")
    assert load_high_score(p) == 0


def test_save_creates_file(tmp_path: Path) -> None:
    p = tmp_path / "hs.txt"
    save_high_score(9999, p)
    assert p.exists()


def test_save_creates_parent_directory(tmp_path: Path) -> None:
    p = tmp_path / "nested" / "dir" / "hs.txt"
    save_high_score(42, p)
    assert p.exists()


def test_round_trip(tmp_path: Path) -> None:
    p = tmp_path / "hs.txt"
    save_high_score(12345, p)
    assert load_high_score(p) == 12345


def test_save_overwrites_previous(tmp_path: Path) -> None:
    p = tmp_path / "hs.txt"
    save_high_score(100, p)
    save_high_score(200, p)
    assert load_high_score(p) == 200


# ---------------------------------------------------------------------------
# Game integration tests
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


def test_game_loads_high_score_at_init(game: Game) -> None:
    assert isinstance(game.high_score, int)
    assert game.high_score >= 0


def test_new_record_false_at_start(game: Game) -> None:
    assert not game._new_record


def test_update_high_score_sets_new_record(game: Game) -> None:
    game.high_score = 0
    game.score = 500
    game._update_high_score()
    assert game._new_record
    assert game.high_score == 500


def test_update_high_score_no_record_when_lower(game: Game) -> None:
    game.high_score = 1000
    game.score = 500
    game._update_high_score()
    assert not game._new_record
    assert game.high_score == 1000


def test_update_high_score_no_record_when_equal(game: Game) -> None:
    game.high_score = 500
    game.score = 500
    game._update_high_score()
    assert not game._new_record
    assert game.high_score == 500


def test_game_over_triggers_high_score_update(game: Game) -> None:
    game.high_score = 0
    game.score = 999
    game.lives = 1
    game._on_player_death()
    assert game.state == GameState.GAME_OVER
    assert game.high_score == 999
    assert game._new_record


def test_reset_clears_new_record_flag(game: Game) -> None:
    game._new_record = True
    game._reset()
    assert not game._new_record


def test_high_score_persists_across_reset(game: Game) -> None:
    game.high_score = 5000
    game._reset()
    assert game.high_score == 5000
