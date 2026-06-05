"""D-005 — full unit conversion (PRD INV-07, SC-1)."""

from __future__ import annotations

import pytest

from control.convert_length import convert_length
from tests.conftest import CONVERSION_FIXTURES, conversion_value


@pytest.mark.parametrize(
    ("input_str", "source_unit", "source_value", "expected"),
    CONVERSION_FIXTURES,
    ids=["meter_input", "feet_input", "yard_input"],
)
def test_d005_convert_length_returns_all_units(
    input_str: str,
    source_unit: str,
    source_value: float,
    expected: dict[str, float],
) -> None:
    """D-005 / INV-07, SC-1 — success includes meter, feet, and yard."""
    result = convert_length(input_str)

    assert result["ok"] is True
    assert result["source"] == {"unit": source_unit, "value": source_value}

    units = {item["unit"] for item in result["conversions"]}
    assert units == {"meter", "feet", "yard"}

    for unit, value in expected.items():
        assert conversion_value(result, unit) == value
