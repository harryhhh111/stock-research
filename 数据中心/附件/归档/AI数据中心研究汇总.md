# AI 数据中心研究笔记（汇总版）

> **归档状态：2026-09-17 起不再维护，也不作为当前研究结论来源。** 本文是早期综合笔记，包含已被后续专项文档替代、且部分口径已过时的内容（尤其是 2026/2027 新增上电 GW 与 NVIDIA 上电量）。
>
> 请使用：[建设进度2026-2029.md](../../建设进度2026-2029.md)（新增 Active IT 与项目台账）、[数据中心1GW.md](../../数据中心1GW.md)（物理 BOM）、[价值量测算.md](../../价值量测算.md)（CapEx）、[NVDA/机柜出货量预测.md](../../../NVDA/机柜与架构/机柜出货量预测.md)（机柜 shipment）及各专项研究。保留本文仅为追溯早期假设。

> 本文整理自本次对话中关于 AI 数据中心的连续讨论。  
> 目标：把零散回答整理为一份可以继续迭代的研究底稿。  
> 说明：为了可读性，去掉了重复表述，但保留了关键结论、假设、公式、区间和推演逻辑。

---

## 目录

1. AI 数据中心 vs 传统数据中心
2. AI 数据中心产业链
3. 全球数据中心分布与 GW 规模
4. High-density AI Factory 的核心特征
5. GB300 vs Vera Rubin
6. POD、CMX、KV Cache
7. 1GW AI Factory 标准模型
8. GB300 1GW BOM
9. Rubin 1GW BOM
10. Rubin vs GB300：单位 GW 效率
11. SSD / Local SSD / Shared AI Storage / CMX
12. NVIDIA 2026/2027 机柜出货预测
13. 2026/2027 全球新增数据中心 GW 与 NVIDIA 占比
14. NVIDIA 之外还需要哪些设备
15. 1GW AI 数据中心建设成本
16. 当前模型中的关键假设与待验证项

---

# 1. AI 数据中心 vs 传统数据中心

AI 数据中心并不是一种完全不同于传统机房的新建筑，本质上仍然是：

- 建筑
- 电力
- 网络
- 制冷
- IT 设备

但 High-density AI Factory 的工程特征已经和传统服务器机房明显不同。

## 1.1 最核心区别

传统数据中心：

> 在一个建筑里放很多相对独立的服务器。

AI Factory：

> 试图把整个数据中心做成一台巨型超级计算机。

传统服务器主要承担：

- 网站
- 数据库
- ERP
- SaaS
- 虚拟机
- 文件服务
- 普通云服务

大型 AI 训练 / 推理集群则要求成千上万颗 GPU 高度协同：

- GPU ↔ GPU 高频同步
- 巨大的 East-West 流量
- 高带宽低延迟网络成为计算系统的一部分

## 1.2 典型区别

| 指标 | 传统数据中心 | High-density AI Factory |
|---|---|---|
| 核心芯片 | CPU | GPU / XPU |
| 基本单位 | Server | Rack / POD / Cluster |
| Rack 功率 | 5–20kW 常见 | 100–200kW+ |
| 冷却 | 风冷为主 | Direct Liquid Cooling 为核心 |
| 网络 | 普通 Ethernet | NVLink + RDMA + 400G/800G/1.6T |
| 流量 | North-South 较多 | East-West 极大 |
| 存储 | 容量/可靠性 | 容量 + 吞吐量 + KV/Context |
| 关键资源 | 空间 + 可靠性 | MW + Network + Cooling |
| 本质 | 很多电脑 | 一台数据中心尺寸的超级计算机 |

---

# 2. AI 数据中心产业链

可以把整个产业链拆成：

1. AI 芯片：NVIDIA、AMD、Google TPU、AWS Trainium 等
2. HBM：SK hynix、Micron、Samsung
3. CPU / DRAM
4. AI 服务器 / Rack：Supermicro、Dell、HPE、Foxconn、Quanta、Wistron 等
5. Scale-up 网络：NVLink / NVSwitch
6. Scale-out 网络：Ethernet / InfiniBand / Spectrum-X
7. 光通信：800G / 1.6T、DSP、laser、fiber
8. SSD / NAND / Shared Storage / CMX
9. Power Train：Transformer、Switchgear、UPS、PDU、Busway
10. Liquid Cooling：CDU、Cold Plate、Manifold
11. Facility Cooling：Chiller、Cooling Tower、Dry Cooler
12. Building / EPC / Land
13. Grid / Gas / Nuclear / BESS
14. Cloud / Neocloud：CoreWeave、Nebius 等
15. 最终 AI 客户：OpenAI、Anthropic、Meta 等

