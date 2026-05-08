# Centipede

A retro 2D arcade game built with Python and pygame-ce. Faithful to the classic
Atari Centipede cabinet: a 12-segment centipede descends through a mushroom field
while three enemy types (flea, spider, scorpion) harass the player from different
angles.

## Gameplay

- **Shoot** the centipede one segment at a time. Each hit leaves a mushroom behind.
- Reach the **bottom** of the screen? The remaining centipede turns around and
  charges back up — faster each level.
- **Flea** drops mushrooms as it falls. Appears when your zone gets too clear.
- **Spider** zigzags through your zone and eats mushrooms. Closer kills score more.
- **Scorpion** poisons mushrooms it crosses, making the centipede dive immediately.
- Clear all 10 levels to win.

### Controls

| Key | Action |
|-----|--------|
| Arrow keys | Move player |
| Space | Fire |
| P | Pause / resume |
| Q | Quit to title |

## Requirements

- Python 3.14
- pygame-ce 2.5.7

> `pygame-ce` (Community Edition) is used instead of standard `pygame` because it
> ships pre-built wheels for Python 3.14. Standard `pygame` 2.6 does not.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```powershell
.venv\Scripts\activate
python -m app.main
```

## Test

```powershell
pytest
```

## Project structure

```
app/
  main.py        — entry point
  game.py        — game loop, state machine, collision logic
  settings.py    — all numeric constants (single source of truth)
  player.py      — player sprite
  bullet.py      — bullet sprite (one on screen at a time)
  centipede.py   — Centipede + Segment classes
  mushroom.py    — mushroom obstacle
  flea.py        — flea enemy
  spider.py      — spider enemy
  scorpion.py    — scorpion enemy
  screens.py     — title, pause, game-over, win overlays
  sound.py       — sound manager
  sprite_loader.py — asset loader
  high_score.py  — persistent high score (local file)
assets/
  sprites/       — pixel art (Ansimuz Legacy Collection, Warped sci-fi series)
  sounds/        — WAV files (gitignored; supply your own — see below)
tests/           — pytest unit tests
```

## Sound assets

Sound files are not included in the repo. Drop these eight WAV files into
`assets/sounds/` to enable audio:

| Filename | Event |
|----------|-------|
| `shoot.wav` | Player fires |
| `hit_mushroom.wav` | Bullet hits mushroom |
| `kill_segment.wav` | Centipede segment destroyed |
| `kill_enemy.wav` | Flea / spider / scorpion destroyed |
| `death.wav` | Player dies |
| `game_over.wav` | All lives lost |
| `level_clear.wav` | Wave cleared |
| `win.wav` | All 10 levels cleared |

Free CC0 sources: [jsfxr](https://sfxr.me), [Kenney](https://kenney.nl/assets),
[freesound.org](https://freesound.org), [opengameart.org](https://opengameart.org).

## Art credits

Sprites are from the **Ansimuz Legacy Collection** (free tier), Warped sci-fi
series. See [ansimuz.com](https://ansimuz.com) for the full collection.

## License

MIT
