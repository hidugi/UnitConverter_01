"""Control-layer orchestration for convert_length (PRD §5.1)."""

from __future__ import annotations

from entity.convert_length import convert_length as convert_all_units

_SUPPORTED_UNITS = frozenset({"meter", "feet", "yard"})


def convert_length(input_str: str) -> dict:
    if ":" not in input_str:
        return {
            "ok": False,
            "error": "FORMAT_INVALID",
            "message": "Invalid format. Use unit:value (ex: meter:2.5)",
        }

    unit, value_str = input_str.split(":", 1)
    if not unit or not value_str:
        return {
            "ok": False,
            "error": "FORMAT_INVALID",
            "message": "Invalid format. Use unit:value (ex: meter:2.5)",
        }

    try:
        value = float(value_str)
    except ValueError:
        return {
            "ok": False,
            "error": "VALUE_NOT_NUMBER",
            "message": f"Invalid number: {value_str}",
        }

    if unit not in _SUPPORTED_UNITS:
        return {
            "ok": False,
            "error": "UNKNOWN_UNIT",
            "message": f"Unknown unit: {unit}",
        }

    if value < 0:
        return {
            "ok": False,
            "error": "NEGATIVE_VALUE",
            "message": "Negative value not allowed",
        }

    conversions = convert_all_units(unit, value)
    return {
        "ok": True,
        "source": {"unit": unit, "value": value},
        "conversions": conversions,
    }
