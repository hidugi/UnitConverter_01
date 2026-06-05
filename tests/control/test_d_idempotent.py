"""D-007 — deterministic conversion (PRD INV-08, SC-3)."""

from __future__ import annotations

from control.convert_length import convert_length


def test_d007_same_input_produces_identical_result() -> None:
    """D-007 / INV-08, SC-3 — identical input yields identical ConversionResult."""
    input_str = "meter:2.5"

    first = convert_length(input_str)
    second = convert_length(input_str)

    assert first == second
