# 1GW 数据中心的电力链路：从电厂到 GPU

> 整理日期：2026-09-02。量级数据引自 `数据中心/数据中心1GW.md`（V1.0 物理模型）、`xAI的数据中心.md`、GEV/Quanta 研究笔记及 WoodMac 供需数据；术语见 `行业背景/术语.md`。
> 口径：**1GW = 1GW IT Load**（进 IT 设备的功率）；电网入口 = IT × PUE（1.10–1.15）≈ **1.1–1.15GW**；视在功率 ÷ PF 0.95 ≈ **1.21GVA**。

**一句话**：电从电厂出来，要经历 **发电 → 升压并网 → 高压输电 → 园区主变电站 → 中压配电 → 机房配电（UPS/PDU）→ 机柜** 七级，每一级都有专用设备、专门的供应商，而目前**几乎每一级都在缺货**。

## 1. 全景链路

```text
【A. 发电】                    【B. 升压并网】              【C. 高压输电】
燃气电厂/核电/电网电            GSU 升压变压器               345/230/138kV 线路
~1.3GW 联合循环（情景）   →    430kV→345kV 等          →    （远距离可选 HVDC）
+ 备用/调峰                     + 开关站
                                    │
                                    ▼
【D. 园区主变电站】               【E. 中压配电】              【F. 机房配电】
主变 345→34.5kV                  MV/LV 变压器 → 480V          UPS（电池撑场）
~1.3–1.6GVA installed      →    数百台 2–5MVA           →    ~1.6GVA installed
GIS/AIS 开关、断路器              MV 开关柜、环网               PDU ~1.6GVA
保护/无功（STATCOM）                                          母线槽 Busway
                                    │                           │
                                    └───────────┬───────────────┘
                                                ▼
                                        【G. 机柜】
                                        Rack PDU / 母线 → 电源 shelf
                                        → 48V（→ 演进中 800VDC）→ GPU
```

每一级都做两件事：**变压**（电压一级级降下来）和**保护/冗余**（任何单点故障不能停机）。

## 2. 逐段拆解：设备、量级、谁供应

### A. 发电（情景变量，不是必选 BOM）

- 全电网供电 → **0 台燃机**完全成立；100% 表后自建 → 1GW IT ≈ **一座 1.3GW 联合循环电厂**（GE 7HA.03 ×3 = 1.29GW，N+1 则 4 台；或 2×1 联合循环 1,282MW）。([1GW 模型 §8][1])
- 现实案例 xAI：临时用 **69 台移动燃机**先把 GPU 跑起来，永久方案是 **41 台 Solar Titan-350 ≈ 1.2GW**（已获许可，尚未投产）。([xAI 笔记][2])
- 供应：GEV / Siemens Energy / Mitsubishi Power（重型机，交期 5–7 年）；Solar Turbines、GEV 航改机（中小机型，快但贵）。
- **如果烧气，还要天然气链**：气田 → 州际高压管道 → 厂区支管（xAI 案例：接 16 英寸主管）。
- **谁在建表后电厂**：完整玩家图谱见 `电力系统/表后发电阵营.md`（xAI、Chevron×Engine No.1×GEV、NRG×GEV×Kiewit、Stargate/Crusoe、Homer City 等；美国已宣布 ~101 GW）。

### B. 升压并网（发电侧出口）

- 设备：**GSU 升压变压器**（发电机出口 → 输电电压）、开关站。
- 瓶颈之王：GSU 交期 **144 周**、价格较 2019 +45%，需求 5 年 +274%。([WoodMac/POWER][3])

### C. 高压输电

- 设备：345/230/138kV 架空线/电缆、塔基；远距离/海上/跨国场景用 **HVDC**（换流站是价值核心）。
- 施工：Quanta 这类承包商（765kV 特高压美国最有经验建设商）；设备：GEV/Hitachi Energy/Siemens Energy。
- xAI 案例：厂址原有接入仅 **8MW**，自费建变电站 + 升级 161kV 线路才到 150MW——**"等电网"是最长的串行路径**。([xAI 笔记][2])

### D. 园区主变电站（数据中心的大门）

- 设备：**主变**（345/138kV → 34.5kV 中压）、GIS/AIS 开关、断路器、继电保护、无功补偿（STATCOM/FACTS）、SCADA。
- 量级：工作视在 1.21GVA，加 N+1/维护裕量 → **installed ~1.3–1.6GVA**（工程模型值）。形态如 6×250MVA 主变。
- 交付形态：GEV Electrification 的 turnkey 变电站（澳洲 hyperscale 案例：132/22kV 整站）。
- 主变交期 128 周、+77% 涨价；美国 80% 大型变压器靠进口。([WoodMac/POWER][3])

### E. 中压配电（园区内）

