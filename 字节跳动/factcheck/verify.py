"""Recompute reported inputs and explicit scenarios; never infer audited accounts."""
from pathlib import Path
import csv
import json

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DATE = "2026-10-05"


def main():
    with (DATA / f"reported-inputs-{DATE}.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    inputs = {row["id"]: float(row["value"]) for row in rows}
    sources = json.loads((DATA / f"sources-{DATE}.json").read_text(encoding="utf-8"))
    source_ids = {s["id"] for s in sources}
    for row in rows:
        if not set(row["source_ids"].split(";")) <= source_ids:
            raise ValueError(f"Unknown source in {row['id']}")
    a = json.loads((DATA / f"scenario-assumptions-{DATE}.json").read_text(encoding="utf-8"))
    v = inputs
    result = {
        "revenue_growth_pct": {
            str(y): (v[f"revenue_{y}"] / v[f"revenue_{y-1}"] - 1) * 100
            for y in (2023, 2024, 2025)
        },
        "revenue_cagr_2022_2025_pct": (v["revenue_2025"] / v["revenue_2022"]) ** (1 / 3) * 100 - 100,
        "reported_margin_pct": {
            period: v[f"profit_{period}"] / v[f"revenue_{period}"] * 100
            for period in ("2024", "2025", "2026h1")
        },
        "profit_growth_2025_pct": (v["profit_2025"] / v["profit_2024"] - 1) * 100,
        "overseas_2024_share_pct": v["overseas_2024"] / v["revenue_2024"] * 100,
        "domestic_2024_residual": v["revenue_2024"] - v["overseas_2024"],
        "overseas_2025_conditional_share_pct": v["overseas_2024"] * (1 + v["overseas_2025_growth"]) / v["revenue_2025"] * 100,
        "buyback_price_change_pct": (v["buyback_2025aug"] / v["buyback_2025mar"] - 1) * 100,
        "valuation_numeric_change_pct": (v["valuation_2026feb"] / v["valuation_2025aug"] - 1) * 100,
        "capex_threshold_change_pct": (v["capex_2026_may"] / v["capex_2026_initial"] - 1) * 100,
        "capex_upper_conditional_growth_pct": (v["capex_2026_upper"] / v["capex_2025_reported"] - 1) * 100,
        "disputed_ecommerce_revenue": v["douyin_revenue_2025_disputed"] * v["douyin_ecommerce_share_disputed"],
        "disputed_revenue_gmv_ratio_pct": v["douyin_revenue_2025_disputed"] * v["douyin_ecommerce_share_disputed"] / v["douyin_gmv_2025_disputed"] * 100,
    }
    prev_revenue = v["revenue_2026h1"] / (1 + v["revenue_2026h1_yoy"])
    h1 = []
    for d in a["h1_profit_decline_bounds"]:
        prev_profit = v["profit_2026h1"] / (1 - d)
        prev_margin = prev_profit / prev_revenue * 100
        h1.append({"assumed_decline_ratio": d, "previous_revenue": prev_revenue,
                   "previous_profit": prev_profit, "previous_margin_pct": prev_margin,
                   "margin_compression_pp": prev_margin - result["reported_margin_pct"]["2026h1"]})
    result["conditional_h1_endpoints_open_upper_bound"] = h1
    result["valuation_profit_sensitivity"] = [
        {"equity_value": e, "profit": profit, "ratio": e / profit}
        for e in a["equity_values"] for profit in a["annual_profit_scenarios"]
    ]
    result["required_cash"] = [
        {"equity_value": e, "yield": rate, "cash": e * rate}
        for e in (5500, 6300) for rate in a["required_cash_yields"]
    ]
    result["cash_conversion_sensitivity"] = [
        {"assumed_conversion": c, "cash": v["profit_2025"] * c,
         "cash_yield_pct_at_5500": v["profit_2025"] * c / 5500 * 100}
        for c in a["cash_conversion"]
    ]
    result["loan_interest_sensitivity"] = [
        {"assumed_rate": rate, "annual_interest_if_fully_drawn": v["loan_2026"] * rate}
        for rate in a["fully_drawn_loan_costs"]
    ]
    result["cash_balance_after_selected_uses_not_standard_fcf"] = [
        {"assumed_cfo": cfo, "assumed_capex": capex,
         "balance": cfo - capex - a["lease_principal_not_in_capex"] - a["buyback"]}
        for cfo in a["cfo_scenarios"] for capex in a["capex_scenarios"]
    ]
    (BASE / f"computed-{DATE}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# 复算与争议核对", "", f"> 核对日期：{DATE}。金额单位亿美元，明确人民币项除外。输入为人工摘录的媒体值/当事人引用；✅只证明算术，非审计真实性。脚本从自身目录读取，保留data不变。", "",
             "运行：`python3 verify.py`；任意当前工作目录均可。完整计算见[JSON](computed-2026-10-05.json)，输入/限定词见[data说明](data/README.md)，来源见[台账](../资料来源-2026-10-05.md)。", "", "## 计算结果", "",
             "| 项目 | 复算 | 判定与限制 |", "|---|---:|---|"]
    checks = [
        ("2023收入增幅（2022采用850）", result["revenue_growth_pct"]["2023"], "%", "✅算术；800与850来源不同"),
        ("2024收入增幅", result["revenue_growth_pct"]["2024"], "%", "🟡基本符合报道29%，非审计"),
        ("2025收入增幅", result["revenue_growth_pct"]["2025"], "%", "🟡基本符合报道29%，非审计"),
        ("2022–2025收入CAGR", result["revenue_cagr_2022_2025_pct"], "%", "✅同一工作序列算术"),
        ("2025报道净利增幅", result["profit_growth_2025_pct"], "%", "🟡基本符合27%；不解IFRS冲突"),
        ("2024报道利润率", result["reported_margin_pct"]["2024"], "%", "✅算术，口径待调节"),
        ("2025报道利润率", result["reported_margin_pct"]["2025"], "%", "✅算术，口径待调节"),
        ("2026H1报道利润率", result["reported_margin_pct"]["2026h1"], "%", "✅算术，非全年"),
        ("2024海外比例", result["overseas_2024_share_pct"], "%", "✅地域，不是业务分部"),
        ("2024国内残差", result["domestic_2024_residual"], "亿美元", "✅残差，不是抖音收入"),
        ("2025海外同比严格取50%后的比例", result["overseas_2025_conditional_share_pct"], "%", "⚠️跨源近似，与超过30%口径待解"),
        ("员工回购单价变化", result["buyback_price_change_pct"], "%", "✅算术，非外部可交易收益"),
        ("5500/3300估值数字变化", result["valuation_numeric_change_pct"], "%", "✅算术；下界/条件不同，不是实际收益"),
        ("1600→2000 AI预算阈值变化", result["capex_threshold_change_pct"], "%", "✅算术；超过2000则超过25%，非实支"),
        ("700/250 capex条件增长", result["capex_upper_conditional_growth_pct"], "%", "✅若执行的上限比值，非实绩"),
        ("争议电商收入", result["disputed_ecommerce_revenue"], "亿元人民币", "⚠️算术正确，未核验分部数据，排除模型"),
        ("争议电商收入/GMV", result["disputed_revenue_gmv_ratio_pct"], "%", "⚠️不可叫纯佣金率或重复加广告"),
    ]
    for label, value, unit, verdict in checks:
        lines.append(f"| {label} | {value:.2f}{unit} | {verdict} |")
    lines += ["", "## 同比利润率的条件反推", "",
              f"收入+30%条件下上年同期收入约{prev_revenue:.2f}；利润降幅近似0%–10%（上端开放），上年利润率端点{h1[0]['previous_margin_pct']:.2f}%–{h1[1]['previous_margin_pct']:.2f}%，同比压缩{h1[0]['margin_compression_pp']:.2f}–{h1[1]['margin_compression_pp']:.2f}个百分点。实际报道近似，不能写一个精确同比结果。",
              "", "❌将2025全年21.00%与2026H1 16.67%差4.33个百分点写成同比降幅，不符合期间可比要求。", "",
              "## 模型算术核对", "",
              "- 估值/利润、所需现金、转换率、利息和资金余额矩阵见完整JSON；所有情景参数明确保存在scenario-assumptions文件。",
              "- 5500/420=13.10倍；非同权利、非同日、非调节后PE。",
              "- 假设296全提款、成本4%/5%/6%：年利息11.84/14.80/17.76亿美元；非实际利率/费用。",
              "- 资金余额=CFO−现金capex−未包含其中的租赁本金−回购；非标准FCF，尚未扣偿债、收购等。", "",
              "## 无法复算和待调节", "",
              "| 问题 | 判定 | 原因 |", "|---|---|---|",
              "| 2025 IFRS大跌与420/480/500亿美元利润 | ⚠️无法勾稽 | 无三张表、股权/优先股调节和归属说明 |",
              "| 集团/分部CFO、FCF、ROIC、ROE | ⚠️无法复算 | 资产、资本与现金流输入缺失 |",
              "| 总债务、净现金、负债率、利息覆盖 | ⚠️无法复算 | 新融资额度不等于余额，缺现金/旧债/提款 |",
              "| 生服712与8500亿元 | ⚠️定义待解 | 支付/核销/地域/期间不明，不直接判同指标造假 |",
              "| 飞书2025增长超过60% | ⚠️无法同口径复算 | ARR与年度收入混合，缺2024收入 |",
              "| Token×统一价推AI收入/成本 | ❌方法不符 | 内外部、免费、模态、缓存和价格不同 |",
              "| 美国商业权益=19.9%全部美国利润 | ❌方法不符 | JV与商业实体职责不同，经济合同未披露 |",
              "| 实际私募股权买入收益、相对Meta实时折价 | ⚠️无法复算 | 无同日成交/权益条款和同口径数据 |", ""]
    (BASE / f"核对结论-{DATE}.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"input_rows": len(rows), "source_count": len(sources),
                      "cagr_pct": result["revenue_cagr_2022_2025_pct"],
                      "margins_pct": result["reported_margin_pct"],
                      "output": str(BASE / f"核对结论-{DATE}.md")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
