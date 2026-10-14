#!/usr/bin/env python3
"""Build a fixed-calendar OpenRouter advertised-price index.

The basket is the 30 models with the most OpenRouter tokens in the 30 UTC days
ending 2026-03-14.  Their *March* token volumes are the weights for every
subsequent month.  This deliberately does not substitute later launches into
the basket or annualise each model's time since launch.

Input data are pinned public Git commits.  The script writes an auditable CSV
next to this file; it makes no claim that an OpenRouter routing price is a
provider's direct-contract price.
"""

from __future__ import annotations

import csv
import json
import subprocess
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
PRICES_URL = (
    "https://api.github.com/repos/jvrck/openrouterlist/contents/data/history/"
    "prices.json?ref=6ffc63058b581c2e4f4bed1f2c68afa163fb29e6"
)
START = date(2026, 3, 14)
END = date(2026, 9, 13)
MONTH_ENDS = [START, date(2026, 4, 13), date(2026, 5, 13), date(2026, 6, 13),
              date(2026, 7, 13), date(2026, 8, 13), END]

# These are the 30-day (2026-02-13--03-14 UTC inclusive) token totals from
# IAPS-AI/OpenRouter-OS-Rankings commit 9ca669e36c5c3c908402e013b53c4449622e0cfe.
# Keeping the observed basket literal prevents
# a later upstream rebuild from silently changing the historical index.
BASKET = [
    ("minimax/minimax-m2.5-20260211", 9005763123986),
    ("google/gemini-3-flash-preview-20251217", 4157725202051),
    ("deepseek/deepseek-v3.2-20251201", 3564071834045),
    ("moonshotai/kimi-k2.5-0127", 3428935123901),
    ("anthropic/claude-4.6-opus-20260205", 2976920775733),
    ("stepfun/step-3.5-flash:free", 2855096986773),
    ("x-ai/grok-4.1-fast", 2560515470922),
    ("z-ai/glm-5-20260211", 2419450887938),
    ("anthropic/claude-4.6-sonnet-20260217", 2403364025209),
    ("anthropic/claude-4.5-sonnet-20250929", 2164948036499),
    ("google/gemini-2.5-flash", 2124292853876),
    ("arcee-ai/trinity-large-preview:free", 2104131322108),
    ("google/gemini-2.5-flash-lite", 1759452749456),
    ("openai/gpt-oss-120b", 1643128321764),
    ("openai/gpt-5-nano-2025-08-07", 1172664790984),
    ("anthropic/claude-4.5-haiku-20251001", 797604823425),
    ("google/gemini-2.0-flash-001", 702378637587),
    ("google/gemini-3.1-pro-preview-20260219", 701915874499),
    ("openai/gpt-5.2-20251211", 680116591271),
    ("openai/gpt-4o-mini", 639352806821),
    ("minimax/minimax-m2.1", 598958086412),
    ("xiaomi/mimo-v2-flash-20251210", 519647774839),
    ("x-ai/grok-4-fast", 501953750603),
    ("openai/gpt-5-mini-2025-08-07", 493677301466),
    ("anthropic/claude-4.5-opus-20251124", 482069680760),
    ("z-ai/glm-4.7-20251222", 465894264077),
    ("google/gemini-3-pro-preview-20251117", 455660096247),
    ("openrouter/hunter-alpha", 431542062919),
    ("google/gemini-2.5-pro", 387350830242),
    ("qwen/qwen3-235b-a22b-07-25", 385738553005),
]

# Ranking permaslugs contain dated deployment identifiers; price history uses
# the provider's stable model ID.  Free/stealth rows intentionally have no map.
PRICE_ID = {
    "minimax/minimax-m2.5-20260211": "minimax/minimax-m2.5",
    "google/gemini-3-flash-preview-20251217": "google/gemini-3-flash-preview",
    "deepseek/deepseek-v3.2-20251201": "deepseek/deepseek-v3.2",
    "moonshotai/kimi-k2.5-0127": "moonshotai/kimi-k2.5",
    "anthropic/claude-4.6-opus-20260205": "anthropic/claude-opus-4.6",
    "x-ai/grok-4.1-fast": "x-ai/grok-4.1-fast",
    "z-ai/glm-5-20260211": "z-ai/glm-5",
    "anthropic/claude-4.6-sonnet-20260217": "anthropic/claude-sonnet-4.6",
    "anthropic/claude-4.5-sonnet-20250929": "anthropic/claude-sonnet-4.5",
    "google/gemini-2.5-flash": "google/gemini-2.5-flash",
    "google/gemini-2.5-flash-lite": "google/gemini-2.5-flash-lite",
    "openai/gpt-oss-120b": "openai/gpt-oss-120b",
    "openai/gpt-5-nano-2025-08-07": "openai/gpt-5-nano",
    "anthropic/claude-4.5-haiku-20251001": "anthropic/claude-haiku-4.5",
    "google/gemini-2.0-flash-001": "google/gemini-2.0-flash-001",
    "google/gemini-3.1-pro-preview-20260219": "google/gemini-3.1-pro-preview",
    "openai/gpt-5.2-20251211": "openai/gpt-5.2",
    "openai/gpt-4o-mini": "openai/gpt-4o-mini",
    "minimax/minimax-m2.1": "minimax/minimax-m2.1",
    "xiaomi/mimo-v2-flash-20251210": "xiaomi/mimo-v2-flash",
    "x-ai/grok-4-fast": "x-ai/grok-4-fast",
    "openai/gpt-5-mini-2025-08-07": "openai/gpt-5-mini",
    "anthropic/claude-4.5-opus-20251124": "anthropic/claude-opus-4.5",
    "z-ai/glm-4.7-20251222": "z-ai/glm-4.7",
    "google/gemini-3-pro-preview-20251117": "google/gemini-3-pro-preview",
    "google/gemini-2.5-pro": "google/gemini-2.5-pro",
    "qwen/qwen3-235b-a22b-07-25": "qwen/qwen3-235b-a22b-07-25",
}


