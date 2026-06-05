"""Shared mock ConversionResult fixtures for UI Track RED tests."""

from __future__ import annotations

MOCK_SUCCESS_METER_25: dict = {
    "ok": True,
    "source": {"unit": "meter", "value": 2.5},
    "conversions": [
        {"unit": "meter", "value": 2.5},
        {"unit": "feet", "value": 8.2},
        {"unit": "yard", "value": 2.7},
    ],
}

MOCK_FORMAT_INVALID: dict = {
    "ok": False,
    "error": "FORMAT_INVALID",
    "message": "Invalid format. Use unit:value (ex: meter:2.5)",
}

MOCK_UNKNOWN_UNIT_CUBIT: dict = {
    "ok": False,
    "error": "UNKNOWN_UNIT",
    "message": "Unknown unit: cubit",
}
