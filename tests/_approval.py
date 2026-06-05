"""Golden Master helpers — approved baseline comparison."""

from __future__ import annotations

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def _normalize(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return normalized.rstrip("\n")


def assert_matches_golden(actual: str, relative: str) -> None:
    """Compare actual output to tests/golden/{relative}, or update when UPDATE_GOLDEN=1."""
    golden_path = GOLDEN_DIR / relative
    actual_norm = _normalize(actual)

    if os.environ.get("UPDATE_GOLDEN"):
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual_norm + "\n", encoding="utf-8", newline="\n")
        return

    if not golden_path.is_file():
        raise AssertionError(f"golden file missing: {golden_path} (run with UPDATE_GOLDEN=1)")

    expected_norm = _normalize(golden_path.read_text(encoding="utf-8"))
    if actual_norm == expected_norm:
        return

    import difflib

    diff = difflib.unified_diff(
        expected_norm.splitlines(),
        actual_norm.splitlines(),
        fromfile=f"golden/{relative}",
        tofile="actual",
        lineterm="",
    )
    raise AssertionError("golden mismatch:\n" + "\n".join(diff))
