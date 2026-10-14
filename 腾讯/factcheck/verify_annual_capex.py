import json
from pathlib import Path
base = Path(__file__).resolve().parent
data = json.loads((base / "data/annual_capex.json").read_text())
results = [{"year": r["year"], "capex_yoy_pct": (r["capex"] / r["prior_capex"] - 1) * 100, "capex_revenue_pct": r["capex"] / r["revenue"] * 100, "capital_commitments": r["buildings_commitment"] + r["investee_commitment"] + r["other_assets_commitment"]} for r in data["rows"]]
(base / "三年资本开支计算结果.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
print(json.dumps(results, ensure_ascii=False, indent=2))
