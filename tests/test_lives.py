"""Tests for the lives system and GameState transitions."""

import pygame
import pytest

from app import settings
from app.game import Game, GameState


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


def test_starts_with_full_lives(game: Game) -> None:
    assert game.lives == settings.PLAYER_LIVES


def test_starts_at_level_1(game: Game) -> None:
    assert game.level == 1


def test_starts_in_title_state(game: Game) -> None:
    assert game.state == GameState.TITLE


def test_death_deducts_a_life(game: Game) -> None:
    game._on_player_death()
    assert game.lives == settings.PLAYER_LIVES - 1


def test_death_enters_dead_state_when_lives_remain(game: Game) -> None:
    game._on_player_death()
    assert game.state == GameState.DEAD


def test_death_timer_set_on_death(game: Game) -> None:
    game._on_player_death()
    assert game._timer == settings.DEATH_FLASH_FRAMES


def test_last_life_triggers_game_over(game: Game) -> None:
    game.lives = 1
    game._on_player_death()
    assert game.state == GameState.GAME_OVER
    assert game.lives == 0


def test_dead_state_counts_down_and_respawns(game: Game) -> None:
    game._on_player_death()
    game._timer = 1
    game._update_timed(settings.DEATH_FLASH_FRAMES, game._on_respawn)
    assert game.state == GameState.PLAYING


def test_reset_restores_full_lives(game: Game) -> None:
    game.lives = 0
    game.state = GameState.GAME_OVER
    game._reset()
    assert game.lives == settings.PLAYER_LIVES
    assert game.state == GameState.TITLE
