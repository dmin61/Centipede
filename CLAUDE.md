# CLAUDE.md — Centipede

## What this project does
A retro 2D Centipede arcade game built with pygame-ce. The player shoots upward
at a descending centipede while navigating a mushroom field.

## Project structure
```
main.py         — pygbag entry point (async wrapper for browser build)
app/
  settings.py   — all game constants (speed, sizes, colors, grid)
  main.py       — desktop entry point, calls Game().run()
  game.py       — main game loop, sprite groups, collision logic
  player.py     — player shooter sprite
  bullet.py     — bullet sprite
  centipede.py  — Centipede + Segment classes
  mushroom.py   — Mushroom obstacle sprite
  flea.py       — Flea enemy (drops mushrooms, appears when zone too clear)
  spider.py     — Spider enemy (zigzags, eats mushrooms, proximity scoring)
  scorpion.py   — Scorpion enemy (poisons mushrooms, triggers centipede dive)
  screens.py    — title, pause, game-over, win overlays
  sound.py      — sound manager (mute toggle, graceful missing-file handling)
  sprite_loader.py — asset loader (pixel art sprites wired to all entities)
  high_score.py — persistent high score (local file)
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
build/
  web/          — pygbag browser build output (index.html, centipede.apk)
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
- `pygbag` — packages the game as a WebAssembly browser build for itch.io

## How to build for browser
```powershell
.venv\Scripts\activate
pygbag .
```
Serves locally at http://localhost:8000. Output goes to `build/web/`.
To publish: zip `build/web/*` and upload to itch.io as an HTML game (600×800).

## Current state
- Complete game: all 10 levels, 3 enemy types (flea, spider, scorpion), score, lives, high score
- Pixel art sprites wired to all entities (Ansimuz Legacy Collection)
- Sound manager wired; 8 WAV files in assets/sounds/ (gitignored)
- Published to itch.io as a browser game (desktop only, keyboard required)

## Asset source

All sprites are from the Ansimuz Legacy Collection (free tier), Warped sci-fi series.
Source path (local, not in repo): `C:\Users\Douglas Min\OneDrive\Legacy Video Asset Collection\Legacy Collection\Assets\`

## Sound source

All 8 sounds added to `assets/sounds/` (gitignored, not tracked in repo).
Free CC0 sources used: jsfxr.me, kenney.nl/assets, freesound.org, opengameart.org.

## Project-specific conventions
- All movement uses pixel coordinates internally; the grid (CELL_SIZE) is used
  for mushroom placement and centipede snapping only
- `settings.py` is the single source of truth for all numeric constants
- Bullet limit: one bullet on screen at a time (classic arcade rule)

## Do not touch
- `.venv/` — managed by pip, not by hand
- `requirements.txt` — regenerate with `pip freeze > requirements.txt` if dependencies change
