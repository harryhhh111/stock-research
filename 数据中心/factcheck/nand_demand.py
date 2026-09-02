#!/usr/bin/env python3
"""NVIDIA 2026/2027 机柜出货 → SSD → NAND 需求测算
输入口径：
- 机柜出货：数据中心/机柜出货量.md Base Case（2026: GB300 4.0万 + VR 1.0万 + GB200尾单0.2万；
  2027: VR 4.8万 + Rubin Ultra 2.9万 + GB300尾单0.3万）
- 单柜本地SSD：GB300 = 17.28TB/tray × 18 tray = 311TB（Lenovo官方参考配置），高配 34TB×18=612TB
- Vera Rubin = 5盘位/tray × 18，容量未公开，沿用 17.28TB/tray 假设
- Rubin Ultra NVL144 = 144 GPU/柜，SSD未公开，按 3.84TB/GPU + boot 假设 ~588TB/柜
- CMX：仅 Rubin 代；情景 = 推理GPU占比 × TB/推理GPU；STX rack 9.2PB 有效容量
"""

TB = 1e-6  # TB → EB（1 EB = 1e6 TB）

def rack_ssd(racks, tb_per_rack):
    return racks * tb_per_rack * TB  # EB

# ---------- 单柜参数 ----------
GB300_BASE_TB = 17.28 * 18        # 311TB/柜（4×3.84T+1×1.92T）/tray
GB300_HIGH_TB = 34.0 * 18         # 612TB/柜（8×4T+1×2T）/tray
VR_TB         = 17.28 * 18        # 假设沿用GB300容量（5盘位，容量未公开）
RU_TB         = 3.84 * 144 + 1.92 * 36  # Rubin Ultra: 3.84T/GPU + 每superchip boot ≈ 622TB

# ---------- 出货量（Base Case，见机柜出货量.md）----------
ship = {
    2026: {"GB300": 40000, "VeraRubin": 10000, "GB200尾单": 2000},
    2027: {"VeraRubin": 48000, "RubinUltra": 29000, "GB300尾单": 3000},
}

# ---------- CMX 情景（仅Rubin代GPU）----------
# (推理GPU占比, TB/推理GPU)
cmx_scen = {"低(50%×2TB)": (0.50, 2), "基准(50%×4TB)": (0.50, 4),
            "高(50%×8TB)": (0.50, 8), "满配(67%×16TB)": (0.67, 16)}

def eb(x): return f"{x:,.2f} EB"

print("=" * 72)
for year, mix in ship.items():
    print(f"\n【{year}】机柜 → 本地 SSD")
    total_local = 0
    rubin_gpus = 0
    for platform, racks in mix.items():
        if "GB300" in platform or "GB200" in platform:
            tb = GB300_BASE_TB
            gpu_per_rack = 72
        elif platform == "VeraRubin":
            tb = VR_TB; gpu_per_rack = 72
            rubin_gpus += racks * gpu_per_rack
        else:  # Rubin Ultra
            tb = RU_TB; gpu_per_rack = 144
            rubin_gpus += racks * gpu_per_rack
        cap = rack_ssd(racks, tb)
        total_local += cap
        ssds = racks * 18 * 5 if gpu_per_rack == 72 else racks * 90  # 5块/tray×18
        if platform == "RubinUltra":
            ssds = racks * 90 * 2  # 假设2倍tray数，粗估
        print(f"  {platform:12s} {racks:>6,}柜 × {tb:>5.0f}TB = {eb(cap):>10s}  | SSD约{ssds/1e4:,.0f}万块")

    print(f"  本地SSD小计: {eb(total_local)}")

    print(f"  Rubin代GPU: {rubin_gpus/1e4:,.0f}万颗 → CMX情景:")
    for name, (share, tb) in cmx_scen.items():
        cmx = rubin_gpus * share * tb * TB
        racks_needed = cmx * 1e3 / 9.2 / 1e3  # EB→PB→/9.2PB
        print(f"    {name:18s}: {eb(cmx):>10s}  (≈{cmx*1e3/9.2:,.0f}个9.2PB CMX rack)")
        print(f"    {'':18s}  合计 {eb(total_local + cmx)}")

# ---------- 对照外部基准 ----------
print("\n" + "=" * 72)
print("外部基准对照：")
print("  Goldman: 全球企业级SSD需求 2026=474EB, 2027=619EB")
print("  Citi: Vera Rubin 相关 NAND ≈ 全球NAND需求 2027年2.8% / 2028年9.3%")
print("  TrendForce: 2026 NAND供需缺口 -4~-5%")

# 本地SSD(base config) + CMX基准 的全球占比（用Goldman eSSD口径）
y26_local = 40000*GB300_BASE_TB*TB + 10000*VR_TB*TB + 2000*GB300_BASE_TB*TB
y26_cmx_base = 10000*72*0.5*4*TB
y27_local = 48000*VR_TB*TB + 29000*RU_TB*TB + 3000*GB300_BASE_TB*TB
y27_rubin_gpus = 48000*72 + 29000*144
y27_cmx_base = y27_rubin_gpus*0.5*4*TB
print(f"\n  本模型2026合计(本地+CMX基准): {y26_local+y26_cmx_base:.1f}EB → 占2026 eSSD {100*(y26_local+y26_cmx_base)/474:.1f}%")
print(f"  本模型2027合计(本地+CMX基准): {y27_local+y27_cmx_base:.1f}EB → 占2027 eSSD {100*(y27_local+y27_cmx_base)/619:.1f}%")
print(f"  若2027全球NAND总需求≈1,300EB（服务器占~40%+），NVIDIA机柜NAND占比≈{100*(y27_local+y27_cmx_base)/1300:.1f}%")
