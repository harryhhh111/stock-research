#!/usr/bin/env python3
"""Estimate list-price billings for the OpenRouter rolling-30-day Top-10.

This is deliberately not a revenue estimate for OpenRouter or a model lab:
rankings-daily exposes only total tokens, not input/output tokens, discounts,
cached-token billing, or the router/lab revenue split.  It reports a transparent
3:1 input/output *published-list-price* scenario and all-input/all-output bounds.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections import defaultdict
from datetime import date, timedelta


RANK_COMMIT = "f0e8f5b17aca"
PRICE_COMMIT = "cd5e7288b779"
RANK_URL = (
    "https://raw.githubusercontent.com/IAPS-AI/OpenRouter-OS-Rankings/"
    f"{RANK_COMMIT}/data/rankings-2026.json"
)
PRICE_URL = (
    "https://api.github.com/repos/jvrck/openrouterlist/contents/data/history/"
    f"prices.json?ref={PRICE_COMMIT}"
)
ENDPOINTS = [date(2026, month, 10) for month in range(4, 10)] + [date(2026, 10, 8)]
WINDOW_DAYS = 30
INPUT_SHARE = 0.75
PRICE_ID_OVERRIDES = {
    "anthropic/claude-4.6-sonnet-20260217": "anthropic/claude-sonnet-4.6",
    "anthropic/claude-4.6-opus-20260205": "anthropic/claude-opus-4.6",
    "anthropic/claude-4.7-opus-20260416": "anthropic/claude-opus-4.7",
    "anthropic/claude-4.8-opus-20260528": "anthropic/claude-opus-4.8",
}


def fetch_json(url: str) -> dict:
    result = subprocess.run(
        ["curl", "-L", "-sS", "--compressed", "--max-time", "120",
         "-H", "Accept: application/vnd.github.raw+json", url],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)


def price_id(slug: str, models: dict) -> str | None:
    """Map dated rankings permaslugs to the matching price-history model ID."""
    if slug == "other" or slug.startswith(("stealth/", "openrouter/")):
        return None
    if ":free" in slug:
        return "__FREE__"
    if slug in PRICE_ID_OVERRIDES:
        return PRICE_ID_OVERRIDES[slug]
    candidates = [slug]
    base = slug.split(":", 1)[0]
    candidates.append(base)
    candidates.append(re.sub(r"-\d{8}$", "", base))
    candidates.append(re.sub(r"-\d{4}-\d{2}-\d{2}$", "", base))
    for candidate in candidates:
        if candidate in models:
            return candidate
    return None


def price_on(points: list[list[object]], on: date) -> tuple[float, float] | None:
    observed = [point for point in points if date.fromisoformat(str(point[0])) <= on]
    if not observed:
        return None
    point = observed[-1]
    return float(point[1]), float(point[2])


def main() -> None:
    rankings = fetch_json(RANK_URL)["data"]
    price_models = fetch_json(PRICE_URL)["models"]
    by_day: defaultdict[date, list[tuple[str, int]]] = defaultdict(list)
    for row in rankings:
        by_day[date.fromisoformat(row["date"])].append((row["model_permaslug"], int(row["total_tokens"])))

    print("window_end,rank,model_permaslug,tokens_30d_t,price_id,pricing_status,input_price_end_usd_per_m,output_price_end_usd_per_m,list_billings_3to1_io_usd_m,all_input_usd_m,all_output_usd_m,priced_token_coverage")
    for end in ENDPOINTS:
        days = [end - timedelta(days=i) for i in range(WINDOW_DAYS)]
        totals: defaultdict[str, int] = defaultdict(int)
        for day in days:
            for slug, tokens in by_day[day]:
                totals[slug] += tokens
        top10 = sorted(
            ((slug, tokens) for slug, tokens in totals.items() if slug != "other"),
            key=lambda pair: pair[1], reverse=True,
        )[:10]
        top10_tokens = sum(tokens for _, tokens in top10)
        priced_tokens = 0
        aggregate_low = aggregate_base = aggregate_high = 0.0
        for rank, (slug, tokens) in enumerate(top10, start=1):
            model_id = price_id(slug, price_models)
            is_free = model_id == "__FREE__"
            points = ([['1900-01-01', 0, 0]] if is_free else
                      price_models.get(model_id, {}).get("points", []) if model_id else [])
            end_price = price_on(points, end)
            status = "free_zero_list_price" if is_free else ("matched" if end_price is not None else "not_publicly_priced")
            low = base = high = None
            model_priced_tokens = 0
            # Price each day at the last historically recorded price, so a model
            # price change inside the 30-day ranking window is not backfilled.
            for day in days:
                day_tokens = dict(by_day[day]).get(slug, 0)
                day_price = price_on(points, day)
                if day_tokens and day_price is not None:
                    priced_tokens += day_tokens
                    model_priced_tokens += day_tokens
                    input_price, output_price = day_price
                    if low is None:
                        low = base = high = 0.0
                    low += day_tokens / 1e6 * input_price
                    base += day_tokens / 1e6 * (INPUT_SHARE * input_price + (1 - INPUT_SHARE) * output_price)
                    high += day_tokens / 1e6 * output_price
            input_end = "" if end_price is None else f"{end_price[0]:.8g}"
            output_end = "" if end_price is None else f"{end_price[1]:.8g}"
            low_s = "" if low is None else f"{low / 1e6:.4f}"
            base_s = "" if base is None else f"{base / 1e6:.4f}"
            high_s = "" if high is None else f"{high / 1e6:.4f}"
            if low is not None:
                aggregate_low += low
                aggregate_base += base
                aggregate_high += high
            print(
                f"{end},{rank},{slug},{tokens / 1e12:.6f},{'' if is_free else model_id or ''},{status},{input_end},{output_end},"
                f"{base_s},{low_s},{high_s},"
                f"{model_priced_tokens / tokens:.1%}"
            )
        print(
            f"{end},TOTAL,top10_aggregate,{top10_tokens / 1e12:.6f},,,,,"
            f"{aggregate_base / 1e6:.4f},{aggregate_low / 1e6:.4f},{aggregate_high / 1e6:.4f},"
            f"{priced_tokens / top10_tokens:.1%}"
        )


if __name__ == "__main__":
    main()
