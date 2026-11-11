#!/usr/bin/env python3
"""Recompute FY2026 research tables from a dated, source-linked transcription.

Run from any directory. All currency inputs except EPS are USD millions.
No network access or file writes; assertions check internal reconciliation only,
not the truth of the source disclosures or future estimates.
"""
import json
from pathlib import Path

INPUT = Path(__file__).resolve().parent / "data" / "fy2026_update_inputs.json"


def growth(current, prior):
    return (current / prior - 1) * 100


def main():
    d = json.loads(INPUT.read_text(encoding="utf-8"))
    a = d["annuals"]
    q = d["quarters"]
    b = d["balance"]
    price = d["market"]["close"]
    for year, values in a.items():
        assert sum(values[k] for k in ("dram", "nand", "other")) == values["revenue"]
        assert sum(s[year] for s in d["segments"].values()) == values["revenue"]
    for metric in ("revenue", "net_income", "dram", "nand", "other"):
        assert sum(q[k][metric] for k in ("q1", "q2", "q3", "q4")) == a["2026"][metric]
    for k in ("q1", "q2", "q3", "q4"):
        assert sum(s[k] for s in d["segments"].values()) == q[k]["revenue"]
    for s in d["segments"].values():
        assert sum(s[k] for k in ("q1", "q2", "q3", "q4")) == s["2026"]
    assert sum(s["op_2026"] for s in d["segments"].values()) - 1851 == a["2026"]["operating_income"]
    annual_metrics = {}
    for year, values in a.items():
        annual_metrics[year] = {
            "gross_margin_pct": values["gross_profit"] / values["revenue"] * 100,
            "operating_margin_pct": values["operating_income"] / values["revenue"] * 100,
            "net_margin_pct": values["net_income"] / values["revenue"] * 100,
            "standard_fcf_million": values["cfo"] - values["cash_capex"],
            "rd_to_revenue_pct": values["rd"] / values["revenue"] * 100,
        }
        if "asset_sales" in values:
            netcapex = values["cash_capex"] - values["incentives"] - values["asset_sales"]
            annual_metrics[year].update(net_capex_million=netcapex, adjusted_fcf_million=values["cfo"]-netcapex)
    spot = json.loads(INPUT.with_name("price_snapshot_2026-10-27.json").read_text(encoding="utf-8"))
    spot_metrics = {row["item"]: growth(row["average"], row["old_average"]) for row in spot["rows"]}
    q4_metrics = {k: {"qoq_pct": growth(q["q4"][k], q["q3"][k]), "yoy_pct": growth(q["q4"][k], q["q4_prior"][k])} for k in ("revenue", "net_income", "eps", "dram", "nand", "other")}
    segment_metrics = {name: {
        "q4_share_pct": s["q4"] / q["q4"]["revenue"] * 100,
        "q4_qoq_pct": growth(s["q4"], s["q3"]),
        "q4_yoy_pct": growth(s["q4"], s["q4_prior"]),
        "fy2026_share_pct": s["2026"] / a["2026"]["revenue"] * 100,
        "fy2026_yoy_pct": growth(s["2026"], s["2025"]),
        "fy2025_yoy_pct": growth(s["2025"], s["2024"]),
        "fy2026_op_margin_pct": s["op_2026"] / s["2026"] * 100,
        "q4_increment_share_pct": (s["q4"] - s["q3"]) / (q["q4"]["revenue"]-q["q3"]["revenue"]) * 100,
    } for name, s in d["segments"].items()}
    cap = price * b["shares"] / 1e6
    debt = b["debt_current"] + b["debt_long"]
    liquid = b["cash"] + b["short_investments"] + b["long_investments"]
    netcash = liquid - debt
    ev = cap - netcash
    val = {
        "market_cap_million": cap, "net_cash_ex_restricted_million": netcash,
        "company_net_cash_including_restricted_million": netcash+b["restricted_cash"],
        "ev_million": ev, "gaap_trailing_pe": price/a["2026"]["eps"],
        "adjusted_trailing_pe": price/a["2026"]["adjusted_eps"],
        "fy2027_adjusted_forward_pe": price/d["consensus"]["fy2027_adjusted_eps"],
        "q1_gaap_annualized_pe": price/(d["guidance"]["gaap_eps"]*4),
        "pb": cap/b["equity_end"], "ps": cap/a["2026"]["revenue"],
        "ev_sales": ev/a["2026"]["revenue"],
        "standard_fcf_yield_pct": annual_metrics["2026"]["standard_fcf_million"]/cap*100,
        "adjusted_fcf_yield_pct": annual_metrics["2026"]["adjusted_fcf_million"]/cap*100,
        "roe_pct": a["2026"]["net_income"]/((b["equity_begin"]+b["equity_end"])/2)*100,
        "roa_pct": a["2026"]["net_income"]/((b["assets_begin"]+b["assets_end"])/2)*100,
    }
    print(json.dumps({"check": "PASS: annual/product/segment/quarter reconciliation", "annual_metrics": annual_metrics,
        "fy2026_yoy_pct": {k:growth(a["2026"][k],a["2025"][k]) for k in ("revenue","net_income","eps","rd","cash_capex","cfo")},
        "q4_metrics": q4_metrics, "segment_metrics": segment_metrics, "valuation": val,
        "price_snapshot_change_pct": spot_metrics,
        "additional_checks": {
            "fy2026_operating_income_yoy_pct": growth(a["2026"]["operating_income"], a["2025"]["operating_income"]),
            "standard_fcf_yoy_pct": growth(annual_metrics["2026"]["standard_fcf_million"], annual_metrics["2025"]["standard_fcf_million"]),
            "net_capex_yoy_pct": growth(annual_metrics["2026"]["net_capex_million"], annual_metrics["2025"]["net_capex_million"]),
            "adjusted_fcf_yoy_pct": growth(annual_metrics["2026"]["adjusted_fcf_million"], annual_metrics["2025"]["adjusted_fcf_million"]),
            "cip_yoy_pct": growth(b["cip_end"],b["cip_begin"]),
            "fy2027_capex_50bn_threshold_yoy_pct": growth(50000,annual_metrics["2026"]["net_capex_million"]),
            "old_fixed_22_1_pe_rebased_gaap_price": a["2026"]["eps"]*1.5*22.1,
        },
        "scenarios": {str(eps): {str(pe): round(eps*pe,2) for pe in (4,5,6,8,10)} for eps in (100,140,176.58,210)},
        "note": "Annual EPS uses annual weighted shares; quarterly rounded EPS must not be substituted for it."}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
