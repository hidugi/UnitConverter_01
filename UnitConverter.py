import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from boundary.cli import run


def main() -> None:
    input_str = input("Insert value for converting (ex: meter:2.5): ")
    run(input_str)


if __name__ == "__main__":
    main()
