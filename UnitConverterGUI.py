import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from boundary.gui import run_gui


if __name__ == "__main__":
    run_gui()
