"""Boundary CLI — stdin/stdout adapter (PRD §5.1)."""

from __future__ import annotations

from control.convert_length import convert_length


def run(input_str: str) -> None:
    result = convert_length(input_str)
    if not result["ok"]:
        print(result.get("message", result.get("error", "Error")))
        return

    source = result["source"]
    for item in result["conversions"]:
        print(f"{source['value']} {source['unit']} = {item['value']} {item['unit']}")
