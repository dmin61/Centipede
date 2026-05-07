"""
Sound manager — loads WAV/OGG files from assets/sounds/ and plays them.
Silently no-ops when a file is missing or the mixer is unavailable.
Toggle mute at runtime with the M key (handled by game.py).
"""

from pathlib import Path

import pygame

SOUNDS_DIR = Path(__file__).parent.parent / "assets" / "sounds"

# Canonical event names and their filenames (add files to assets/sounds/ to activate)
_SOUND_FILES: dict[str, str] = {
    "shoot":        "shoot.wav",
    "hit_mushroom": "hit_mushroom.wav",
    "kill_segment": "kill_segment.wav",
    "kill_enemy":   "kill_enemy.wav",
    "death":        "death.wav",
    "level_clear":  "level_clear.wav",
    "game_over":    "game_over.wav",
    "win":          "win.wav",
}


class SoundManager:
    """
    Loads all known sound files at init time.
    Missing files produce no error — the slot stays None and play() skips it.
    """

    def __init__(self) -> None:
        self.muted = False
        self._sounds: dict[str, pygame.mixer.Sound | None] = {}

        if not pygame.mixer.get_init():
            # Mixer not available (headless test, missing audio device, etc.)
            for name in _SOUND_FILES:
                self._sounds[name] = None
            return

        for name, filename in _SOUND_FILES.items():
            path = SOUNDS_DIR / filename
            if path.exists():
                try:
                    self._sounds[name] = pygame.mixer.Sound(str(path))
                except pygame.error:
                    self._sounds[name] = None
            else:
                self._sounds[name] = None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def play(self, name: str) -> None:
        """
        Play a sound by event name. Silently ignored when:
        - the manager is muted
        - the sound file was not found
        - the mixer is not available
        """
        if self.muted:
            return
        sound = self._sounds.get(name)
        if sound is not None:
            sound.play()

    def toggle_mute(self) -> None:
        """Flip mute state. Stops all currently playing sounds when muting."""
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.stop()
