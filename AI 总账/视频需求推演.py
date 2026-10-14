#!/usr/bin/env python3
"""视频生成推理电力需求推演 —— v2 (2026-09-04) 用户分层版

与 coding 需求模型 v3.1 同构: 三档用户分层 + 三情景 + 2026-2029 年度推演 + 双口径锚点校准。

单位: "视频秒" (video-second) = 1 秒生成好的视频内容
强度: H100 级等效 GPU-秒 / 视频秒, 2026 基准: 重度 150 / 中度 80 / 轻度 60
  标定: Cantor Fitzgerald: 10s Sora 2 ≈ 40 GPU-min = 240 GPU-s/s (旗舰);
        Veo Fast 定价为 Standard 1/4-1/3 (蒸馏) -> 主流 80;
        Open-Sora 2.0 高压缩 VAE 后 5s/768p < 3 min 单卡 ≈ 36 GPU-s/s (开源/轻量)
功率系数: 每 GPU 全含功率 (服务器分摊 + PUE) = 1.4 kW
  P(GW) = DAU(百万) x 视频秒/人/天 x 强度(GPU-s/s) / 效率 / 86400 x 1.4 kW x 1e-6... 
        即 P = dau_m x sec x intensity / eff x 1.62e-5 GW... (1e6 x 1.4 / 86400 / 1e6 = 1.62e-5? 见代码)

效率路径 (模型蒸馏/少步采样/VAE 压缩/专用芯片带来的强度下降):
  依据: Veo 同代内 Lite($0.05/s) vs Standard($0.40/s) 已有 8x 价差; Open-Sora 2.0 单篇论文 10x;
        LLM 推理 2023-2026 实际降幅每年数倍 -> 保守 1.8x/年, 基准 2.5x/年, 激进 3x/年

2026 锚点 (三情景共用): 双口径校准 0.1-0.3 GW, 中枢 ~0.2 GW
  路径 A (收入): 全球 AI 视频收入 $2-3.5B/yr ÷ 实现价 $0.05-0.15/s = 0.04-0.19B 视频秒/天
  路径 B (生成量): Google Flow 275M 条/5mo + 可灵 ARR $5亿反推 + Sora 遗产 + 其他 = 0.05-0.2B/天

运行: python3 视频需求推演.py   (无外部依赖)
"""

KW_PER_GPU = 1.4
SEC_PER_DAY = 86400
YEARS = [2026, 2027, 2028, 2029]
PEAK_LO, PEAK_HI = 1.3, 1.8

# 三档画像 (2026): dau=百万 DAU当量, sec=视频秒/人/天, inten=GPU-s/视频秒
TIER0 = {
    "重度": dict(dau=0.15, sec=400, inten=150),   # 工作室/专业创作者/MCN/广告: 50条x8s, $100-200/天
    "中度": dict(dau=3.0,  sec=12,  inten=80),    # 半职业创作者/电商营销: 每天 1-2 条 Fast 档
    "轻度": dict(dau=30.0, sec=0.5, inten=60),    # 消费级玩票: 两周一条 Lite/Fast
}

# 三情景: 各档 dau/sec 路径 + 效率路径 + 激进情景的"实时内容"第四档
SCEN = {
    "保守": dict(
        eff=[1, 1.8, 3.2, 5.8],
        重度=dict(dau=[0.15, 0.20, 0.25, 0.30], sec=[400, 450, 480, 500]),
        中度=dict(dau=[3, 4, 5, 6],             sec=[12, 16, 20, 25]),
        轻度=dict(dau=[30, 38, 44, 50],          sec=[0.5, 0.6, 0.7, 0.8]),
        实时=None,
    ),
    "基准": dict(
        eff=[1, 2.5, 6.25, 15.6],
        重度=dict(dau=[0.15, 0.25, 0.40, 0.60], sec=[400, 550, 650, 800]),
        中度=dict(dau=[3, 5, 8, 12],            sec=[12, 20, 35, 50]),
        轻度=dict(dau=[30, 45, 70, 100],         sec=[0.5, 0.8, 1.1, 1.5]),
        实时=None,
    ),
    "激进": dict(
        eff=[1, 3.0, 9.0, 27.0],
        重度=dict(dau=[0.15, 0.35, 0.70, 1.20], sec=[400, 700, 1000, 1500]),
        中度=dict(dau=[3, 7, 14, 25],           sec=[12, 30, 70, 120]),
        轻度=dict(dau=[30, 60, 130, 250],        sec=[0.5, 1.2, 2.2, 4.0]),
        # 相变档: AI 内容从生产工具变为消费内容本身 (个性化信息流早期形态)
        实时=dict(dau=[0, 0, 2, 10],            sec=[0, 0, 300, 600], inten=30),
    ),
}


