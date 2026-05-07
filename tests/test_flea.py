"""Tests for the Flea enemy."""

import pygame
import pytest
from unittest.mock import patch

from app import settings
from app.flea import Flea


@pytest.fixture(autouse=True)
def init_pygame() -> None:
    pygame.init()
    yield
    pygame.quit()


def test_flea_starts_at_row_zero() -> None:
    f = Flea(col=5)
    assert f.row == 0


def test_flea_starts_at_correct_col() -> None:
    f = Flea(col=7)
    assert f.col == 7
    assert f.rect.left == 7 * settings.CELL_SIZE


def test_flea_starts_with_full_hp() -> None:
    f = Flea(col=0)
    assert f.hp == settings.FLEA_HP


def test_flea_does_not_move_before_interval() -> None:
    f = Flea(col=5)
    initial_row = f.row
    f.update()  # one frame — step interval > 1
    # Only moves if step_interval == 1, which requires FLEA_STEPS == FPS
    if settings.FLEA_STEPS < settings.FPS:
        assert f.row == initial_row


def test_flea_moves_down_after_interval() -> None:
    f = Flea(col=5)
    # Force timer to trigger
    f._step_timer = f._step_interval - 1
    f.update()
    assert f.row == 1


def test_flea_survives_first_hit() -> None:
    f = Flea(col=5)
    destroyed = f.hit()
    assert not destroyed
    assert f.hp == settings.FLEA_HP - 1


def test_flea_destroyed_on_second_hit() -> None:
    f = Flea(col=5)
    f.hit()
    destroyed = f.hit()
    assert destroyed
    assert not f.alive()


def test_flea_kills_itself_at_bottom() -> None:
    f = Flea(col=5)
    f._step_timer = f._step_interval - 1
    f.row = settings.ROWS - 1  # one step from the edge
    f.update()
    assert not f.alive()


def test_flea_drop_returned_when_chance_100() -> None:
    f = Flea(col=5)
    f._step_timer = f._step_interval - 1
    with patch("app.flea.random.random", return_value=0.0):  # 0.0 < any drop chance
        result = f.update()
    assert result == (5, 1)


def test_flea_no_drop_returned_when_chance_0() -> None:
    f = Flea(col=5)
    f._step_timer = f._step_interval - 1
    with patch("app.flea.random.random", return_value=1.0):  # 1.0 >= any drop chance
        result = f.update()
    assert result is None
