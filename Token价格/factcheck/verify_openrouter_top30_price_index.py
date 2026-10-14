#!/usr/bin/env python3
"""Recompute the 30-day-usage-weighted, launch-to-cutoff OpenRouter price index."""

from __future__ import annotations

import csv
from pathlib import Path


DATA = Path(__file__).with_name("data") / "openrouter_top30_price_index_2026-09-13.csv"
ADJUSTMENTS = Path(__file__).with_name("data") / "openrouter_top30_price_signal_adjustments_2026-09-13.csv"


def change_pct(row: dict[str, str], metric: str) -> float:
    start = float(row[f"first_{metric}_usd_per_m"])
    end = float(row[f"last_{metric}_usd_per_m"])
    return (end / start - 1) * 100


def weighted(rows: list[dict[str, str]], value) -> float:
    denominator = sum(float(row["token_volume_30d_t"]) for row in rows)
    return sum(float(row["token_volume_30d_t"]) * value(row) for row in rows) / denominator


def main() -> None:
    with DATA.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    with ADJUSTMENTS.open(encoding="utf-8", newline="") as handle:
        adjustments = list(csv.DictReader(handle))

    assert len(rows) == 30
    assert [int(row["rank"]) for row in rows] == list(range(1, 31))
    eligible = [row for row in rows if row["index_eligible"] == "yes"]
    total = sum(float(row["token_volume_30d_t"]) for row in rows)
    covered = sum(float(row["token_volume_30d_t"]) for row in eligible)
    lifecycle_neutralized = {
        row["ranked_model_permaslug"]
        for row in adjustments
        if row["applies_lifecycle"] == "yes"
    }

    print(f"top-30 volume: {total:.3f}T tokens")
    print(f"priced-model coverage: {covered:.3f}T tokens ({covered / total:.1%})")
    for metric in ("input", "output"):
        print(f"weighted {metric} change: {weighted(eligible, lambda row: change_pct(row, metric)):.1f}%")
        normalized = weighted(
            eligible,
            lambda row: 0
            if row["ranked_model_permaslug"] in lifecycle_neutralized
            else change_pct(row, metric),
        )
        print(f"promotion/tier-neutral {metric} change: {normalized:.1f}%")


if __name__ == "__main__":
    main()
