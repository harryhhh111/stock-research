#!/usr/bin/env python3
"""Recompute OpenRouter public-token growth from a pinned daily-data commit.

The source provides the top 50 public model variants plus a daily ``other``
row.  Summing every row per UTC date therefore yields the published total of
public text-token traffic represented by that dataset, not the global LLM
market or private OpenRouter traffic.
"""

from __future__ import annotations

import json
import math
import subprocess
from collections import defaultdict
from datetime import date, timedelta


COMMIT = "f0e8f5b17aca"
URL = (
    "https://raw.githubusercontent.com/IAPS-AI/OpenRouter-OS-Rankings/"
    f"{COMMIT}/data/rankings-2026.json"
)
START = date(2026, 4, 10)
END = date(2026, 10, 8)
WINDOW_DAYS = 30


def fetch() -> dict:
    result = subprocess.run(
        ["curl", "-L", "-sS", "--compressed", "--max-time", "120", URL],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    payload = fetch()
    daily: defaultdict[date, int] = defaultdict(int)
    for row in payload["data"]:
        daily[date.fromisoformat(row["date"])] += int(row["total_tokens"])

    expected = list(START - timedelta(days=WINDOW_DAYS - 1) + timedelta(days=i)
                    for i in range((END - (START - timedelta(days=WINDOW_DAYS - 1))).days + 1))
    missing = [day for day in expected if day not in daily]
    assert not missing, missing

    def rolling(end: date) -> int:
        return sum(daily[end - timedelta(days=i)] for i in range(WINDOW_DAYS))

    # Calendar month spacing is used for an interpretable month-over-month table.
    endpoints = [date(2026, month, 10) for month in range(4, 10)] + [END]
    values = [(day, rolling(day)) for day in endpoints]
    print(f"source commit: {COMMIT}; data through {END}; UTC; 30-day rolling sums")
    print("end_date\ttrailing_30d_tokens_T\tchange_vs_prior\tannualized_doubling_days")
    prior_day, prior_value = None, None
    for day, value in values:
        if prior_value is None:
            change, doubling = "base", ""
        else:
            elapsed = (day - prior_day).days
            ratio = value / prior_value
            change = f"{ratio - 1:+.1%}"
            doubling = f"{math.log(2) / math.log(ratio) * elapsed:.1f}" if ratio > 1 else "N/A"
        print(f"{day}\t{value / 1e12:.3f}\t{change}\t{doubling}")
        prior_day, prior_value = day, value

    start_value, end_value = values[0][1], values[-1][1]
    elapsed = (END - START).days
    six_month_ratio = end_value / start_value
    six_month_doubling = math.log(2) / math.log(six_month_ratio) * elapsed
    print()
    print(f"{START} to {END}: {start_value / 1e12:.3f}T -> {end_value / 1e12:.3f}T; "
          f"{six_month_ratio:.2f}x; implied doubling every {six_month_doubling:.1f} days")

    recent_start = END - timedelta(days=60)
    recent_ratio = rolling(END) / rolling(recent_start)
    recent_doubling = math.log(2) / math.log(recent_ratio) * 60
    print(f"{recent_start} to {END}: {rolling(recent_start) / 1e12:.3f}T -> {end_value / 1e12:.3f}T; "
          f"{recent_ratio:.2f}x; implied doubling every {recent_doubling:.1f} days")


if __name__ == "__main__":
    main()
