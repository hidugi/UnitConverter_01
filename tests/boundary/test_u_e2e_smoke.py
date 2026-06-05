"""U-004 — boundary to control end-to-end smoke (PRD SC-1, E002)."""

from __future__ import annotations

import pytest

from boundary.cli import run
from control.convert_length import convert_length


def test_u004_e2e_output_matches_control_result(capsys: pytest.CaptureFixture[str]) -> None:
    """U-004 / SC-1 — CLI output reflects real convert_length result for meter:2.5."""
    input_str = "meter:2.5"
    expected = convert_length(input_str)

    run(input_str)

    captured = capsys.readouterr()
    assert expected["ok"] is True

    for item in expected["conversions"]:
        if item["unit"] == "feet":
            assert f"{item['value']} feet" in captured.out
        if item["unit"] == "yard":
            assert f"{item['value']} yard" in captured.out
