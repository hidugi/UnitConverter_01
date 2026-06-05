"""D-003 — unknown unit rejection (PRD §5.1, UNKNOWN_UNIT)."""

from __future__ import annotations

import pytest

from control.convert_length import convert_length


@pytest.mark.parametrize(
    ("input_str", "unknown_unit"),
    [
        ("cubit:1.0", "cubit"),
        ("inch:10", "inch"),
    ],
    ids=["cubit", "inch"],
)
def test_d003_unknown_unit_returns_error(input_str: str, unknown_unit: str) -> None:
    """D-003 / UNKNOWN_UNIT — unit must be meter, feet, or yard."""
    result = convert_length(input_str)

    assert result["ok"] is False
    assert result["error"] == "UNKNOWN_UNIT"
    assert unknown_unit in result["message"]
