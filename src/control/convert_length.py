"""Control-layer orchestration for convert_length (PRD §5.1)."""

from __future__ import annotations

from entity.convert_length import convert_length as convert_all_units

_SUPPORTED_UNITS = frozenset({"meter", "feet", "yard"})


def _make_error(error: str, message: str) -> dict:
    return {"ok": False, "error": error, "message": message}


def _parse_format(input_str: str) -> dict | tuple[str, str]:
    if ":" not in input_str:
        return _make_error(
            "FORMAT_INVALID",
            "Invalid format. Use unit:value (ex: meter:2.5)",
        )

    unit, value_str = input_str.split(":", 1)
    if not unit or not value_str:
        return _make_error(
            "FORMAT_INVALID",
            "Invalid format. Use unit:value (ex: meter:2.5)",
        )

    return unit, value_str


def _validate_unit_and_value(unit: str, value_str: str) -> dict | float:
    try:
        value = float(value_str)
    except ValueError:
        return _make_error("VALUE_NOT_NUMBER", f"Invalid number: {value_str}")

    if unit not in _SUPPORTED_UNITS:
        return _make_error("UNKNOWN_UNIT", f"Unknown unit: {unit}")

    if value < 0:
        return _make_error("NEGATIVE_VALUE", "Negative value not allowed")

    return value


def convert_length(input_str: str) -> dict:
    parsed = _parse_format(input_str)
    if isinstance(parsed, dict):
        return parsed

    unit, value_str = parsed
    validated = _validate_unit_and_value(unit, value_str)
    if isinstance(validated, dict):
        return validated

    conversions = convert_all_units(unit, validated)
    return {
        "ok": True,
        "source": {"unit": unit, "value": validated},
        "conversions": conversions,
    }