---

# 3. 全球数据中心分布与 GW 规模

研究数据中心最适合统一用：

> **IT Power Capacity（MW / GW）**

而不是 FLOPS。

原因：

- 不同 GPU / TPU 精度口径不同
- 利用率不同
- 软件栈不同
- 但 1GW IT Load 是统一物理尺度

## 3.1 全球格局

全球数据中心用电高度集中在：

- 美国
- 中国

美国 + 中国约占全球数据中心用电大头。

大致量级：

- 美国：50GW+ 级
- 中国：30–40GW 级
- 德国：约 3GW
- 英国：约 2–3GW
- 日本：约 1.5–2GW
- 印度：约 1.5GW
- 新加坡：1GW+，密度极高

## 3.2 大型单体园区开始进入 GW 时代

过去：

> 100MW 已经算巨型数据中心。

现在：

> 1GW、2GW、5GW 级 AI campus 开始出现。

典型公开规划中出现过：

- Meta Hyperion：5GW 级
- Stargate UAE：5GW 园区
- OpenAI Stargate：多 GW
- 大型美国园区：1–2GW+
- 中东：多 GW

---

# 4. High-density AI Factory 的核心特征

## 4.1 Rack 功率快速提升

大致演进：

- H100 SuperPOD：约 40.8kW/rack（32 GPU）
- GB300 NVL72：约 142kW/rack（72 GPU）
- Vera Rubin NVL72：约 227kW/rack（72 GPU）

GPU 数没增加，但 Rack 功率显著增加。

这意味着：

> 同样 1GW，能容纳的 GPU 数会下降。

## 4.2 网络越来越重要

AI Factory 中网络不再只是“连接设备”，而是计算机的一部分。

从：

- 400G
- 800G
- 1.6T

不断升级。

Rubin 还开始引入：

- Silicon Photonics
- CPO（Co-Packaged Optics）

因此：

> 网络带宽/GW 可能继续增加，即使 GPU/GW 下降。

---

# 5. GB300 vs Vera Rubin

## 5.1 核心规格

| 指标 | GB300 NVL72 | Vera Rubin NVL72 |
|---|---:|---:|
| GPU | 72 × B300 | 72 × Rubin |
| CPU | 36 × Grace | 36 × Vera |
| HBM/GPU | 288GB HBM3E | 288GB HBM4 |
| HBM 带宽/GPU | ~8TB/s | ~22TB/s |
| NVLink/GPU | ~1.8TB/s | ~3.6TB/s |
| Scale-out | ~800Gb/s/GPU | ~1.6Tb/s/GPU |
| Rack 功率 | ~142kW | ~227kW |
| GPU 数/Rack | 72 | 72 |

## 5.2 最关键变化

Rubin 不是简单“更快的 GPU”，而是整套系统升级：

- HBM3E → HBM4
- HBM 带宽大幅提高
- NVLink 翻倍
- Scale-out 网络翻倍
- Grace → Vera
- BlueField-3 → BlueField-4
- 更强的 Context Memory / CMX
- 更高 Rack 功率
- 更高液冷密度

## 5.3 Vera CPU 为什么需要 1.5TB LPDDR5X

重点不是“CPU 自己跑程序要这么多内存”。

核心用途：

1. 给 GPU 提供第二级大容量高速内存池
2. KV Cache offload
3. Request / Session 状态
4. Agent runtime / sandbox
5. Data staging
6. CPU-side orchestration

可以理解成：

- HBM = GPU 手边的超高速工作台
- LPDDR = GPU 旁边的大货架
- CMX / NVMe = 更大的共享上下文缓存层

每颗 Vera：

> 1.5TB LPDDR5X

36 颗 Vera：

> 54TB LPDDR5X / NVL72

相比 Grace 时代约 17TB，增长约 3 倍。

---

# 6. POD、CMX、KV Cache

## 6.1 POD 是什么

POD：

> 一组预先设计好、作为一个整体工作的机架。

层级：

GPU  
→ Compute Tray / Server  
→ Rack  
→ POD  
→ Cluster / AI Factory  
→ Data Center

POD 不是固定 GPU 数量的统一标准。

它是：

> 标准化、可复制的集群单元。

## 6.2 Vera Rubin POD

