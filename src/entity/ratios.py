"""Conversion ratio constants (PRD INV-02, INV-03)."""

from __future__ import annotations

FEET_PER_METER = 3.28084
YARD_PER_METER = 1.09361


def ratios() -> dict[str, float]:
    """Return meter-based conversion ratios for supported units."""
    return {"feet": FEET_PER_METER, "yard": YARD_PER_METER}
