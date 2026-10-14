from pathlib import Path
import json

data = json.loads((Path(__file__).resolve().parent / "data/margin_inputs_20261007.json").read_text())
for year, (revenue, cost, op, net, attributable) in data["rows"].items():
    print(year, "毛利/经营利润/合并净利/归母净利率", *(f"{v/revenue*100:.2f}%" for v in [revenue-cost, op, net, attributable]))
a, b = data["rows"]["2024"], data["rows"]["2025"]
print("2025归母净利润同比", f"{(b[4]/a[4]-1)*100:.2f}%")
print("2025经营利润同比", f"{(b[2]/a[2]-1)*100:.2f}%")
