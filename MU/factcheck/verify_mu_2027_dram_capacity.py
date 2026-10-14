#!/usr/bin/env python3
"""Reproduce the strict lower-bound calculation in MU capacity research.

This is not a forecast of Micron's total output.  It only converts the public
relative Tongluo Phase 1 statement into WSPM and annual-average equivalents.
"""

from __future__ import annotations

import csv
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


DATA_FILE = Path(__file__).with_name("data") / "mu_2027_dram_capacity_source_register.csv"


def one_decimal(value: float) -> str:
    """Use conventional half-up rounding so the report and script agree."""
    return str(Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def load_numeric_inputs() -> dict[str, float]:
    with DATA_FILE.open(newline="", encoding="utf-8") as source_file:
        rows = {row["input_id"]: row["value"] for row in csv.DictReader(source_file)}
    return {
        "base_low": float(rows["micron_q4_2026_dram_wspm_low"]),
        "base_high": float(rows["micron_q4_2026_dram_wspm_high"]),
        "tongluo_share": float(rows["tongluo_phase1_share_lower_bound"]),
    }


def main() -> None:
    inputs = load_numeric_inputs()
    base_range = (inputs["base_low"], inputs["base_high"])
    share = inputs["tongluo_share"]

    tongluo_end = tuple(base * share for base in base_range)
    print("# Micron Tongluo Phase 1: strict lower-bound calculation")
    print(f"2026Q4 DRAM baseline (third-party): {base_range[0]:.0f}–{base_range[1]:.0f} kWSPM")
    print(
        "Tongluo 2027H2 end run-rate lower bound: "
        f">{one_decimal(tongluo_end[0])}–>{one_decimal(tongluo_end[1])} kWSPM"
    )
    print()
    print("| 2027 timing assumption | Average incremental WSPM lower bound | Normalized capacity increase |")
    print("|---|---:|---:|")
    for name, average_factor in (
        ("H2 linear ramp / Q4 stable output", 0.25),
        ("Stable from July", 0.50),
    ):
        average_increment = tuple(value * average_factor for value in tongluo_end)
        print(
            f"| {name} | >{one_decimal(average_increment[0])}–>{one_decimal(average_increment[1])} kWSPM "
            f"| >{share * average_factor * 100:.1f}% |"
        )
    print()
    print("Idaho Fab 1 is deliberately excluded: public information gives first-wafer timing, not WSPM.")


if __name__ == "__main__":
    main()
