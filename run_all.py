from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

COMMANDS = [
    [sys.executable, "-m", "src.simulate", "--output", "data/synthetic_liver_chip.csv", "--seed", "42"],
    [sys.executable, "evaluate.py"],
    [sys.executable, "run_demo.py"],
    [sys.executable, "make_figures.py"],
    [sys.executable, "benchmark_active_learning.py"],
    [sys.executable, "-m", "pytest", "-q"],
]


def main() -> None:
    for command in COMMANDS:
        print("+", " ".join(command), flush=True)
        subprocess.run(command, cwd=ROOT, check=True)
    print("\nAll reproducibility steps completed successfully.")


if __name__ == "__main__":
    main()
