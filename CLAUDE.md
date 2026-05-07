# CLAUDE.md — Centipede

## What this project does
A retro 2D Centipede arcade game built with pygame-ce. The player shoots upward
at a descending centipede while navigating a mushroom field.

## Project structure
```
app/
  settings.py   — all game constants (speed, sizes, colors, grid)
  main.py       — entry point, calls Game().run()
  game.py       — main game loop, sprite groups, collision logic
  player.py     — player shooter sprite
  bullet.py     — bullet sprite
  centipede.py  — Centipede + Segment classes
  mushroom.py   — Mushroom obstacle sprite
assets/
  sprites/      — drop pixel art PNG files here (gitignored until added)
  sounds/       — drop WAV/OGG sound files here (gitignored until added)
tests/          — pytest unit tests for individual entities
```

## How to run
```powershell
.venv\Scripts\activate
python -m app.main
```

## How to test
```powershell
.venv\Scripts\activate
pytest
```

## Key dependencies
- `pygame-ce 2.5.7` — pygame Community Edition; has pre-built wheels for Python 3.14
  (standard `pygame` 2.6 does not support Python 3.14 yet)

## Current state
- Core game loop working: player movement, shooting, centipede movement, mushroom field
- Placeholder colored rectangles for all sprites (no art loaded yet)
- Game over / win detection implemented
- Score tracking implemented

## Project-specific conventions
- All movement uses pixel coordinates internally; the grid (CELL_SIZE) is used
  for mushroom placement and centipede snapping only
- `settings.py` is the single source of truth for all numeric constants
- Bullet limit: one bullet on screen at a time (classic arcade rule)

## Do not touch
- `.venv/` — managed by pip, not by hand
- `requirements.txt` — regenerate with `pip freeze > requirements.txt` if dependencies change