Rubin POD 不再只是很多 GPU Rack。

而是组合：

- Rubin NVL72 Compute Rack
- Vera CPU Rack
- Spectrum-6 Networking Rack
- BlueField-4 / CMX Context Memory Rack
- 其他专用推理/支持系统

所以 Rubin 越来越接近：

> POD-scale AI supercomputer

## 6.3 KV Cache 是什么

Transformer 推理时，为了避免每生成一个 token 都重新计算全部历史 token，会缓存历史 token 的 Key / Value 中间结果。

这就是：

> KV Cache

它不是：

- 模型参数
- 用户数据库
- 长期记忆

而是：

> 推理过程中的可重算临时状态。

## 6.4 CMX 是什么

CMX：

> 面向 Context / KV Cache 的高速共享存储层。

它不是普通 Shared Storage。

主要服务：

- 长上下文
- 多轮推理
- Agentic AI
- 大量并发 Agent

CMX 的意义是：

> 不让大量“暂时不用但之后还会用”的 KV Cache 长时间占据昂贵 HBM。

---

# 7. 1GW AI Factory 标准模型

以后统一：

> **1GW = 1GW IT Load**

不是电网入口。

如果 PUE = 1.10–1.15：

> 电网实际 operating load ≈ 1.10–1.15GW

---

# 8. GB300 1GW BOM

我们用 Vertiv + Schneider 两套完整 Reference Design 交叉验证。

## 8.1 GPU/GW

Vertiv：

- 4.992MW IT
- 32 × GB300 NVL72 Compute Rack
- 32 × Support Rack

对应：

> ~461,538 GPU/GW

Schneider：

- 7.536MW IT
- 3 × 1,152 GPU cluster

对应：

> ~458,599 GPU/GW

两者差异极小。

所以固定：

> **GB300 ≈ 46 万 GPU / GW IT**

## 8.2 Compute Rack 占 IT 比例

Vertiv：

> Compute Rack ≈ 91%

Schneider：

> Compute Rack ≈ 90.5%

所以可以用：

> **GB300 完整 AI Factory 中约 90–91% IT 功率进入 NVL72 Compute Rack，约 9–10% 为外部网络/存储/Support IT。**

## 8.3 1GW GB300 基础 BOM

约：

- 6,390–6,400 个 NVL72 Compute Rack
- 460,000 B300 GPU
- 230,000 Grace CPU
- 115,000 Compute Tray
- 57,500 NVSwitch Tray
- 460,000 ConnectX-8
- 115,000 BlueField-3

## 8.4 HBM

每 GPU：

> 288GB HBM3E

所以：

> 460,000 × 288GB ≈ 132.5PB

结论：

> **GB300 ≈ 132.5PB HBM3E / GW**

## 8.5 网络

NVIDIA 8-rack reference：

- 576 GPU
- ~3,524 transceiver positions

即：

> ~6.12 transceiver positions / GPU

1GW：

> 460,000 × 6.12 ≈ 281 万个 transceiver BOM-equivalent

注意：

> 281 万 ≠ 281 万个 800G 光模块

因为其中还包括：

- breakout
- 双端口 OSFP
- 铜
- 不同速率
- 不同端点

## 8.6 UPS / PDU

Vertiv reference：

- 4.992MW IT
- 8MVA installed IT UPS

所以：

> **~1.6GVA installed UPS / 1GW IT**

PDU 也约：

> **~1.6GVA / GW**

## 8.7 液冷

GB300 reference：

> ~78% liquid  
> ~22% air

所以 1GW IT：

- Liquid cooling physical load ≈ 780MW thermal
- Air cooling ≈ 220MW thermal

---

# 9. Rubin 1GW BOM

Rubin 的 1GW 口径更复杂。

存在两种视角：

1. Compute Rack 理论极限
2. 完整 Full-stack AI Factory

## 9.1 NVIDIA 官方尺度

公开口径可以用：

> **约 30 万 Rubin GPU / GW**

这个比纯机柜功率直接除得到的理论极限更合理。

所以第一版固定：

> **Rubin ≈ 30 万 GPU / GW**

## 9.2 Compute Rack

72 GPU/rack：

> 300,000 ÷ 72 ≈ 4,167 Rack/GW

## 9.3 HBM

每 Rubin GPU：

> 288GB HBM4

所以：

> 300,000 × 288GB ≈ 86.4PB HBM4/GW

如果使用更完整、支持系统更重的厂商方案，GPU/GW 可能更低。

