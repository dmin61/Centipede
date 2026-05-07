"""
Sprite loading with graceful fallback to colored rectangles.

convert_alpha() is intentionally omitted so this module can be called
before a display mode is initialised (unit tests, headless builds).
"""

from pathlib import Path

import pygame

from app import settings

SPRITES_DIR = Path(__file__).parent.parent / "assets" / "sprites"

# Default fallback colors keyed by folder name
_FALLBACKS: dict[str, tuple[int, int, int]] = {
    "player":               settings.GREEN,
    "centipede/segment-01": settings.RED,
    "centipede/segment-02": (180, 0, 0),
    "centipede/segment-03": (160, 0, 0),
    "mushroom":             settings.BROWN,
    "bullet":               settings.YELLOW,
    "flea":                 (220, 220, 50),
    "spider":               (150, 0, 200),
    "scorpion":             (200, 130, 0),
    "background":           settings.BLACK,
}


def _colored_rect(
    size: tuple[int, int],
    color: tuple[int, int, int],
) -> pygame.Surface:
    surface = pygame.Surface(size)
    surface.fill(color)
    return surface


def load_composite(
    folder: str,
    size: tuple[int, int] | None = None,
    fallback_color: tuple[int, int, int] | None = None,
    glob_pattern: str = "*.png",
) -> pygame.Surface:
    """
    Composite all PNGs matching glob_pattern inside assets/sprites/<folder>/,
    sorted by filename (lowest = bottom layer). Layers are blitted at (0, 0)
    onto a canvas sized to the maximum of all layer dimensions.

    Falls back to a colored rectangle when the folder is missing or empty.

    Args:
        folder: Path relative to assets/sprites/ (e.g. "player").
        size: Target (width, height). Defaults to (CELL_SIZE, CELL_SIZE).
        fallback_color: RGB color for the fallback surface.
        glob_pattern: Filename filter (e.g. "0__*.png" for mushroom layers).

    Returns:
        New pygame.Surface scaled to size.
    """
    target = size or (settings.CELL_SIZE, settings.CELL_SIZE)
    color = fallback_color or _FALLBACKS.get(folder, (128, 128, 128))
    dir_path = SPRITES_DIR / folder

    if not dir_path.is_dir():
        return _colored_rect(target, color)

    png_files = sorted(dir_path.glob(glob_pattern))
    if not png_files:
        return _colored_rect(target, color)

    try:
        surfaces = [pygame.image.load(str(p)) for p in png_files]
        max_w = max(s.get_width() for s in surfaces)
        max_h = max(s.get_height() for s in surfaces)
        canvas = pygame.Surface((max_w, max_h), pygame.SRCALPHA)
        for surf in surfaces:
            canvas.blit(surf, (0, 0))
        return pygame.transform.smoothscale(canvas, target)
    except pygame.error:
        return _colored_rect(target, color)


def load_single(
    relative_path: str,
    size: tuple[int, int] | None = None,
    fallback_color: tuple[int, int, int] | None = None,
    rotate: float = 0,
) -> pygame.Surface:
    """
    Load a single PNG from assets/sprites/<relative_path>.

    Falls back to a colored rectangle when the file is missing.

    Args:
        relative_path: Path relative to assets/sprites/ (e.g. "bullet/bolt1.png").
        size: Target (width, height). Defaults to (CELL_SIZE, CELL_SIZE).
        fallback_color: RGB color for the fallback surface.
        rotate: Degrees to rotate counter-clockwise before scaling.

    Returns:
        New pygame.Surface scaled to size.
    """
    target = size or (settings.CELL_SIZE, settings.CELL_SIZE)
    folder_key = str(Path(relative_path).parent)
    color = fallback_color or _FALLBACKS.get(folder_key, (128, 128, 128))
    file_path = SPRITES_DIR / relative_path

    if not file_path.exists():
        return _colored_rect(target, color)

    try:
        img = pygame.image.load(str(file_path))
        if rotate:
            img = pygame.transform.rotate(img, rotate)
        return pygame.transform.smoothscale(img, target)
    except pygame.error:
        return _colored_rect(target, color)
