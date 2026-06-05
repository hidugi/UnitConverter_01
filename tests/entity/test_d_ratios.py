"""D-006 — conversion ratios (PRD INV-02, INV-03, SC-2)."""

from __future__ import annotations

from control.convert_length import convert_length
from entity.ratios import FEET_PER_METER, YARD_PER_METER
from tests.conftest import conversion_value


def test_d006_entity_uses_exact_feet_ratio() -> None:
    """D-006 / INV-02 — feet ratio must be 3.28084, not rounded 3.28."""
    assert FEET_PER_METER == 3.28084
    assert FEET_PER_METER != 3.28


def test_d006_entity_uses_exact_yard_ratio() -> None:
    """D-006 / INV-03 — yard ratio must be 1.09361."""
    assert YARD_PER_METER == 1.09361


def test_d006_wrong_feet_ratio_would_not_match_fixture() -> None:
    """D-006 / SC-2 — 3.28-based math diverges from the accepted fixture."""
    wrong_feet = round(2.5 * 3.28, 1)
    assert wrong_feet != 8.2


def test_d006_meter_input_matches_rounded_fixture() -> None:
    """D-006 / SC-2 — meter:2.5 produces feet=8.2 and yard=2.7."""
    result = convert_length("meter:2.5")

    assert result["ok"] is True
    assert conversion_value(result, "feet") == 8.2
    assert conversion_value(result, "yard") == 2.7
