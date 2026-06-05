"""U-002, U-003 — CLI error messaging (PRD FORMAT_INVALID, UNKNOWN_UNIT)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from boundary.cli import run
from tests.boundary.conftest import MOCK_FORMAT_INVALID, MOCK_UNKNOWN_UNIT_CUBIT


def test_u002_cli_prints_format_invalid_message(capsys: pytest.CaptureFixture[str]) -> None:
    """U-002 / FORMAT_INVALID — stdout or stderr shows format error guidance."""
    with patch("boundary.cli.convert_length", return_value=MOCK_FORMAT_INVALID):
        run("meter2.5")

    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "format" in output.lower() or "unit:value" in output.lower()


def test_u003_cli_prints_unknown_unit_message(capsys: pytest.CaptureFixture[str]) -> None:
    """U-003 / UNKNOWN_UNIT — stdout includes unknown unit name."""
    with patch("boundary.cli.convert_length", return_value=MOCK_UNKNOWN_UNIT_CUBIT):
        run("cubit:1.0")

    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "Unknown unit: cubit" in output or "cubit" in output.lower()
