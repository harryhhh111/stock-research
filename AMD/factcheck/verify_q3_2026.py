"""Recompute the AMD Q3 update from preserved manual inputs. No network or writes."""
import json
from pathlib import Path

data = json.loads((Path(__file__).resolve().parent / "data/2026-11-04-q3-inputs.json").read_text())
quarters = data["quarters"]
current = [quarters[key] for key in ("Q1'26", "Q2'26", "Q3'26")]
for key, expected in data["nine_months_2026"].items():
    if key != "source":
        actual = sum(q[key] for q in current)
        assert actual == expected, (key, actual, expected)
for label, q in quarters.items():
    assert q["cfo"] - q["capex"] == q["fcf"], label
    if "embedded_op" in q:
        assert sum(q[k] for k in ("dc", "client", "gaming", "embedded")) == q["revenue"], label
        assert sum(q[k] for k in ("dc_op", "cg_op", "embedded_op", "all_other_op")) == q["op"], label
    margins = {k: round(q[k] / q["revenue"] * 100, 2) for k in ("gross", "op", "net", "ng_gross", "ng_op", "ng_net", "fcf", "capex")}
    print(label, "margins (%)", margins)
    if "embedded_op" in q:
        print("  segments: share / operating margin (%)", {k: (round(q[k]/q["revenue"]*100, 2), round(q[op]/q[k]*100, 2)) for k, op in (("dc","dc_op"),("embedded","embedded_op"))})
for key in ("revenue", "op", "net", "ng_op", "ng_net", "cfo", "capex", "fcf"):
    q = quarters["Q3'26"][key]
    print("Q3", key, "yoy/qoq (%)", *(round((q/quarters[base][key]-1)*100,2) for base in ("Q3'25", "Q2'26")))
print("TTM Q4'25-Q3'26 ($B)", {k: sum(quarters[p][k] for p in ("Q4'25","Q1'26","Q2'26","Q3'26"))/1000 for k in ("revenue","net","ng_net","cfo","capex","fcf")})
for label, base in data["comparison_revenue_2025"].items():
    q = quarters[label]
    print(label, "revenue / yoy / share", {k: (q[k]/1000, round((q[k]/base[k]-1)*100,2), round(q[k]/q["revenue"]*100,2)) for k in ("dc","client","gaming","embedded")})
g = data["guidance"]
print("FY2026 implicit revenue low/mid/high ($B)", [(data["nine_months_2026"]["revenue"]+g["q4_revenue_mid"]*factor)/1000 for factor in (1-g["relative_range"],1,1+g["relative_range"])])
print("PASS: quarter/cumulative, segment/group, and CFO-CapEx=FCF reconciliation")
