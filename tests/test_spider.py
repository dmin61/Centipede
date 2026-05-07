"""Tests for the Spider enemy."""

import pygame
import pytest

from app import settings
from app.spider import Spider, _ZONE_TOP, _ZONE_BOT


@pytest.fixture(autouse=True)
def init_pygame() -> None:
    pygame.init()
    yield
    pygame.quit()


def _advance(spider: Spider, steps: int = 1) -> None:
    """Force spider to take N grid steps regardless of its timer."""
    for _ in range(steps):
        spider._step_timer = spider._step_interval - 1
        spider.update()


def test_spider_starts_at_zone_top() -> None:
    s = Spider()
    assert s.row == _ZONE_TOP


def test_spider_stays_above_zone_bottom() -> None:
    s = Spider()
    s._dy = 1  # moving down
    for _ in range(settings.PLAYER_ZONE_ROWS + 5):
        _advance(s)
        if s.alive():
            assert s.row <= _ZONE_BOT


def test_spider_stays_below_zone_top() -> None:
    s = Spider()
    s._dy = -1  # moving up
    for _ in range(settings.PLAYER_ZONE_ROWS + 5):
        _advance(s)
        if s.alive():
            assert s.row >= _ZONE_TOP


def test_spider_exits_left_edge() -> None:
    s = Spider()
    s.col = 0
    s._dx = -1
    _advance(s)
    assert not s.alive()


def test_spider_exits_right_edge() -> None:
    s = Spider()
    s.col = settings.COLS - 1
    s._dx = 1
    _advance(s)
    assert not s.alive()


def test_spider_score_close() -> None:
    s = Spider()
    player_rect = pygame.Rect(
        s.rect.centerx - 50,
        s.rect.centery - 50,
        settings.CELL_SIZE,
        settings.CELL_SIZE,
    )
    assert s.score_for_kill(player_rect) == settings.SPIDER_SCORE_CLOSE


def test_spider_score_far() -> None:
    s = Spider()
    player_rect = pygame.Rect(
        s.rect.centerx + 300,
        s.rect.centery + 300,
        settings.CELL_SIZE,
        settings.CELL_SIZE,
    )
    assert s.score_for_kill(player_rect) == settings.SPIDER_SCORE_FAR
