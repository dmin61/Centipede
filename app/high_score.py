"""High score persistence — read/write a single integer to data/high_score.txt."""

from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "data"
_SCORE_FILE = _DATA_DIR / "high_score.txt"


def load_high_score(path: Path = _SCORE_FILE) -> int:
    """
    Read the stored high score.
    Returns 0 if the file is missing, empty, or contains non-integer data.
    """
    try:
        return int(path.read_text().strip())
    except (FileNotFoundError, ValueError, OSError):
        return 0


def save_high_score(score: int, path: Path = _SCORE_FILE) -> None:
    """
    Write score to disk. Creates the data/ directory if it does not exist.
    Silently ignores write errors (read-only filesystem, etc.).
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(score))
    except OSError:
        pass