def fetch_json(url: str) -> object:
    # curl uses the workstation's certificate store; the bundled Python on this
    # host does not.  No credentials are sent and the URL pins the git commit.
    result = subprocess.run(
        ["curl", "-L", "-sS", "--compressed", "--max-time", "120",
         "-H", "Accept: application/vnd.github.raw+json", url],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)


def price_on(points: list[list[object]], on: date) -> tuple[float, float] | None:
    """Last recorded price no later than `on`; zero/free offers are excluded."""
    eligible = [point for point in points if date.fromisoformat(str(point[0])) <= on]
    if not eligible:
        return None
    point = eligible[-1]
    input_price, output_price = float(point[1]), float(point[2])
    return (input_price, output_price) if input_price > 0 and output_price > 0 else None


def main() -> None:
    prices = fetch_json(PRICES_URL)["models"]
    basket = BASKET

    output = DATA / "openrouter_fixed_march30_monthly_price_index_2026-09-13.csv"
    rows: list[dict[str, object]] = []
    for rank, (slug, volume) in enumerate(basket, start=1):
        model_id = PRICE_ID.get(slug, "")
        history = prices.get(model_id, {}) if model_id else {}
        points = history.get("points", [])
        row: dict[str, object] = {
            "rank_march30d": rank,
            "ranked_model_permaslug": slug,
            "price_history_model_id": model_id,
            "march30d_token_volume": f"{volume:.0f}",
            "present_on_2026_09_13": history.get("present_now", ""),
            "exclusion_reason": "" if model_id else "free_or_stealth_or_no_stable_price_id",
        }
        for endpoint in MONTH_ENDS:
            value = price_on(points, endpoint)
            key = endpoint.isoformat().replace("-", "_")
            row[f"input_{key}_usd_per_m"] = "" if value is None else f"{value[0]:.8g}"
            row[f"output_{key}_usd_per_m"] = "" if value is None else f"{value[1]:.8g}"
        rows.append(row)

    fields = list(rows[0])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    full_volume = sum(volume for _, volume in basket)
    # A model removed before the end date does not have a September list price.
    # Do not carry its stale last price forward: this is a continuing-model
    # price index, and removal is reported as coverage loss rather than a 0% move.
    common = [
        row for row in rows
        if row["present_on_2026_09_13"] is True
        and all(row[f"input_{d.isoformat().replace('-', '_')}_usd_per_m"]
                and row[f"output_{d.isoformat().replace('-', '_')}_usd_per_m"]
                for d in MONTH_ENDS)
    ]
    covered = sum(float(row["march30d_token_volume"]) for row in common)
    print(f"fixed March Top-30 volume: {full_volume / 1e12:.3f}T tokens")
    print(f"continuing, all-seven-endpoint priced coverage: {covered / 1e12:.3f}T ({covered / full_volume:.1%}), {len(common)} models")
    for metric in ("input", "output"):
        print(f"\n{metric} price index, weights fixed on 2026-03-14:")
        base = None
        previous = None
        for endpoint in MONTH_ENDS:
            key = endpoint.isoformat().replace("-", "_")
            mean = sum(float(row["march30d_token_volume"]) * float(row[f"{metric}_{key}_usd_per_m"]) for row in common) / covered
            if base is None:
                base = mean
            month_change = "base" if previous is None else f"{mean / previous - 1:+.1%} MoM"
            print(f"{endpoint}: ${mean:.4g}/M, index {mean / base * 100:.1f}, cumulative {mean / base - 1:+.1%}, {month_change}")
            previous = mean
        elapsed_days = (END - START).days
        weekly = (mean / base) ** (7 / elapsed_days) - 1
        print(f"six-month geometric weekly equivalent: {weekly:+.3%} (not a claim of a constant weekly price cut)")


if __name__ == "__main__":
    main()
