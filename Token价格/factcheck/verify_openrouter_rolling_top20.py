#!/usr/bin/env python3
"""Reproduce public-visible rolling 30-day Top-20 model rankings from OpenRouter data.

The public endpoint exposes the top 50 named public models per day and one
aggregated ``other`` row.  This script ranks named models using their displayed
daily tokens, and reports their share of *all* public tokens (including other).
It cannot recover a named model's traffic on days when that model was below the
daily Top-50 cutoff, so the result is a reproducible public-visible ranking,
not a claim to be a complete market-wide Top-20.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path


RANK_COMMIT = "f0e8f5b17aca"
RANK_URL = (
    "https://raw.githubusercontent.com/IAPS-AI/OpenRouter-OS-Rankings/"
    f"{RANK_COMMIT}/data/rankings-2026.json"
)
PRICE_COMMIT = "cd5e7288b779"
PRICE_URL = (
    "https://raw.githubusercontent.com/jvrck/openrouterlist/"
    f"{PRICE_COMMIT}/data/history/prices.json"
)
WINDOW_DAYS = 30
DEFAULT_ENDPOINTS = [date(2026, month, 10) for month in range(4, 10)] + [date(2026, 10, 8)]
INPUT_SHARE = 0.75
PRICE_ID_OVERRIDES = {
    "anthropic/claude-4.6-sonnet-20260217": "anthropic/claude-sonnet-4.6",
    "anthropic/claude-4.6-opus-20260205": "anthropic/claude-opus-4.6",
    "anthropic/claude-4.7-opus-20260416": "anthropic/claude-opus-4.7",
    "anthropic/claude-4.8-opus-20260528": "anthropic/claude-opus-4.8",
}


def fetch_json(url: str) -> dict:
    result = subprocess.run(
        ["curl", "-L", "-sS", "--compressed", "--max-time", "120", url],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def price_id(slug: str, models: dict) -> str | None:
    """Map dated ranking slugs to IDs in the historical price dataset."""
    if slug.startswith(("stealth/", "openrouter/")):
        return None
    if ":free" in slug:
        return "__FREE__"
    if slug in PRICE_ID_OVERRIDES:
        return PRICE_ID_OVERRIDES[slug]
    base = slug.split(":", 1)[0]
    candidates = [slug, base, re.sub(r"-\d{8}$", "", base), re.sub(r"-\d{4}-\d{2}-\d{2}$", "", base)]
    return next((candidate for candidate in candidates if candidate in models), None)


def price_on(points: list[list[object]], on: date) -> tuple[float, float] | None:
    observed = [point for point in points if date.fromisoformat(str(point[0])) <= on]
    if not observed:
        return None
    point = observed[-1]
    return float(point[1]), float(point[2])


def rolling_top20(
    rows: list[dict[str, str]], price_models: dict, end: date
) -> tuple[list[dict[str, object]], dict[str, object]]:
    by_day: defaultdict[date, list[tuple[str, int]]] = defaultdict(list)
    for row in rows:
        by_day[date.fromisoformat(row["date"])].append(
            (row["model_permaslug"], int(row["total_tokens"]))
        )

    days = [end - timedelta(days=offset) for offset in range(WINDOW_DAYS)]
    model_tokens: defaultdict[str, int] = defaultdict(int)
    days_visible: defaultdict[str, int] = defaultdict(int)
    all_public_tokens = 0
    named_visible_tokens = 0
    other_tokens = 0
    for day in days:
        for slug, tokens in by_day[day]:
            all_public_tokens += tokens
            if slug == "other":
                other_tokens += tokens
            else:
                named_visible_tokens += tokens
                model_tokens[slug] += tokens
                days_visible[slug] += 1

    top20 = sorted(model_tokens.items(), key=lambda item: item[1], reverse=True)[:20]
    top20_tokens = sum(tokens for _, tokens in top20)
    priced_tokens = 0
    aggregate_input = aggregate_base = aggregate_output = 0.0
    result = []
    for rank, (slug, tokens) in enumerate(top20, start=1):
        model_id = price_id(slug, price_models)
        is_free = model_id == "__FREE__"
        points = ([['1900-01-01', 0, 0]] if is_free else
                  price_models.get(model_id, {}).get("points", []) if model_id else [])
        end_price = price_on(points, end)
        priced_model_tokens = 0
        low = base = high = 0.0
        for day in days:
            day_tokens = dict(by_day[day]).get(slug, 0)
            day_price = price_on(points, day)
            if day_tokens and day_price is not None:
                priced_model_tokens += day_tokens
                priced_tokens += day_tokens
                input_price, output_price = day_price
                low += day_tokens / 1e6 * input_price
                base += day_tokens / 1e6 * (INPUT_SHARE * input_price + (1 - INPUT_SHARE) * output_price)
                high += day_tokens / 1e6 * output_price
        aggregate_input += low
        aggregate_base += base
        aggregate_output += high
        if is_free:
            status = "free_zero_list_price"
        elif not priced_model_tokens:
            status = "not_publicly_priced"
        elif priced_model_tokens < tokens:
            status = "partial_historical_price_match"
        else:
            status = "matched"
        result.append(
            {
                "window_end": end.isoformat(),
                "rank": rank,
                "model_permaslug": slug,
                "tokens_30d": tokens,
                "tokens_30d_t": f"{tokens / 1e12:.6f}",
                "days_visible_in_daily_top50": days_visible[slug],
                "share_all_public_tokens": f"{tokens / all_public_tokens:.2%}",
                "share_named_visible_tokens": f"{tokens / named_visible_tokens:.2%}",
                "price_id": "" if is_free else model_id or "",
                "pricing_status": status,
                "input_price_end_usd_per_m": "" if end_price is None else f"{end_price[0]:.8g}",
                "output_price_end_usd_per_m": "" if end_price is None else f"{end_price[1]:.8g}",
                "priced_token_coverage": f"{priced_model_tokens / tokens:.1%}",
                "list_billings_3to1_io_usd_m": "" if not priced_model_tokens else f"{base / 1e6:.4f}",
                "all_input_usd_m": "" if not priced_model_tokens else f"{low / 1e6:.4f}",
                "all_output_usd_m": "" if not priced_model_tokens else f"{high / 1e6:.4f}",
            }
        )
    summary = {
        "window_end": end.isoformat(),
        "all_public_tokens_30d_t": f"{all_public_tokens / 1e12:.6f}",
        "named_visible_tokens_30d_t": f"{named_visible_tokens / 1e12:.6f}",
        "other_tokens_30d_t": f"{other_tokens / 1e12:.6f}",
        "top20_tokens_30d_t": f"{top20_tokens / 1e12:.6f}",
        "top20_share_all_public_tokens": f"{top20_tokens / all_public_tokens:.2%}",
        "top20_share_named_visible_tokens": f"{top20_tokens / named_visible_tokens:.2%}",
        "priced_top20_tokens_30d_t": f"{priced_tokens / 1e12:.6f}",
        "priced_token_coverage": f"{priced_tokens / top20_tokens:.2%}",
        "list_billings_3to1_io_usd_m": f"{aggregate_base / 1e6:.4f}",
        "all_input_usd_m": f"{aggregate_input / 1e6:.4f}",
        "all_output_usd_m": f"{aggregate_output / 1e6:.4f}",
    }
    return result, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True, help="Detailed Top-20 CSV output path")
    parser.add_argument("--summary-output", type=Path, required=True, help="Window summary CSV output path")
    args = parser.parse_args()

    rows = fetch_json(RANK_URL)["data"]
    price_models = fetch_json(PRICE_URL)["models"]
    all_results: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    for end in DEFAULT_ENDPOINTS:
        result, summary = rolling_top20(rows, price_models, end)
        all_results.extend(result)
        summaries.append(summary)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_results[0]))
        writer.writeheader()
        writer.writerows(all_results)
    with args.summary_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)


if __name__ == "__main__":
    main()