因此 Rubin 的 HBM/GW 需要继续按实际 Factory 架构区分。

---

# 10. Rubin vs GB300：单位 GW 效率

## 10.1 GPU 数

GB300：

> ~46 万 GPU/GW

Rubin：

> ~30 万 GPU/GW（官方尺度）

Rubin GPU/GW 下降约：

> 35%

如果采用更完整 Full-stack 方案，下降幅度可能接近 50%。

## 10.2 峰值 FP4 inference

粗略：

GB300：

> ~20 PFLOPS sparse FP4 / GPU

Rubin：

> ~50 PFLOPS NVFP4 / GPU

所以单 GPU：

> Rubin ≈ 2.5× GB300

如果用：

- GB300：46 万 GPU/GW
- Rubin：30 万 GPU/GW

则：

GB300：

> 460k × 20PF ≈ 9.2 ZFLOPS/GW

Rubin：

> 300k × 50PF ≈ 15 ZFLOPS/GW

提升约：

> **~63% / GW**

如果采用更保守的 23 万 GPU/GW Full-stack Rubin，则提升约 25%。

因此 Rubin 的单位 GW 峰值算力提升大致可看成：

> **+25% 到 +60%+**

取决于完整 Factory 支持系统占比。

## 10.3 实际 token/MW

真实 token/MW 的提升大概率高于简单 FLOPS/MW，因为 Rubin 同时提升：

- HBM 带宽
- NVLink
- 1.6T 网络
- KV Cache reuse
- CMX
- 软件栈

但缺少公开、同模型、同 QoS 的 GB300 vs Rubin 直接 benchmark。

---

# 11. SSD / Local SSD / Shared AI Storage / CMX

必须拆成三层：

1. Local SSD
2. Shared AI Storage
3. CMX

## 11.1 Local SSD

### GB300

典型 5 盘配置：

- 4 × 3.84TB E1.S
- 1 × 1.92TB boot

每 tray：

> 17.28TB

约 115,000 tray/GW：

> **~1.99EB Local SSD / GW**

高配 reference 可到约：

> ~3.9EB/GW

所以基准：

> **GB300 Local SSD ≈ 2.0EB/GW**

### Rubin

每 tray：

- 4 × E1.S data
- 1 × boot

约 5 块 SSD/tray。

按 ~30 万 GPU/GW：

- ~75,000 compute tray/GW
- ~37.5 万块普通 NVMe

如果沿用类似容量：

> **~1.3EB Local SSD / GW**

排除 CMX 后：

> Rubin 普通 Local SSD 比 GB300 少。

## 11.2 Shared AI Storage

Shared AI Storage：

> 整个 GPU 集群共同使用的共享存储池。

主要存：

- Dataset
- Checkpoint
- 模型文件
- 训练数据
- Log
- Intermediate output

它不是 AI 特有新硬件。

只是：

> 高吞吐共享文件 / 对象存储。

建模时可以暂用：

> **1TB usable Shared Storage / Training GPU**

作为工程基准参数。

## 11.3 CMX

CMX 主要存：

> KV Cache / Context Memory

不是普通 Local SSD。

我们之前采用的建模假设：

> **16TB CMX SSD / CMX-enabled Rubin GPU**

注意：

> 这是产业链估算参数，不是 NVIDIA 固定 BOM。

## 11.4 Workload Mix 假设

假设：

- 推理占 AI Compute：2/3
- 训练：1/3
- 推理中一半需要 CMX

则整个 1GW 被分成：

- 1/3 Training
- 1/3 普通 Inference
- 1/3 CMX Inference

### GB300 SSD/GW

GB300：

- Local SSD ≈ 1.99EB
- Training Shared Storage ≈ 0.15EB
- CMX = 0

合计：

> **~2.14EB SSD / GW**

### Rubin SSD/GW

Rubin：

- Local SSD ≈ 1.30EB
- Training Shared Storage ≈ 0.10EB
- CMX ≈ 1.60EB

合计：

> **~3.0EB SSD / GW**

因此：

> Rubin SSD/GW 比 GB300 高约 40%，增量主要来自 CMX。

---

# 12. NVIDIA 2026/2027 机柜出货预测

## 12.1 2026

Base Case：

> **~5.2 万柜**

合理区间：

> 4.7–5.7 万

拆分：

- GB300：~4 万柜
- Vera Rubin：~1 万柜
- GB200 尾单/其他：~0.2 万

## 12.2 2027

Base Case：

