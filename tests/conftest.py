"""Shared fixtures for Logic Track RED tests (PRD §5.3, TEST_PLAN §4.3)."""

from __future__ import annotations

# input_str, source_unit, source_value, expected conversions (1-decimal rounding)
CONVERSION_FIXTURES: list[tuple[str, str, float, dict[str, float]]] = [
    ("meter:2.5", "meter", 2.5, {"meter": 2.5, "feet": 8.2, "yard": 2.7}),
    ("feet:8.2", "feet", 8.2, {"meter": 2.5, "feet": 8.2, "yard": 2.7}),
    ("yard:2.7", "yard", 2.7, {"meter": 2.5, "feet": 8.2, "yard": 2.7}),
]


def conversion_value(result: dict, unit: str) -> float:
    """Extract a single unit value from a successful ConversionResult."""
    for item in result["conversions"]:
        if item["unit"] == unit:
            return item["value"]
    raise KeyError(f"unit not found in conversions: {unit}")
