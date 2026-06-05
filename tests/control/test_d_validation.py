"""D-004 — negative value rejection (PRD §5.1, NEGATIVE_VALUE)."""

from __future__ import annotations

import pytest

from control.convert_length import convert_length


@pytest.mark.parametrize(
    "input_str",
    [
        "meter:-1",
        "feet:-0.1",
    ],
    ids=["meter_negative", "feet_negative"],
)
def test_d004_negative_value_returns_error(input_str: str) -> None:
    """D-004 / NEGATIVE_VALUE — value must be >= 0."""
    result = convert_length(input_str)

    assert result["ok"] is False
    assert result["error"] == "NEGATIVE_VALUE"
    assert "message" in result
