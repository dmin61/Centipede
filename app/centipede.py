"""Centipede entity — a chain of segments that snakes down the screen."""

from __future__ import annotations

import pygame
from app import settings


class Segment(pygame.sprite.Sprite):
    """One segment of the centipede."""

    def __init__(self, col: int, row: int, is_head: bool = False) -> None:
        super().__init__()
        self.image = pygame.Surface((settings.CELL_SIZE, settings.CELL_SIZE))
        color = settings.RED if is_head else (180, 0, 0)
        self.image.fill(color)
        self.rect = self.image.get_rect(
            topleft=(col * settings.CELL_SIZE, row * settings.CELL_SIZE)
        )
        self.col = col
        self.row = row
        self.is_head = is_head

    @property
    def grid_pos(self) -> tuple[int, int]:
        return self.col, self.row


class Centipede:
    """
    Manages all segments as a group. The head leads; each body segment
    follows the position the segment ahead just vacated.
    """

    def __init__(self) -> None:
        self.segments: list[Segment] = []
        self.all_sprites = pygame.sprite.Group()
        self._direction = 1      # 1 = right, -1 = left
        self._drop_pending = False
        self._spawn()

    def _spawn(self) -> None:
        """Place the centipede at the top of the screen."""
        for i in range(settings.CENTIPEDE_LENGTH):
            seg = Segment(
                col=settings.CENTIPEDE_LENGTH - 1 - i,
                row=0,
                is_head=(i == 0),
            )
            self.segments.append(seg)
            self.all_sprites.add(seg)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def update(self, mushroom_cols_by_row: dict[int, set[int]]) -> None:
        """
        Move the centipede one step. Segments follow leader positions.

        Args:
            mushroom_cols_by_row: mapping of row → set of occupied columns,
                used for collision-aware direction reversal.
        """
        # Collect positions before moving (each segment follows the one ahead)
        previous_positions = [(s.col, s.row) for s in self.segments]

        head = self.segments[0]

        if self._drop_pending:
            head.row += 1
            self._direction *= -1
            self._drop_pending = False
        else:
            head.col += self._direction

        # Check if head hit a wall or mushroom
        at_wall = head.col < 0 or head.col >= settings.COLS
        at_mushroom = head.col in mushroom_cols_by_row.get(head.row, set())

        if at_wall or at_mushroom:
            # Revert head, schedule a drop next frame
            head.col = previous_positions[0][0]
            self._drop_pending = True
        else:
            # Body segments follow the path of the segment ahead
            for i in range(1, len(self.segments)):
                self.segments[i].col, self.segments[i].row = previous_positions[i - 1]

        # Sync pixel positions
        for seg in self.segments:
            seg.rect.topleft = (
                seg.col * settings.CELL_SIZE,
                seg.row * settings.CELL_SIZE,
            )

    def remove_segment(self, segment: Segment) -> None:
        """Remove a hit segment. Promotes the next segment to head if needed."""
        idx = self.segments.index(segment)
        self.segments.pop(idx)
        segment.kill()

        if idx == 0 and self.segments:
            self.segments[0].is_head = True
            self.segments[0].image.fill(settings.RED)

    @property
    def is_defeated(self) -> bool:
        """True when all segments have been destroyed."""
        return len(self.segments) == 0