> **~8 万柜**

合理区间：

> 6.8–9.5 万

高盛模型约：

> 7.7 万柜

大致结构：

- Vera Rubin：4.5–5.0 万柜
- Rubin Ultra：2.7–3.2 万柜
- 少量 GB300 尾单

## 12.3 生命周期数量级

大致：

- GB200：2025 年 ~2.0–2.4 万柜
- GB300 生命周期：~4.8 万柜
- Vera Rubin 生命周期：~5.8 万柜

---

# 13. 2026/2027 全球新增数据中心 GW 与 NVIDIA 占比

我们定义：

> 新增 GW = 当年真正上电 / 投产的 IT capacity

Base Case：

| 年份 | 全球新增上电 DC | NVIDIA 实际上电 |
|---|---:|---:|
| 2026E | ~15GW | ~8.7GW |
| 2027E | ~25GW | ~15GW |

## 13.1 2026 NVIDIA GW

约：

- 4 万柜 GB300
- 1 万柜 Rubin

GB300：

> 40,000 ÷ 6,400 ≈ 6.25GW

Rubin：

> 10,000 ÷ 4,167 ≈ 2.4GW

合计：

> **~8.65GW**

所以：

> NVIDIA 约占 2026 全球新增 GW 的 ~58%

## 13.2 2027

机柜出货不能直接等于当年上电 GW。

因为：

- Rack 可能提前到货
- 数据中心可能晚于机柜上电
- 电网 / 变电站 / 冷却可能延迟
- Rubin Ultra 机柜功率更高

因此 Base Case：

> **2027 NVIDIA 实际新增上电 ≈ 13–16GW**

中值：

> **~15GW**

---

# 14. NVIDIA 之外还需要哪些设备

完整 BOM 树：

## 14.1 发电 / 电网

- Main Transformer
- GIS / AIS
- Protection Relay
- Substation
- Gas Turbine（可选）
- Backup Generator
- BESS / Battery / Supercapacitor

典型供应商：

- Hitachi Energy
- Siemens Energy
- GE Vernova
- Eaton
- Schneider

## 14.2 中低压配电

- MV Transformer
- MV Switchgear
- LV Switchgear / MSB
- UPS
- PDU
- RPP
- Busway / Busbar
- Rack Power Shelf
- Rack PDU

供应商：

- Vertiv
- Schneider
- Eaton
- Siemens
- Delta
- Lite-On

## 14.3 液冷

- CDU
- Cold Plate
- Manifold
- Hose / Quick Disconnect
- Leak Detection

供应商：

- Vertiv
- Motivair
- nVent
- CoolIT
- Boyd

## 14.4 Facility Cooling

- Chiller
- Cooling Tower
- Dry Cooler
- Pump
- Heat Exchanger
- CRAH / Fan Wall

供应商：

- Trane
- Carrier
- Johnson Controls
- Vertiv
- Schneider
- Alfa Laval

## 14.5 网络

- Leaf Switch
- Spine
- Super-Spine
- 800G / 1.6T 光模块
- AEC
- DAC
- Fiber
- OOB Management Switch

供应链包括：

- NVIDIA
- Arista
- Broadcom
- Coherent
- Lumentum
- Credo
- Corning
- Cisco

## 14.6 存储

- Local NVMe SSD
- Shared Storage SSD
- CMX SSD
- Storage Server / Array

供应商：

- Kioxia
- Samsung
- Micron
- Solidigm
- DDN
- Pure Storage
- 其他 storage vendor

## 14.7 第三方服务器器件

- HBM3E / HBM4
- LPDDR5X
- PCB
- Rack / Chassis
- PSU
- Connector
- Busbar
- MLCC / ABF 等

## 14.8 建筑 / 运维

- Fire Suppression
- Leak Detection
- BMS
- EPMS
- DCIM
- SCADA
- Physical Security
- Steel Structure
- Cable Tray
- Piping
- Commissioning

---

# 15. 1GW AI 数据中心建设成本

我们前面形成的核心结论：

> **1GW 高密度 AI Factory 完整投资约 $50–60B**

## 15.1 粗拆

| 项目 | 约 1GW CapEx |
|---|---:|
| GPU/CPU/NVLink/HBM 等 Compute Rack | ~$25B |
| 外部 Network / Optics | ~$4.5–6B |
| Building + Power + Cooling Facility | ~$10–13B |
| Storage / Land / Engineering / Grid / Commissioning 等 | ~$5–10B+ |
| 可选自建燃气电厂 | 另加 ~$3B |
| 总计 | **~$50–60B/GW** |

