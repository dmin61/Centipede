"""Tests for centipede frenzy mode (triggered by poisoned mushrooms)."""

import pygame
import pytest

from app import settings
from app.centipede import Centipede


@pytest.fixture(autouse=True)
def init_pygame() -> None:
    pygame.init()
    yield
    pygame.quit()


def _step(c: Centipede, mushroom_index: dict | None = None, poisoned: set | None = None) -> None:
    """Force one grid step regardless of the centipede's internal timer."""
    c._step_timer = c._step_interval - 1
    c.update(mushroom_index or {}, poisoned or set())


def test_centipede_not_frenzied_by_default() -> None:
    c = Centipede()
    assert not c._frenzied


def test_frenzy_activates_on_poisoned_mushroom() -> None:
    c = Centipede()
    head = c.segments[0]
    # Place a poisoned mushroom one step ahead of the head
    target_col = head.col + c._direction
    poisoned = {(target_col, head.row)}
    mushroom_index = {head.row: {target_col}}  # mushroom blocks horizontal
    _step(c, mushroom_index, poisoned)
    assert c._frenzied


def test_frenzied_centipede_moves_straight_down() -> None:
    c = Centipede()
    c._frenzied = True
    initial_row = c.segments[0].row
    _step(c)
    assert c.segments[0].row == initial_row + 1
    # Col must not change
    assert c.segments[0].col == settings.CENTIPEDE_LENGTH - 1


def test_frenzied_centipede_ignores_mushrooms() -> None:
    c = Centipede()
    c._frenzied = True
    head = c.segments[0]
    # Put a mushroom directly below the head
    mushroom_index = {head.row + 1: {head.col}}
    initial_col = head.col
    _step(c, mushroom_index)
    # Should still move down and not change direction
    assert head.col == initial_col
    assert head.row == 1  # dropped one row
