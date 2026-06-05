"""Boundary PyQt GUI — visual adapter (PRD §5.1)."""

from __future__ import annotations

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from control.convert_length import convert_length

_SUPPORTED_UNITS = ("meter", "feet", "yard")


class UnitConverterWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Unit Converter")
        self.setMinimumSize(420, 320)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        input_group = QGroupBox("Input")
        form = QFormLayout(input_group)

        self._unit_combo = QComboBox()
        self._unit_combo.addItems(_SUPPORTED_UNITS)
        form.addRow("Unit:", self._unit_combo)

        self._value_spin = QDoubleSpinBox()
        self._value_spin.setRange(0.0, 1_000_000.0)
        self._value_spin.setDecimals(4)
        self._value_spin.setValue(2.5)
        self._value_spin.setSingleStep(0.1)
        form.addRow("Value:", self._value_spin)

        layout.addWidget(input_group)

        button_row = QHBoxLayout()
        self._convert_btn = QPushButton("Convert")
        self._convert_btn.clicked.connect(self._on_convert)
        button_row.addStretch()
        button_row.addWidget(self._convert_btn)
        layout.addLayout(button_row)

        output_group = QGroupBox("Results")
        output_layout = QVBoxLayout(output_group)
        self._result_view = QTextEdit()
        self._result_view.setReadOnly(True)
        self._result_view.setPlaceholderText("Conversion results appear here.")
        output_layout.addWidget(self._result_view)
        layout.addWidget(output_group)

        hint = QLabel("Format equivalent: unit:value (ex: meter:2.5)")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet("color: gray;")
        layout.addWidget(hint)

    def _on_convert(self) -> None:
        unit = self._unit_combo.currentText()
        value = self._value_spin.value()
        input_str = f"{unit}:{value}"

        result = convert_length(input_str)
        if not result["ok"]:
            message = result.get("message", result.get("error", "Error"))
            self._result_view.clear()
            QMessageBox.warning(self, "Conversion Error", message)
            return

        source = result["source"]
        lines = [
            f"{source['value']} {source['unit']} = {item['value']} {item['unit']}"
            for item in result["conversions"]
        ]
        self._result_view.setPlainText("\n".join(lines))


def run_gui() -> None:
    app = QApplication(sys.argv)
    window = UnitConverterWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()
