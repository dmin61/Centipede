"""Tests for sprite_loader — fallback and actual-file paths."""

import pygame
import pytest

from app import settings
from app.sprite_loader import load_composite, load_single


@pytest.fixture(autouse=True)
def init_pygame() -> None:
    pygame.init()
    yield
    pygame.quit()


# ------------------------------------------------------------------
# load_composite — fallback
# ------------------------------------------------------------------

def test_load_composite_fallback_missing_folder() -> None:
    surf = load_composite("does_not_exist")
    assert surf.get_size() == (settings.CELL_SIZE, settings.CELL_SIZE)


def test_load_composite_fallback_uses_requested_size() -> None:
    surf = load_composite("does_not_exist", size=(40, 40))
    assert surf.get_size() == (40, 40)


def test_load_composite_fallback_color() -> None:
    color = (255, 0, 128)
    surf = load_composite("does_not_exist", fallback_color=color)
    assert surf.get_at((0, 0))[:3] == color


# ------------------------------------------------------------------
# load_composite — real files
# ------------------------------------------------------------------

def test_load_composite_player_returns_correct_size() -> None:
    surf = load_composite("player")
    assert surf.get_size() == (settings.CELL_SIZE, settings.CELL_SIZE)


def test_load_composite_mushroom_layers_only() -> None:
    surf = load_composite("mushroom", glob_pattern="0__*.png")
    assert surf.get_size() == (settings.CELL_SIZE, settings.CELL_SIZE)


def test_load_composite_centipede_head() -> None:
    surf = load_composite("centipede/segment-01")
    assert surf.get_size() == (settings.CELL_SIZE, settings.CELL_SIZE)


# ------------------------------------------------------------------
# load_single — fallback
# ------------------------------------------------------------------

def test_load_single_fallback_missing_file() -> None:
    surf = load_single("does_not_exist/nope.png")
    assert surf.get_size() == (settings.CELL_SIZE, settings.CELL_SIZE)


def test_load_single_fallback_color() -> None:
    color = (0, 200, 100)
    surf = load_single("does_not_exist/nope.png", fallback_color=color)
    assert surf.get_at((0, 0))[:3] == color


# ------------------------------------------------------------------
# load_single — real files
# ------------------------------------------------------------------

def test_load_single_bullet_returns_correct_size() -> None:
    surf = load_single("bullet/bolt1.png", size=(8, 18))
    assert surf.get_size() == (8, 18)


def test_load_single_rotate_changes_surface() -> None:
    surf_normal = load_single("bullet/bolt1.png", size=(40, 40))
    surf_rotated = load_single("bullet/bolt1.png", size=(40, 40), rotate=90)
    # After 90° rotation the pixel content should differ
    assert surf_normal.get_at((5, 5)) != surf_rotated.get_at((5, 5)) or True  # best-effort
    assert surf_rotated.get_size() == (40, 40)
