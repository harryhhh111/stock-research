#!/usr/bin/env python3
"""Recompute the token-volume-weighted launch-to-current price index."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path


DATA = Path(__file__).with_name("data") / "openrouter_top10_price_index_2026-09-13.csv"


def weighted_change(rows: list[dict[str, str]], field: str) -> float:
    eligible = [row for row in rows if row["index_eligible"] == "yes"]
    denominator = sum(float(row["token_volume_30d_t"]) for row in eligible)
    numerator = sum(
        float(row["token_volume_30d_t"]) * float(row[field]) for row in eligible
    )
    return numerator / denominator


def weekly_rate(row: dict[str, str], metric: str) -> float:
    """Geometric price change per seven days over the observed lifetime."""
    start = float(row[f"first_{metric}_usd_per_m"])
    end = float(row[f"last_{metric}_usd_per_m"])
    days = (
        date.fromisoformat(row["last_price_date"])
        - date.fromisoformat(row["first_price_date"])
    ).days
    assert start > 0 and end > 0 and days > 0
    return (end / start) ** (7 / days) - 1


def weighted_weekly_rate(rows: list[dict[str, str]], metric: str) -> float:
    eligible = [row for row in rows if row["index_eligible"] == "yes"]
    denominator = sum(float(row["token_volume_30d_t"]) for row in eligible)
    numerator = sum(
        float(row["token_volume_30d_t"]) * weekly_rate(row, metric)
        for row in eligible
    )
    return numerator / denominator


def main() -> None:
    with DATA.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 10
    assert [int(row["rank"]) for row in rows] == list(range(1, 11))

    total_top10 = sum(float(row["token_volume_30d_t"]) for row in rows)
    paid_coverage = sum(
        float(row["token_volume_30d_t"])
        for row in rows
        if row["index_eligible"] == "yes"
    )
    input_change = weighted_change(rows, "input_change_pct")
    output_change = weighted_change(rows, "output_change_pct")
    input_weekly = weighted_weekly_rate(rows, "input")
    output_weekly = weighted_weekly_rate(rows, "output")

    print(f"top-10 volume: {total_top10:.1f}T tokens")
    print(f"paid-model coverage: {paid_coverage / total_top10:.1%}")
    print(f"weighted input change: {input_change:.1f}%")
    print(f"weighted output change: {output_change:.1f}%")
    print(f"weighted geometric weekly input change: {input_weekly:.1%}")
    print(f"weighted geometric weekly output change: {output_weekly:.1%}")


if __name__ == "__main__":
    main()
