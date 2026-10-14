from pathlib import Path
import json

def main():
    data = json.loads((Path(__file__).resolve().parent / "data/revenue_inputs_20261005.json").read_text())
    rows = data["rows"]
    for year, values in rows.items():
        assert sum(values[:4]) == values[4], (year, "收入分类不平")
        assert sum(values[5:]) == values[4], (year, "分部抵销不平")
    for i, name in enumerate(data["keys"]):
        if i == 8:
            continue
        growth24 = (rows["2024"][i] / rows["2023"][i] - 1) * 100
        growth25 = (rows["2025"][i] / rows["2024"][i] - 1) * 100
        cagr = ((rows["2025"][i] / rows["2023"][i]) ** 0.5 - 1) * 100
        h1 = (rows["2026H1"][i] / rows["2025H1"][i] - 1) * 100
        print(f"{name}: 2024同比 {growth24:.2f}%, 2025同比 {growth25:.2f}%, 两年CAGR {cagr:.2f}%, 2026H1同比 {h1:.2f}%")
    for year in ["2023", "2024", "2025"]:
        r = rows[year]
        print(f"{year}服务占比 {(r[2]+r[3])/r[4]*100:.2f}%")
    print("✅ 五个期间分类与分部收入均勾稽一致")

if __name__ == "__main__":
    main()
