# 1GW AI Factory 标准物理模型 V1.0

> 整理/核对日期：2026-08-22（精简重写）；2026-08-25 补 GPU→机柜换算（§1、§9、§10）。
> 用途：把"新增 1GW IT"映射为可复用的物理 BOM 基准，供产业链收入池测算（HBM/SSD/网络/供电/液冷）调用。
> 下游：`存储与NAND/NAND需求测算.md`、`行业背景/机柜对比.md`。待办：在此 V1.0 上补**美元价值量**（GPU/HBM/光互连/UPS/液冷各值多少钱 → 映射到 NVIDIA/Micron/SK hynix/Vertiv/Schneider/Eaton/GE Vernova 收入）。

**一句话结论**：GB300 时代 1GW ≈ 46 万 GPU ≈ **6,400 个 NVL72 计算柜（含 Support 柜共 ~1.28 万物理机柜）** + 132.5PB HBM + ~2EB 本地 SSD + ~1.6GVA UPS + 0.78GW 液冷；Rubin 完整 Factory 同样 1GW 只剩 ~23 万 GPU ≈ **3,200 计算柜 + ~800 存储柜**，HBM bit 减半但代际升级，配套系统（网络/存储/CMX）占 IT 功率从 ~9% 升至 ~27%。

## 0. 口径锁定

- **1GW = 1GW IT Load**（进 GPU/CPU/NVSwitch/NIC/存储/网络设备的功率），不是电网入口
- 电网入口 = IT × PUE，现代高密度液冷取 **PUE 1.10–1.15** → 1GW IT ≈ 1.10–1.15GW Facility Power（可按气候带调整）

## 1. GB300：46 万 GPU/GW（A 级置信度）

两家竞争对手的完整机房 Reference Design 独立交叉验证：

| 方案 | IT 规模 | 内容 | 换算 GPU/GW |
|---|---|---|---:|
| Vertiv #028 | 4.992MW | 32 × NVL72（142kW）+ 32 × Support Rack | **461,538** |
| Schneider RD110 | 7.536MW | 3 × 1,152-GPU cluster | **458,599** |

差异仅 0.64% → 固定 **GB300 ≈ 46 万 B300/GW IT**。([Schneider][1])

**机柜换算**：460,000 ÷ 72 = **~6,400 个 NVL72 Compute Rack/GW**（密度 ≈ **6.4 计算柜/MW IT**）。按 Vertiv 1:1 Support Rack 布局，再加 ~6,400 个 Support 柜 → **物理机柜合计 ~1.28 万/GW**（Support 柜可合并，是上限口径）。对照 `合同/AI算力合同.md` §2：Horizon 按 189kW/柜分摊 IT 只有 5.3 柜/MW——差别在配套 IT 分摊口径，不在 GPU 数。

**Support IT 比例同样被双源验证**：Vertiv 91.0% / Schneider 90.45% 的 IT 功率进 Compute Rack → **GB300 完整 Factory：~90–91% 进 NVL72，~9–10% 为柜外网络/存储/Support IT**（非假设，是两套 reference 的自然结果）。

## 2. GB300 1GW 核心 BOM（由 NVIDIA 官方架构直接乘出）

每 NVL72 = 72 GPU + 36 Grace + 18 Compute Tray + 9 NVSwitch Tray；每 Compute Tray = 4 GPU + 2 Grace + 4 ConnectX-8 + 1 BlueField-3。([NVIDIA Docs][2])

| 硬件 | 1GW GB300 |
|---|---:|
| NVL72 Compute Rack | ~6,390（460,000÷72） |
| B300 GPU | ~460,000 |
| Grace CPU | ~230,000 |
| Compute Tray | ~115,000 |
| NVSwitch Tray | ~57,500 |
| ConnectX-8 | ~460,000 |
| BlueField-3 | ~115,000 |

Support Rack reference 口径 ~6,400 个（1:1 布局），但**大型园区会合并设备，实际未必需要这么多独立 support 柜**。

## 3. HBM：~132.5PB HBM3E/GW

460,000 × 288GB = **132.5PB/GW**（每 GPU 288GB HBM3E，[NVIDIA Docs][2]）。速算：新增 10GW ≈ 1.325EB HBM。

## 4. 网络：~281 万 transceiver BOM-equivalent（基准/下限）

NVIDIA 8-rack reference：576 GPU → 3,524 transceiver positions（East-West 2,304 + Converged 1,220）= **6.12 个/GPU**([NVIDIA Docs][3])。460,000 × 6.12 ≈ **281 万**。

两个修正：

