"""Entity-layer length conversion using PRD ratios (INV-02, INV-03)."""

from __future__ import annotations

from entity.ratios import FEET_PER_METER, YARD_PER_METER


def convert_length(unit: str, value: float) -> list[dict[str, float | str]]:
    """Normalize to meter and return all unit conversions (1-decimal rounding)."""
    if unit == "meter":
        meter_value = value
    elif unit == "feet":
        meter_value = value / FEET_PER_METER
    elif unit == "yard":
        meter_value = value / YARD_PER_METER
    else:
        raise ValueError(f"unsupported unit: {unit}")

    meter_display = round(meter_value, 1)

    meter_out = value if unit == "meter" else meter_display
    feet_out = value if unit == "feet" else round(meter_display * FEET_PER_METER, 1)
    yard_out = value if unit == "yard" else round(meter_display * YARD_PER_METER, 1)

    return [
        {"unit": "meter", "value": meter_out},
        {"unit": "feet", "value": feet_out},
        {"unit": "yard", "value": yard_out},
    ]
