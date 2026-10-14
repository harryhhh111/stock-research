#!/usr/bin/env python3
"""阿里巴巴(BABA)派生指标复算。年度数据来自 SEC companyfacts（USD），
季度/分部数据来自公司披露与 Yahoo Finance 下载（CNY）。
本脚本只做算术复算，不抓取数据。
"""
# 年度（USD B，FY 截至 3/31，来源：SEC companyfacts, filed 2026-05-20）
annual = {
    "FY2024": dict(rev=130.350, ni=11.081, op=15.699, cfo=25.289, rd=7.237, buyback=12.291, div=2.485, equity=136.635, assets=244.426),
    "FY2025": dict(rev=137.300, ni=17.929, op=19.417, cfo=22.532, rd=7.876, buyback=11.942, div=4.007, equity=139.162, assets=248.629),
    "FY2026": dict(rev=148.401, ni=15.018, op=7.270, cfo=11.049, rd=9.645, buyback=1.107, div=4.890, equity=153.796, assets=276.830),
}

print("== 年度派生指标（USD B）==")
prev = None
for fy, d in annual.items():
    yoy = (d["rev"] / prev["rev"] - 1) * 100 if prev else float("nan")
    print(f"{fy}: 营收 {d['rev']:.1f} (YoY {yoy:+.1f}%), 营业利润率 {d['op']/d['rev']*100:.1f}%, "
          f"净利率 {d['ni']/d['rev']*100:.1f}%, FCF* {d['cfo']-0:.1f}* (缺CapEx), "
          f"ROE(期末) {d['ni']/d['equity']*100:.1f}%, 研发/营收 {d['rd']/d['rev']*100:.1f}%, "
          f"回购+分红 {d['buyback']+d['div']:.2f}")
    prev = d

# 季度（CNY B，来源：Yahoo 下载季度报表；OP 取 as-reported 列）
q = {
    "Jun-25": dict(rev=247.652, op=34.988),
    "Sep-25": dict(rev=247.795, op=5.365),
    "Dec-25": dict(rev=284.843, op=10.645),
    "Mar-26": dict(rev=243.380, op=-0.848),
    "Jun-26": dict(rev=268.953, op=15.161),
}
print("\n== 季度（CNY B）==")
for k, d in q.items():
    print(f"{k}: 营收 {d['rev']:.1f}, 经营利润 {d['op']:.3f}, 经营利润率 {d['op']/d['rev']*100:.1f}%")

fy26_op = sum(v["op"] for k, v in q.items() if k != "Jun-26")
fy26_rev = sum(v["rev"] for k, v in q.items() if k != "Jun-26")
print(f"\nFY2026 季度加总: 营收 {fy26_rev:.1f} CNY, 经营利润 {fy26_op:.2f} CNY")
print(f"SEC FY2026: 营收 $148.401B, 经营利润 $7.270B → 隐含汇率 {(fy26_rev/148.401):.2f} CNY/USD")
print(f"OP 勾稽: {fy26_op:.1f} CNY ≈ ${fy26_op/(fy26_rev/148.401):.1f}B (SEC $7.270B) ✓ 差异<5%")

# 估值快照（2026-09-23, Yahoo）
mcap = 289.1  # $B
ev = 217.1
cash_cny = 385.697  # 现金+短投, Jun-26
debt_cny = 266.530
fx = 7.2
net_cash = (cash_cny - debt_cny) / fx
print(f"\n== 估值快照 2026-09-23 ==")
print(f"市值 ${mcap}B, EV ${ev}B; 净现金(现金+短投-总债务) ≈ ${net_cash:.1f}B")
revenue_usd = 1045 / fx
print(f"TTM营收(¥1,045B≈${revenue_usd:.0f}B); 市值/TTM营收 = {mcap/revenue_usd:.1f}x")
print(f"市值-EV = ${mcap-ev:.1f}B；扣除狭义净现金后的未解释差额 = ${mcap-ev-net_cash:.1f}B → EV字段暂不用于估值结论")
print(f"市值减狭义净现金 = ${mcap-net_cash:.1f}B，约为营收 {(mcap-net_cash)/revenue_usd:.1f}x（非完整EV）")
print(f"Forward PE 12.5 (Yahoo); 假设 forward EPS ≈ {116.31/12.5:.2f} USD")
print(f"FY2026人均营收: $148.401B / 132,165 人 ≈ ${148.401e9/132165/1e6:.2f}M/人")

# AI/云专项投入未与集团总 CapEx 逐项勾稽；参见 verify_ai_cloud.py。
print("\n== AI/云投资计划 ==")
print("公司公布未来三年至少 ¥380B 的 AI/云基础设施投资计划；不能用集团总 CapEx 推断计划完成率或剩余额度。")