1. **281 万 ≠ 281 万个 800G 光模块**——含 twin-port OSFP、2×400G breakout、铜、不同速率/端点，是"BOM position equivalent"，不能直接 × 800G ASP
2. 1GW 有 115,000 个 node，远超 1,024 node 的 super-spine 门槛 → 真实园区还有 Leaf→Spine→Super-Spine 高层互连，**281 万是下限而非精确值**

## 5. 供电：UPS/PDU ~1.6GVA/GW（reference 值）

Vertiv 4.992MW IT 配 4×2MVA UPS（4-to-make-3）与 8×1MVA PDU → 均为 **~1.60GVA installed/GW IT**。注意：installed nameplate ≠ 实际负载，差额来自冗余/维护/设计裕量。**研究 Vertiv/Schneider/Eaton 的正确指标是 installed GVA / IT GW，GB300 Tier III 型 ≈ 1.6×**。

## 6. 液冷：分清"物理需求"和"采购台数"

- **物理需求**：1GW IT → ~1GW 热。GB300 参考 78% 液冷 → **~0.78GW 直接液冷 + 0.22GW 风冷**
- **采购台数不能机械放大**：Vertiv 5MW 设计外推得 ~800 台 XDU2300/GW，但 Trane 1GW Reference Design（RD501）明确 1GW 不能复制小模块，而是拆成 ~102.4MW thermal partitions（每 block = 10×9.6MW + 1×6.4MW CDU pod，共享冗余）([Trane][4])
- **200kW+/Rubin 时代**：Trane 按 512 rack×200kW/block、**94–100% 液冷**设计 → 物理液冷 **~0.94–1.0GW/GW IT**
- 结论：CDU 台数由单台容量 + 冗余架构决定，**不作为行业需求参数；物理热负载才是**

## 7. 变压器与电网侧

- 工作视在功率：1.15GW ÷ PF 0.95 ≈ **1.21GVA**；加 N+1/维护/裕量 → 主电力系统 installed transformer capacity **~1.3–1.6GVA（工程模型值，未经 reference 验证）**
- 必须分两级统计，不能混成"多少台"：**Grid 主变 GVA**（如 6×250MVA）与 **data-hall 配电变压器 GVA**（数百台 2–5MVA 级）。待 Siemens/Schneider 完整 MV schematic 深挖

## 8. 燃机：情景变量，不是必选 BOM

- 全 Grid 供电 → **0 台燃机**完全成立
- 100% behind-the-meter 气电：1GW IT 需 ~1.1–1.15GW 净发电 ≈ **一座 1.3GW 级联合循环电厂**。GE 7HA.03（430MW 单循环）×3 = 1.29GW，N+1 则 4 台；GE 2×1 联合循环 1,282MW、Siemens SGT6-9000HL 2×1 ≈ 1,310MW —— 同一尺度。([GE Vernova][5], [Siemens][6])
- 经验公式：**1GW IT AI Factory ≈ 一座 1.3GW 联合循环电厂**（前提：100% onsite gas）

## 9. Rubin：完整 Factory 只剩 ~23 万 GPU/GW

依据 Supermicro Vera Rubin NVL72 DCBBS 蓝图：**1,152 GPU Scalable Unit = 5MW power envelope**（含 compute/network/storage/context memory/power/cooling），可 5MW→1GW 复制。([Supermicro][7])

- 1GW ÷ 5MW = 200 SU → **230,400 GPU/GW**；每 SU 16 个 NVL72 → **~3,200 Compute Rack/GW**（密度 ≈ **3.2 计算柜/MW IT**）
- 计算柜功率 3,200 × 227kW = 726MW → **Compute Rack 占 IT 仅 ~73%**（GB300 是 90–91%），其余 ~27% 给网络/存储/CMX/support——证实 Rubin POD 不再只是"很多 NVL72 柜"
- **物理机柜合计**：3,200 计算柜 + ~800 存储柜（每 SU 4 个 NVMe storage rack × 200 SU，见 §10 口径说明）+ 网络/CMX 柜（数量待查）→ **≥ ~4,000 柜/GW**
- **HBM 反降**：230,400 × 288GB HBM4 = **66.4PB/GW**，约为 GB300 一半。原因不是单 GPU 变少（仍 288GB），而是 GPU 数减半
- ⚠️ **不等于"HBM 需求减半"**：HBM4 带宽 22TB/s（2.75×），die 数/堆叠/ASP/单位 bit 价值全变。研究 Micron/SK 必须区分 **bit demand 与 revenue demand**
- **两种情景**：Training-heavy ~27–30 万 GPU/GW = **3,750–4,170 计算柜**（纯计算柜理论上限 317,000 GPU ≈ 4,400 柜，留 ~10% support；待更多 reference 验证）；完整 Agentic/DSX 型 **~23 万 = 3,200 柜**（Supermicro 蓝图支撑）

## 10. 1GW 总表 V1.0