- 设备：**MV/LV 配电变压器**（34.5kV → 480V，数百台 2–5MVA 级）、MV 开关柜、环网柜、电缆。
- 注意口径：主变 GVA 与配电变压器 GVA **必须分开统计**（1GW 模型 §7）。
- 中压开关柜也缺：交期 44 周，价格较 2021 +50%。([WoodMac/POWER][3])
- 供应：GEV（Prolec）、Eaton、Schneider、Hitachi Energy。

### F. 机房配电（楼内，Tier III 冗余）

- 设备链：**UPS**（市电中断时电池撑住，等柴发启动）→ **PDU** → **母线槽** → 柜内；备用**柴油发电机**。
- 量级：UPS installed **~1.6GVA/GW IT**、PDU 同量级（Vertiv reference，4-to-make-3 冗余）——installed 大于实际负载的部分全是冗余。
- 供应：**Vertiv、Eaton、Schneider**（表后配电三巨头；和 GEV 的电网侧错层）。

### G. 机柜级

- Rack PDU/母线 → 电源 shelf → 板上 48V 供电；Rubin 代在向 **800VDC** 架构演进（Eaton 等在推）。
- 这一级属于 IT 基础设施 BOM，见 `数据中心1GW.md`。

## 3. 1GW 数量级总表

| 链路环节 | 关键设备 | 1GW IT 量级 | 主要供应商 | 当前交期/状态 |
|---|---|---|---|---|
| A 发电（表后情景） | 联合循环电厂 | ~1.3GW（7HA.03×3–4） | GEV/SE/MHI | 燃机 5–7 年 |
| B 升压 | GSU 变压器 | 数台大型 GSU | GEV/Hitachi/SE | **144 周** |
| C 输电 | 高压线路/HVDC | 视距离 | Quanta 施工 + 三家设备 | 施工排期紧 |
| D 主变电站 | 主变 + GIS + 保护 | ~1.3–1.6GVA installed | GEV Elec. turnkey | **128 周** |
| E 中压配电 | 配电变 + MV 开关柜 | 数百台 2–5MVA | GEV/Eaton/Schneider | 开关柜 44 周 |
| F 机房配电 | UPS + PDU + 柴发 | 各 ~1.6GVA | Vertiv/Eaton/Schneider | 紧张但好于主变 |
| G 机柜 | Rack PDU/电源 shelf | ~6,400 柜（GB300） | Vertiv/台达等 | 随 GPU 交付 |

## 4. 瓶颈排序（哪一级最卡）

按交期和供给刚性排：**① GSU/主变（128–144 周，GOES 卡脖子）≈ ② 重型燃机（5–7 年，若选表后发电）> ③ MV 开关柜（44 周）> ④ UPS/PDU（相对好）**。所以现实中 AI 园区的关键路径是：**变压器 slot + 并网审批 + （如自建）燃机 slot**——xAI 用"移动燃机 + 自接送电"绕开前两个，这就是它 122 天上线的本质。([xAI 笔记][2])

## 5. 映射到研究标的

| 环节 | 标的 | 对应笔记 |
|---|---|---|
| 发电设备 | **GEV Power**（燃机） | `电力系统/GEV.md` §2 |
| 升压/变电站/输电设备 | **GEV Electrification**、Hitachi Energy、Siemens Energy | `电力系统/GEV.md` §3 |
| 输电/变电站施工 | **Quanta (PWR)** | `电力系统/Quanta.md` |
| 机房配电（UPS/PDU/液冷） | Vertiv、Eaton、Schneider | 待立项 |
| 备用柴发 | Cummins、Caterpillar | 未覆盖 |
| 天然气管道 | 州际管道公司 | `xAI的数据中心.md` §4 |

**GEV 的特殊性一眼可见：A–D 级它全都卖**（燃机 + GSU + 主变 + turnkey 变电站 + 电网软件），这就是"双卡位"在物理链路上的具体含义。

## 6. 来源与核实记录

1. `数据中心/数据中心1GW.md` —— 1GW 物理模型 V1.0（PUE、GVA 口径、燃机情景、UPS/PDU 1.6GVA）
2. `数据中心/xAI的数据中心.md` —— 8MW→150MW 并网、69 台移动燃机、41 台 Titan-350 1.2GW、天然气链
3. [POWER Magazine / Wood Mackenzie Q2'25 变压器调查](https://www.powermag.com/transformers-in-2026-shortage-scramble-or-self-inflicted-crisis/) —— 交期与涨价
4. `电力系统/GEV.md`、`电力系统/Quanta.md` —— 供应商与施工商定位

核实记录：2026-09-02 初稿。量级数字均引自上述已核实笔记；§3 总表 D/E 级 GVA 为工程模型值（1GW 模型注明"未经 reference 验证"），引用时注意。

> 后续的 2027 项目级设备、接电和 commissioning 台账见 [2027新增数据中心电力上游台账.md](2027新增数据中心电力上游台账.md)。该台账明确区分设备订单、接电与 Active IT，避免按变压器台数或厂商市占率直接相加。
