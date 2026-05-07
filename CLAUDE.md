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
  sprites/
    player/           — ship 01 (5 layer PNGs, Warped series)
    centipede/
      segment-01/     — enemy-01 frames (5 PNGs)
      segment-02/     — enemy-02 frames (4 PNGs)
      segment-03/     — enemy-03 frames (4 PNGs)
    mushroom/         — sunny-mushroom spritesheets + walk frames
    bullet/           — bolt1–4.png (4-frame animated bolt)
    effects/
      hit/            — hit1–3.png
      death/          — enemy-death1–8.png
    background/       — stage-back.png + sprites.png (top-down space)
  sounds/             — WAV files (gitignored); see Sound source below
                        shoot.wav, hit_mushroom.wav, kill_segment.wav,
                        kill_enemy.wav, death.wav, game_over.wav,
                        level_clear.wav, win.wav
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
- Placeholder colored rectangles for all sprites (art and sound assets added, not yet wired to game code)
- Game over / win detection implemented
- Score tracking implemented

## Asset source

All sprites are from the Ansimuz Legacy Collection (free tier), Warped sci-fi series.
Source path (local, not in repo): `C:\Users\Douglas Min\OneDrive\Legacy Video Asset Collection\Legacy Collection\Assets\`

## Sound source

Sounds are not yet added. Recommended free sources (all CC0, no attribution required):

| Tool / Site | Best for | Format |
| --- | --- | --- |
| jsfxr.me | Generate laser, explosion, hit sounds in browser | WAV export |
| kenney.nl/assets | Pre-made Sci-Fi Sounds and Interface Sounds packs | WAV/OGG |
| freesound.org | Broader search; filter by CC0 license | WAV/OGG |
| opengameart.org | Game-specific packs including retro arcade sets | WAV/OGG |

All 8 sounds added to `assets/sounds/` (gitignored, not tracked in repo).

## Project-specific conventions
- All movement uses pixel coordinates internally; the grid (CELL_SIZE) is used
  for mushroom placement and centipede snapping only
- `settings.py` is the single source of truth for all numeric constants
- Bullet limit: one bullet on screen at a time (classic arcade rule)

## Do not touch
- `.venv/` — managed by pip, not by hand
- `requirements.txt` — regenerate with `pip freeze > requirements.txt` if dependencies change
