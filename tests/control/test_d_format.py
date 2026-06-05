"""D-001, D-002 — input format validation (PRD §5.1, FORMAT_INVALID / VALUE_NOT_NUMBER)."""

from __future__ import annotations

import pytest

from control.convert_length import convert_length


@pytest.mark.parametrize(
    "input_str",
    [
        "meter2.5",  # missing colon
        ":2.5",  # empty unit
        "meter:",  # empty value
    ],
    ids=["no_colon", "empty_unit", "empty_value"],
)
def test_d001_format_invalid_returns_error(input_str: str) -> None:
    """D-001 / FORMAT_INVALID — colon missing or empty unit/value."""
    result = convert_length(input_str)

    assert result["ok"] is False
    assert result["error"] == "FORMAT_INVALID"
    assert "message" in result


@pytest.mark.parametrize(
    "input_str",
    [
        "meter:abc",
        "feet:2.5.3",
    ],
    ids=["non_numeric", "multiple_dots"],
)
def test_d002_value_not_number_returns_error(input_str: str) -> None:
    """D-002 / VALUE_NOT_NUMBER — value cannot be parsed as float."""
    result = convert_length(input_str)

    assert result["ok"] is False
    assert result["error"] == "VALUE_NOT_NUMBER"
    assert "message" in result