## 15.2 Compute Rack 价值

市场 BOM 估算：

- GB300 NVL72：约 ~$4M/rack
- Vera Rubin NVL72：约 ~$7.8M/rack

GB300：

> ~6,400 rack/GW × ~$4M ≈ ~$25.6B/GW

Rubin：

如果完整 Factory 中 Rack 数下降、单柜价格上升：

> 核心计算系统 CapEx/GW 仍大致在 ~$25B 级

所以：

> Rubin GPU 数/GW 下降，不代表客户每 GW 少花很多钱。

## 15.3 Facility

不包含 active IT equipment 的数据中心建设成本大致：

> **~$10–13B/GW IT**

包含：

- Power
- Cooling
- Building
- UPS
- PDU
- Chiller
- Busway
- Mechanical
- Electrical

## 15.4 自建天然气电厂

如果 1GW IT、PUE ~1.15：

> Facility load ~1.15GW

若 100% onsite gas：

大致相当于：

> 一座 ~1.3GW Combined Cycle Power Plant

CapEx：

> 约 ~$3B 级

但：

> 不是所有 AI 数据中心都需要自建燃气电厂。

---

# 16. 当前模型中的关键假设与待验证项

## 16.1 已经相对可靠

### GB300

- ~46 万 GPU/GW
- ~132.5PB HBM3E/GW
- ~2EB Local SSD/GW
- ~1.6GVA UPS/GW reference
- ~0.78GW liquid cooling/GW
- ~6,400 NVL72/GW

这些得到多个 Reference Design 交叉验证。

## 16.2 Rubin 仍需继续验证

关键变量：

- 实际 GPU/GW
- Full-stack vs Training-heavy Factory
- Rubin Ultra 电气架构
- 800VDC adoption
- CPO 渗透
- CMX adoption
- CMX TB/GPU
- Vera LPDDR 真实 BOM
- Rubin Shared Storage 结构

## 16.3 SSD 模型最大敏感项

不是 Shared AI Storage。

而是：

> **CMX penetration × TB per CMX-enabled GPU**

目前建模：

> 16TB/GPU

如果这个参数变化：

Rubin SSD/GW 会剧烈变化。

## 16.4 数据中心新增 GW 最大不确定性

2027 尤其明显。

原因：

- 电网连接
- 变电站
- Transformer shortage
- Cooling commissioning
- HBM
- Packaging
- Rack delivery
- Utility delay
- Site delay

所以：

> Rack shipment ≠ energized GW

两者必须分开。

---

# 当前用于后续研究的 Base Case

为了后面继续算产业链收入，可以暂时固定：

## 2026

- 全球新增 DC：~15GW
- NVIDIA：~8.7GW
- NVIDIA Rack：~5.2 万柜
- GB300：~4 万柜
- Rubin：~1 万柜

## 2027

- 全球新增 DC：~25GW
- NVIDIA 上电：~15GW
- NVIDIA Rack shipment：~8 万柜
- Rubin 为主
- Rubin Ultra H2 开始放量

---

# 最值得继续深挖的 5 个问题

1. 1GW 中网络 / 光模块的真实美元价值量
2. Transformer / Switchgear / UPS / Busway 的 1GW 完整电气 BOM
3. Rubin / Rubin Ultra 的 800VDC 对 Vertiv、Eaton、Schneider 的影响
4. CMX 最终渗透率与 TB/GPU
5. 2026/2027 AI 数据中心新增 GW 对 HBM、NAND、液冷、电力设备各自的实际收入池

---

# 一句话总结

AI 数据中心的研究核心，不应该是简单问：

> “有多少 GPU？”

而应该统一转换成：

> **GW → Rack → GPU → HBM / SSD / Network → Power / Cooling → CapEx → 各供应商收入**

当前最适合长期使用的基准：

- GB300：约 **46 万 GPU/GW**
- Rubin：约 **30 万 GPU/GW**（仍需按 Factory 类型继续细分）
- GB300 SSD：约 **2.1EB/GW**（含少量 Shared Training Storage）
- Rubin SSD：约 **3.0EB/GW**（假设 1/3 总算力使用 CMX，16TB/GPU）
- 1GW AI Factory 总投资：约 **$50–60B**
- 2026 NVIDIA 新增上电：约 **8.7GW**
- 2027 NVIDIA 新增上电：约 **15GW**