| 项目 | GB300 AI Factory | Rubin Full-stack Factory |
|---|---:|---:|
| IT Load | 1GW | 1GW |
| Compute Rack（GPU ÷ 72） | ~6,400（≈6.4 柜/MW） | ~3,200（≈3.2 柜/MW） |
| 物理机柜合计（估） | ~12,800（+Support 柜，1:1 上限口径） | ≥ ~4,000（+~800 存储柜 + 网络/CMX 柜待查） |
| GPU | ~460,000 | ~230,000 |
| CPU | ~230,000 Grace | ~115,000 Vera |
| HBM | ~132.5PB HBM3E | ~66.4PB HBM4 |
| CPU 内存（LPDDR5X） | ~110PB | ~173PB |
| 柜内本地 SSD（不含 CMX） | ~2EB（满配上限 ~7.3EB） | 容量未公开；另有 ~800 个独立 storage rack（容量待查） |
| Compute Rack 占 IT | ~90–91% | ~73% |
| 网络代际 | 800G/400G breakout | 1.6T/CPO |
| Transceiver 基准 | ~2.8M equivalent（下限） | 不能直接沿用 |
| 直接液冷 | ~0.78GW | 接近全液冷 |
| UPS installed | ~1.6GVA（reference） | 架构变化中 |
| 电网负荷 | ~1.1–1.15GW | 类似（取决于 PUE） |
| 变压器 | ~1.2GVA 工作 + 冗余 | 类似，配电架构变化 |
| Onsite gas | 0 或 ~1.3GW 电厂 | 0 或 ~1.3GW 电厂 |

口径说明：

- **CPU 内存**：Grace 480GB/CPU（23万×0.48TB≈110PB）、Vera 1.5TB/CPU（11.5万×1.5TB≈173PB）。方向与 HBM 相反：GPU 数减半但 CPU 内存/GPU 0.5TB→1.5TB，总量反增 ~56%
- **柜内 SSD**：GB300 按 Lenovo 指南 4×3.84TB E1.S + 1×1.92TB M.2/tray，~311TB/柜（~3.84TB/GPU）×6,390 ≈ 2EB；满配 8×7.68TB/tray 上限 ~7.3EB。([Lenovo][10]) Rubin compute tray 确认 E1.S Gen6 但容量未公开；柜外存储按 DCBBS 每 SU 4 个 NVMe storage rack × 200 SU = ~800 个 storage rack，单柜容量待查；BlueField-4 板载 512GB SSD 按 CMX 口径未计入

## 11. 方法论要点（为什么不混）

- **GPU 平台决定物理 IT BOM**；Vertiv/Schneider 决定怎么工程化；Trane 说明 1GW 规模后冷却不能机械复制 5MW 模块；Eaton 说明供电架构还会 AC→高压 DC 演变；燃机是供电情景不是固定 BOM
- GB300 各项（46万 GPU、132.5PB HBM、2EB SSD、1.6GVA UPS、0.78GW 液冷、6,400 柜）经多 Reference Design 交叉验证，**A 级置信度**
- Rubin 除 Supermicro 蓝图项外，GPU/GW、800VDC、CPO、CMX 渗透、storage rack 容量均**待验证**

[1]: https://www.se.com/ph/en/download/document/RD110DSR0/ "Schneider Electric Reference Design 110: 7,536 kW GB300 AI Clusters"
[2]: https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html "NVIDIA NVL72 AI Factory — System Hardware & Components"
[3]: https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/network-logical-architecture.html "NVIDIA NVL72 AI Factory — Network Logical Architecture"
[4]: https://www.trane.com/content/dam/Trane/Commercial/global/markets/data-centers/Trane-ReferenceDesign-1GW.pdf "Trane Reference Design #501 (1GW)"
[5]: https://www.gevernova.com/gas-power/products/gas-turbines/7ha "GE Vernova 7HA Gas Turbine"
[6]: https://www.siemens-energy.com/global/en/home/products-services/product/sgt6-9000hl-heavy-duty-gas-turbine.html "Siemens Energy SGT6-9000HL"
[7]: https://ir.supermicro.com/news/news-details/2026/Supermicro-Introduces-DCBBS-Blueprints-for-NVIDIA-Vera-Rubin-NVL72-and-NVIDIA-HGX-Rubin-NVL8-Built-to-Scale-from-5MW-to-1GW-as-an-End-to-End-Total-Solution/default.aspx "Supermicro DCBBS Blueprints for Vera Rubin NVL72（5MW→1GW）"
[8]: https://www.supermicro.com/zh_cn/accelerators/nvidia/vera-rubin "Supermicro Vera Rubin 方案"
[9]: https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/ "NVIDIA Vera Rubin NVL72"
[10]: https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai "Lenovo GB300 NVL72 Product Guide"
