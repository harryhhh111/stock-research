#!/usr/bin/env python3
"""Coding agent 推理电力需求推演 2026-2029 —— v3 分层版 (锚点经外部口径重校准)

2026 锚点: 全球 coding 推理 ≈ 0.1-0.6 GW 平均, 中枢 0.30 GW
  路径 A (收入反推, 全口径): 全球 coding 推理收入 ~$25-40B/yr (Anthropic coding ~$15-21B
    [总 run rate $30B x coding 50-70%] + OpenAI $5-8B + Copilot/Cursor/Google/中国 $5-10B),
    实现价格 $2-10/M oe token -> 0.11-0.55 GW
  路径 B (token 流量): 全球 API ~100-200T 总token/天, coding 25-40% -> 0.18-0.59 GW
  两路径收敛 -> 中枢 0.30 GW
三档 DAU 校准: 重度 2.5M / 中度 12M / 轻度 130M
  校验: 2.5x4.8 + 12x0.48 + 130x0.048 = 12 + 5.76 + 6.24 = 24T oe/天 -> 24/80 = 0.30 GW ✓

通用公式: P(GW) = DAU(百万) x oe-token(百万/人/天) / (80 x 机队效率)
oe 折算: cached 0.02 / fresh 0.2 / output 1.0, 构成 80/15/5
三档画像 (2026): 重度 50M 总token/天 -> 4.8M oe; 中度 5M -> 0.48M; 轻度 0.5M -> 0.048M

运行: python3 "coding 需求推演 2026-2029.py"   (无外部依赖)
"""

YEARS = [2026, 2027, 2028, 2029]
PEAK_LO, PEAK_HI = 1.3, 1.8  # 装机口径峰谷系数

SCEN = {
    "保守": dict(
        eff=[1.0, 1.3, 1.8, 2.4],
        heavy=dict(dau=[2.5, 3.7, 5.0, 6.3], tok=[4.8, 7.0, 10.0, 13.0]),
        med=dict(dau=[12, 16, 20, 24], tok=[0.48, 0.60, 0.72, 0.86]),
        light=dict(dau=[130, 175, 208, 260], tok=[0.048, 0.055, 0.062, 0.070]),
    ),
    "基准": dict(
        eff=[1.0, 1.6, 2.3, 3.25],
        heavy=dict(dau=[2.5, 4.0, 6.0, 8.0], tok=[4.8, 9.6, 19.0, 34.0]),
        med=dict(dau=[12, 18, 28, 40], tok=[0.48, 0.72, 1.08, 1.62]),
        light=dict(dau=[130, 189, 293, 433], tok=[0.048, 0.060, 0.075, 0.096]),
    ),
    "激进": dict(
        eff=[1.0, 1.9, 3.0, 4.5],
        heavy=dict(dau=[2.5, 5.0, 8.75, 12.5], tok=[4.8, 14.0, 34.0, 68.0]),
        med=dict(dau=[12, 22, 40, 60], tok=[0.48, 0.86, 1.55, 2.80]),
        light=dict(dau=[130, 228, 475, 865], tok=[0.048, 0.067, 0.096, 0.134]),
    ),
}


def gw(dau_m, tok_m, eff):
    return dau_m * tok_m / (80 * eff)


for name, s in SCEN.items():
    print(f"\n{'='*72}\n=== {name} ===")
    print("年份 | 重度GW | 中度GW | 轻度GW | 合计平均GW | 装机GW(1.3-1.8) | 重度占比")
    for i, y in enumerate(YEARS):
        h = gw(s["heavy"]["dau"][i], s["heavy"]["tok"][i], s["eff"][i])
        m = gw(s["med"]["dau"][i], s["med"]["tok"][i], s["eff"][i])
        l = gw(s["light"]["dau"][i], s["light"]["tok"][i], s["eff"][i])
        t = h + m + l
        print(f"{y} | {h:6.3f} | {m:6.3f} | {l:6.3f} | {t:8.3f} "
              f"| {t*PEAK_LO:5.2f}-{t*PEAK_HI:5.2f} | {h/t*100:4.0f}%")

# 基准 2029 机柜换算 + 占第三方全球 AI 功率预测比例
s = SCEN["基准"]
t29 = sum(gw(s[t]["dau"][3], s[t]["tok"][3], s["eff"][3]) for t in ("heavy", "med", "light"))
inst = t29 * 1.5
print(f"\n2029 基准合计: 平均 {t29:.2f} GW, 装机中枢 {inst:.2f} GW")
for kw, label in [(200, "Rubin NVL144 代"), (600, "Rubin Ultra NVL576 代")]:
    print(f"  全由 {label}机柜承担: ~{inst*1e6/(kw*1.2):,.0f} 机柜")
print(f"  占 Goldman 2029 全球 AI 功率 (21.7 GW): {t29/21.7*100:.1f}%")
print(f"  占 McKinsey 2029 全球 AI 功率 (57.2 GW): {t29/57.2*100:.1f}%")
