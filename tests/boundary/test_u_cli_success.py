"""U-001 — successful CLI output (PRD INV-07, SC-1)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from boundary.cli import run
from tests.boundary.conftest import MOCK_SUCCESS_METER_25


def test_u001_cli_prints_feet_and_yard_conversions(capsys: pytest.CaptureFixture[str]) -> None:
    """U-001 / INV-07, SC-1 — stdout includes converted feet and yard values."""
    with patch("boundary.cli.convert_length", return_value=MOCK_SUCCESS_METER_25):
        run("meter:2.5")

    captured = capsys.readouterr()
    assert "8.2 feet" in captured.out
    assert "2.7 yard" in captured.out
