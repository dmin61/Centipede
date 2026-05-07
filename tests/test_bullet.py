"""Tests for Bullet entity."""

import pygame
import pytest
from app.bullet import Bullet
from app import settings


@pytest.fixture(autouse=True)
def init_pygame() -> None:
    pygame.init()
    yield
    pygame.quit()


def test_bullet_moves_upward() -> None:
    b = Bullet(x=100, y=200)
    initial_y = b.rect.y
    b.update()
    assert b.rect.y < initial_y


def test_bullet_removed_when_off_screen() -> None:
    group = pygame.sprite.Group()
    b = Bullet(x=100, y=5)
    group.add(b)
    # Force bullet past the top edge
    b.rect.bottom = -1
    b.update()
    assert b not in group
