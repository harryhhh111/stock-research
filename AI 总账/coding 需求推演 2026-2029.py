#!/usr/bin/env python3
"""Coding agent 推理电力需求推演 2026-2029 —— v3.2 分层版 (重+中人数锚定 SO 调查, 三变量三角互锁)

2026 锚点: 全球 coding 推理 ≈ 0.2-0.6 GW 平均, 中枢 0.47 GW
  路径 A (收入反推, 全口径): 全球 coding 推理收入 ~$25-40B/yr (Anthropic coding ~$15-21B
    [总 run rate $30B x coding 50-70%] + OpenAI $5-8B + Copilot/Cursor/Google/中国 $5-10B),
    实现价格 $2-10/M oe token -> 0.11-0.55 GW
  路径 B (token 流量): 全球 API ~100-200T 总token/天, coding 25-40% -> 0.18-0.59 GW
  v3.2: 重+中人数锚定 Stack Overflow 2025 (47M 开发者 x 47.1% 每天用 AI ≈ 22M 日活),
    中度强度从 Anthropic 企业均值 $13/天向全球混合均值 $10/天稀释 -> 0.47 GW
三档 DAU 校准: 重度 3.0M / 中度 18M / 轻度 100M  (重+中 21M ≈ SO 隐含 22M ✓)
  校验: 3.0x4.8 + 18x1.0 + 100x0.048 = 14.4 + 18.0 + 4.8 = 37.2T oe/天 -> 37.2/80 = 0.47 GW ✓

通用公式: P(GW) = DAU(百万) x oe-token(百万/人/天) / (80 x 机队效率)
oe 折算: cached 0.02 / fresh 0.2 / output 1.0, 构成 80/15/5
三档画像 (2026): 重度 50M 总token/天 -> 4.8M oe; 中度 10.4M -> 1.0M oe; 轻度 0.5M -> 0.048M
中度人数路径受开发者池约束 (2029 全球日活 AI 开发者 ~45-50M, 重+中不能超过池子)

运行: python3 "coding 需求推演 2026-2029.py"   (无外部依赖)
"""

YEARS = [2026, 2027, 2028, 2029]
PEAK_LO, PEAK_HI = 1.3, 1.8  # 装机口径峰谷系数

SCEN = {
    "保守": dict(
        eff=[1.0, 1.3, 1.8, 2.4],
        heavy=dict(dau=[3.0, 3.7, 5.0, 6.3], tok=[4.8, 7.0, 10.0, 13.0]),
        med=dict(dau=[18, 22, 27, 33], tok=[1.00, 1.25, 1.50, 1.79]),
        light=dict(dau=[100, 135, 160, 200], tok=[0.048, 0.055, 0.062, 0.070]),
    ),
    "基准": dict(
        eff=[1.0, 1.6, 2.3, 3.25],
        heavy=dict(dau=[3.0, 4.0, 6.0, 8.0], tok=[4.8, 9.6, 19.0, 34.0]),
        med=dict(dau=[18, 24, 34, 45], tok=[1.00, 1.50, 2.25, 3.38]),
        light=dict(dau=[100, 145, 225, 333], tok=[0.048, 0.060, 0.075, 0.096]),
    ),
    "激进": dict(
        eff=[1.0, 1.9, 3.0, 4.5],
        heavy=dict(dau=[3.0, 5.0, 8.75, 12.5], tok=[4.8, 14.0, 34.0, 68.0]),
        med=dict(dau=[18, 26, 40, 55], tok=[1.00, 1.79, 3.23, 5.82]),
        light=dict(dau=[100, 175, 365, 666], tok=[0.048, 0.067, 0.096, 0.134]),
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
