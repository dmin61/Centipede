"""Centipede entity — a chain of segments that snakes down the screen."""

from __future__ import annotations

import pygame
from app import settings
from app.sprite_loader import load_composite


class Segment(pygame.sprite.Sprite):
    """One segment of the centipede."""

    def __init__(self, col: int, row: int, is_head: bool = False) -> None:
        super().__init__()
        folder = "centipede/segment-01" if is_head else "centipede/segment-02"
        self.image = load_composite(folder)
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

    Args:
        steps_per_second: Grid cells the head advances per second.
        start_row:        Row the centipede spawns on (increases each level).
    """

    def __init__(
        self,
        steps_per_second: int = settings.CENTIPEDE_BASE_STEPS,
        start_row: int = 0,
    ) -> None:
        self._step_interval = max(1, settings.FPS // steps_per_second)
        self._step_timer = 0
        self._direction = 1        # 1 = right, -1 = left
        self._drop_pending = False
        self._frenzied = False     # True after hitting a poisoned mushroom

        self.segments: list[Segment] = []
        self.all_sprites = pygame.sprite.Group()
        self._spawn(start_row)

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _spawn(self, start_row: int) -> None:
        """Place the centipede at start_row, extending leftward."""
        for i in range(settings.CENTIPEDE_LENGTH):
            seg = Segment(
                col=settings.CENTIPEDE_LENGTH - 1 - i,
                row=start_row,
                is_head=(i == 0),
            )
            self.segments.append(seg)
            self.all_sprites.add(seg)

    def _move(
        self,
        mushroom_cols_by_row: dict[int, set[int]],
        poisoned_positions: set[tuple[int, int]],
    ) -> None:
        """Advance the centipede one grid step."""
        previous_positions = [(s.col, s.row) for s in self.segments]
        head = self.segments[0]
        head_moved = False

        if self._frenzied:
            # Dive straight down — ignore walls and mushrooms
            head.row += 1
            head_moved = True

        elif self._drop_pending:
            head.row += 1
            self._direction *= -1
            self._drop_pending = False
            head_moved = True

        else:
            # Normal horizontal movement
            next_col = head.col + self._direction
            at_wall = next_col < 0 or next_col >= settings.COLS
            at_mushroom = next_col in mushroom_cols_by_row.get(head.row, set())

            if at_wall or at_mushroom:
                self._drop_pending = True
                # Hitting a poisoned mushroom triggers frenzy on the NEXT drop
                if at_mushroom and (next_col, head.row) in poisoned_positions:
                    self._frenzied = True
            else:
                head.col = next_col
                head_moved = True

        # Body follows only when the head actually moved
        if head_moved:
            for i in range(1, len(self.segments)):
                self.segments[i].col, self.segments[i].row = previous_positions[i - 1]

        # Sync pixel positions for all segments
        for seg in self.segments:
            seg.rect.topleft = (
                seg.col * settings.CELL_SIZE,
                seg.row * settings.CELL_SIZE,
            )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def update(
        self,
        mushroom_cols_by_row: dict[int, set[int]],
        poisoned_positions: set[tuple[int, int]] | None = None,
    ) -> None:
        """
        Called every frame. Advances the centipede only when the step timer fires.

        Args:
            mushroom_cols_by_row: row → occupied cols, for collision/direction logic.
            poisoned_positions:   (col, row) pairs of poisoned mushrooms.
        """
        self._step_timer += 1
        if self._step_timer >= self._step_interval:
            self._step_timer = 0
            self._move(mushroom_cols_by_row, poisoned_positions or set())

    def remove_segment(self, segment: Segment) -> None:
        """Remove a hit segment. Promotes the next segment to head if needed."""
        idx = self.segments.index(segment)
        self.segments.pop(idx)
        segment.kill()

        if idx == 0 and self.segments:
            self.segments[0].is_head = True
            self.segments[0].image = load_composite("centipede/segment-01")

    @property
    def is_defeated(self) -> bool:
        """True when all segments have been destroyed."""
        return len(self.segments) == 0