def gw(dau_m, sec, inten, eff):
    """平均功率 GW"""
    return dau_m * 1e6 * sec * inten / eff * KW_PER_GPU / SEC_PER_DAY / 1e6


def kwh(inten):
    return inten * KW_PER_GPU / 3600


print("=" * 78)
print("0. 物理标尺 (2026 强度)")
print("=" * 78)
for name, t in TIER0.items():
    print(f"{name}档 ({t['inten']:>3} GPU-s/视频秒): 1 视频秒 ≈ {kwh(t['inten'])*1000:5.1f} Wh, "
          f"10s 视频 ≈ {kwh(t['inten'])*10:4.2f} kWh; 该档用户每天 {t['sec']:>6.1f} 视频秒")

print()
print("=" * 78)
print("1. 2026 锚点校验 (三情景共用)")
print("=" * 78)
tot_p, tot_v = 0, 0
for name, t in TIER0.items():
    p = gw(t["dau"], t["sec"], t["inten"], 1)
    v = t["dau"] * t["sec"] / 1000  # B 视频秒/天
    tot_p += p; tot_v += v
    print(f"{name}: {t['dau']:>5.2f}M DAU x {t['sec']:>6.1f} s/天 = {v*1000:6.1f}M 视频秒/天 -> {p*1000:5.1f} MW")
print(f"合计: {tot_v:.3f}B 视频秒/天 -> {tot_p:.2f} GW 平均 (外部包络 0.1-0.3 GW 内)")
for rev, price in [(2.0, 0.15), (3.5, 0.05)]:
    print(f"  路径A: 收入 ${rev}B/yr ÷ ${price}/s = {rev/price/365:.2f}B 视频秒/天")

print()
print("=" * 78)
print("2. 三情景年度推演 (平均功率 GW)")
print("=" * 78)
for sc, s in SCEN.items():
    print(f"\n--- {sc} ---")
    print("年份 | 重度MW | 中度MW | 轻度MW | 实时MW | 合计GW | 装机GW(1.3-1.8) | 视频秒B/天")
    for i, y in enumerate(YEARS):
        parts = {}
        for tier in ("重度", "中度", "轻度"):
            parts[tier] = gw(s[tier]["dau"][i], s[tier]["sec"][i], TIER0[tier]["inten"], s["eff"][i])
        rt = 0
        if s["实时"]:
            rt = gw(s["实时"]["dau"][i], s["实时"]["sec"][i], s["实时"]["inten"], s["eff"][i])
        t_gw = sum(parts.values()) + rt
        vol = sum(s[t]["dau"][i] * s[t]["sec"][i] for t in ("重度", "中度", "轻度")) / 1000
        if s["实时"]:
            vol += s["实时"]["dau"][i] * s["实时"]["sec"][i] / 1000
        print(f"{y} | {parts['重度']*1000:6.0f} | {parts['中度']*1000:6.0f} | {parts['轻度']*1000:6.0f} "
              f"| {rt*1000:6.0f} | {t_gw:6.3f} | {t_gw*PEAK_LO:5.2f}-{t_gw*PEAK_HI:5.2f} | {vol:6.2f}")

print()
print("=" * 78)
print("3. 终局检验: 1.8 万亿视频秒/天 (10亿人 x 30分钟) 需要多少效率")
print("=" * 78)
for p in (20, 50, 100):
    i_need = p * 1e6 * SEC_PER_DAY / (1800e9 * KW_PER_GPU)
    print(f"压到 {p:>3} GW 平均: 强度 {i_need:4.1f} GPU-s/视频秒 = 2026 重度的 1/{150/i_need:,.0f}, 轻度的 1/{60/i_need:.0f}")

print()
print("=" * 78)
print("4. 与 coding v3.1 对照")
print("=" * 78)
print("coding: 2026 = 0.42 GW | 2029 保守/基准/激进 = 0.81 / 1.88 / 3.95 GW")
veo = 0.40 / 250 * 3600 / KW_PER_GPU * 24
cod = 151e3 * 5 / 1e6 * 86400 / 162
print(f"每 kW 每天收入: Veo 旗舰 ${veo:.0f} vs coding(GB300, $5/M oe) ${cod:.0f} -> {cod/veo:.0f}x 货币化密度差")
