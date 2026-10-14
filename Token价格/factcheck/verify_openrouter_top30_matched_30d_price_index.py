#!/usr/bin/env python3
"""Recompute the matched 29-day price change for the current usage Top-30."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path


DATA = Path(__file__).with_name("data") / "openrouter_top30_matched_30d_price_index_2026-09-13.csv"
ADJUSTMENTS = Path(__file__).with_name("data") / "openrouter_top30_price_signal_adjustments_2026-09-13.csv"


def weighted(
    rows: list[dict[str, str]], metric: str, neutralized: set[str] | None = None
) -> float:
    start = f"start_{metric}_usd_per_m"
    end = f"end_{metric}_usd_per_m"
    denominator = sum(float(row["token_volume_30d_t"]) for row in rows)
    return sum(
        float(row["token_volume_30d_t"])
        * (
            0
            if neutralized and row["ranked_model_permaslug"] in neutralized
            else float(row[end]) / float(row[start]) - 1
        )
        for row in rows
    ) / denominator


def main() -> None:
    with DATA.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    with ADJUSTMENTS.open(encoding="utf-8", newline="") as handle:
        adjustments = list(csv.DictReader(handle))

    assert len(rows) == 19
    assert all(row["window_start_date"] == "2026-08-15" for row in rows)
    assert all(row["window_end_date"] == "2026-09-13" for row in rows)
    covered = sum(float(row["token_volume_30d_t"]) for row in rows)
    full_top30_volume = 400.767608729549
    days = (date(2026, 9, 13) - date(2026, 8, 15)).days
    confirmed_promos = {
        row["ranked_model_permaslug"]
        for row in adjustments
        if row["adjustment_class"] == "confirmed_promotional_step"
    }
    nonstandard_prices = {row["ranked_model_permaslug"] for row in adjustments}

    print(f"matched priced-model coverage: {covered:.3f}T tokens ({covered / full_top30_volume:.1%} of Top-30)")
    for metric in ("input", "output"):
        change = weighted(rows, metric)
        weekly = (1 + change) ** (7 / days) - 1
        print(f"matched {days}-day weighted {metric} change: {change:.1%}")
        print(f"matched geometric weekly {metric} change: {weekly:.1%}")
        promo_neutral = weighted(rows, metric, confirmed_promos)
        print(f"confirmed-promo-neutral {metric} change: {promo_neutral:.1%}")
        standardized = weighted(rows, metric, nonstandard_prices)
        standardized_weekly = (1 + standardized) ** (7 / days) - 1
        print(f"standard-price-normalized {metric} change: {standardized:.1%}")
        print(f"standard-price-normalized weekly {metric} change: {standardized_weekly:.1%}")


if __name__ == "__main__":
    main()
