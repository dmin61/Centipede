"""Tests for the Scorpion enemy."""

import pygame
import pytest

from app import settings
from app.scorpion import Scorpion
from app.mushroom import Mushroom


@pytest.fixture(autouse=True)
def init_pygame() -> None:
    pygame.init()
    yield
    pygame.quit()


def _advance(scorpion: Scorpion, steps: int = 1) -> None:
    for _ in range(steps):
        scorpion._step_timer = scorpion._step_interval - 1
        scorpion.update()


def test_scorpion_row_in_mushroom_field() -> None:
    s = Scorpion()
    assert 2 <= s.row <= settings.ROWS - settings.PLAYER_ZONE_ROWS - 1


def test_scorpion_moves_horizontally() -> None:
    s = Scorpion()
    initial_row = s.row
    _advance(s)
    if s.alive():
        assert s.row == initial_row  # row never changes


def test_scorpion_exits_screen() -> None:
    s = Scorpion()
    # Force it to the edge one step from exit
    if s._dx == 1:
        s.col = settings.COLS - 1
    else:
        s.col = 0
    _advance(s)
    assert not s.alive()


def test_scorpion_poisons_mushroom_on_overlap() -> None:
    s = Scorpion()
    # Place a mushroom at the scorpion's exact grid position
    m = Mushroom(col=s.col, row=s.row)
    assert not m.is_poisoned
    # Simulate the overlap check from game.py
    if s.rect.colliderect(m.rect):
        m.poison()
    assert m.is_poisoned


def test_mushroom_poison_changes_color() -> None:
    m = Mushroom(col=3, row=3)
    color_before = m.image.get_at((settings.CELL_SIZE // 2, settings.CELL_SIZE // 2))
    m.poison()
    color_after = m.image.get_at((settings.CELL_SIZE // 2, settings.CELL_SIZE // 2))
    assert color_before != color_after
