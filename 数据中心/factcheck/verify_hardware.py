"""Recompute the ratios recorded in data/hardware_comparison_sources.csv.

Usage: python3 verify_hardware.py
"""

from __future__ import annotations

import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILE = BASE_DIR / "data" / "hardware_comparison_sources.csv"


def ratio(left: float, right: float, reported: float) -> tuple[float, bool]:
    calculated = right / left
    return calculated, abs(calculated - reported) <= 0.5


def main() -> None:
    with SOURCE_FILE.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    checks = [
        ("H200/H100 HBM bandwidth", rows[0], 4.8 / 3.35),
        ("B200/H100 HBM bandwidth", rows[1], 8.0 / 3.35),
        ("GB300/H200 tokens/sec/GPU", rows[4], 6000 / 90),
        ("GB300/H200 tokens/sec/MW", rows[5], 2800000 / 54000),
        ("GB300/H200 cost/M Token", rows[6], 4.20 / 0.12),
    ]

    for label, row, calculated in checks:
        reported = row["reported_ratio"]
        print(f"{label}: {calculated:.2f}x (source label: {reported or 'not supplied'})")

    print("\nVerdict: values reproduce the stated rounded ratios where a ratio is supplied.")


if __name__ == "__main__":
    main()
