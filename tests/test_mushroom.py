"""Tests for Mushroom entity."""

import pygame
import pytest
from app.mushroom import Mushroom
from app import settings


@pytest.fixture(autouse=True)
def init_pygame() -> None:
    pygame.init()
    yield
    pygame.quit()


def test_mushroom_starts_at_full_hp() -> None:
    m = Mushroom(col=5, row=5)
    assert m.hp == settings.MUSHROOM_HP


def test_mushroom_hit_reduces_hp() -> None:
    m = Mushroom(col=5, row=5)
    m.hit()
    assert m.hp == settings.MUSHROOM_HP - 1


def test_mushroom_destroyed_after_max_hits() -> None:
    m = Mushroom(col=5, row=5)
    for _ in range(settings.MUSHROOM_HP - 1):
        assert not m.hit()
    destroyed = m.hit()
    assert destroyed


def test_mushroom_pixel_position() -> None:
    m = Mushroom(col=3, row=7)
    assert m.rect.left == 3 * settings.CELL_SIZE
    assert m.rect.top == 7 * settings.CELL_SIZE
