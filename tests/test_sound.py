"""Tests for SoundManager — behaviour when files are absent and mute toggle."""

import pygame
import pytest

from app.sound import SoundManager


@pytest.fixture(autouse=True)
def init_pygame() -> None:
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mgr() -> SoundManager:
    return SoundManager()


def test_starts_unmuted(mgr: SoundManager) -> None:
    assert not mgr.muted


def test_toggle_mute_enables_mute(mgr: SoundManager) -> None:
    mgr.toggle_mute()
    assert mgr.muted


def test_toggle_mute_twice_restores_unmuted(mgr: SoundManager) -> None:
    mgr.toggle_mute()
    mgr.toggle_mute()
    assert not mgr.muted


def test_all_known_events_are_registered(mgr: SoundManager) -> None:
    expected = {
        "shoot", "hit_mushroom", "kill_segment", "kill_enemy",
        "death", "level_clear", "game_over", "win",
    }
    assert expected == set(mgr._sounds.keys())


def test_sound_slots_are_sound_or_none(mgr: SoundManager) -> None:
    # Every slot must be either a loaded Sound or None — never an error object
    for name, sound in mgr._sounds.items():
        assert sound is None or isinstance(sound, pygame.mixer.Sound), (
            f"Unexpected type for '{name}': {type(sound)}"
        )


def test_play_unknown_name_does_not_raise(mgr: SoundManager) -> None:
    mgr.play("not_a_real_sound")  # should silently no-op


def test_play_while_muted_does_not_raise(mgr: SoundManager) -> None:
    mgr.muted = True
    mgr.play("shoot")  # should silently no-op
