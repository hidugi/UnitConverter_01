"""U-004 — boundary to control end-to-end smoke (PRD SC-1, E002)."""

from __future__ import annotations

import pytest

from boundary.cli import run
from control.convert_length import convert_length
from tests._approval import assert_matches_golden


def test_u004_golden_meter_25_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    """U-004 / SC-1 — meter:2.5 CLI stdout golden master (no Mock)."""
    run("meter:2.5")

    captured = capsys.readouterr()
    assert_matches_golden(captured.out, "u004_meter_25_stdout.approved.txt")


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
