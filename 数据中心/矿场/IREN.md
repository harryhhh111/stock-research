# IREN：比特币矿场 → AI 算力的转型样本（大型）

> 整理/核对日期：2026-08-28（由 7 段问答精简整合；含 FY26 财报 2026-08-27 更新。2026-08-28：§3 补回 BOM/supercluster/赶工费细项，新增 §4 单柜收入两层拆解、§5 厂房两本账，§8 扩为完整规格表）。
> 研究定位：与 `HIVE.md` 同框架的矿场转型样本（IREN = 大型、自持机房版）。合同口径细节在 `../合同/AI算力合同.md`，本文只留指针。

**一句话结论**：IREN 已从矿企变成**高杠杆 AI 基础设施开发商 + GPU Cloud**——矿机 2026 年底全部退出（FY26 计提 $638.8M 减值），Microsoft $9.7B 首单 Horizon 1 已交付，2026 产能基本售罄、年底 ARR 目标 >$4B，**新签 3 年合同价格 >$20M/MW/年（比 2025-11 的 Microsoft 单价翻倍以上）**。但单项目全口径 CapEx $8.1–8.5M/柜 vs 首份 5 年合同 EBITDA $7.81M/柜（0.92–0.96×）——**第一份合同只够回本，真正的回报在数据中心资产的第二代设备上**。

## 1. 公司现状与转型（FY26 财报，2026-08-27，[10][11]）

- 沿革：原名 Iris Energy，2024 改名 IREN；模式 = **自持电力 + 土地 + 自建数据中心 + 买 GPU 出租**（与 HIVE 租 Bell 机房相反）
- 收入轨迹：FY25 $511M（97% 来自三个矿池，AI Cloud 仅 $16.4M [3]）→ FY26 $707M，其中 **AI Cloud $128.8M**（Q4 单季 $70.5M，环比翻倍）
- **矿机退出**：管理层明确 2026 年 12 月底 Bitcoin mining 基本全部 decommission，FY26 计提 **$638.8M 减值**（Q3 时预估 ~$520M，Q4 单季实际 $450.4M）；Q3 FY26 收入下降的原因之一就是 GPU 安装前提前退役部分矿机（管理层定性为 ASIC→GPU 转换）[2]——"矿场改 AI 还是另建"的争论已有答案：**拆矿机，电力和站点全转 GPU**
  - **退出成本口径**：$638.8M ÷ 750MW ≈ **$0.85M/MW**——约等于矿机原始采购成本（$0.85–0.93M/MW），也约等于 2025-05 环境下 ~1.1 年的挖矿现金利润（$0.75M/MW/年，由 Q3 FY25 的 hashprice $54 / hash cost $23 推算 [15]）。注意：减值是账面损失**非现金流出**；拆除/处置现金费用未单独披露；提前退役的机会成本未量化
- AI Cloud 直接毛利率：Q4 直接成本仅 $9.2M → **~87%**（不含折旧/SG&A/融资）[11]
- ARR 轨迹：Q4 末 $0.5B → Horizon 1 验收后 operating ARR **$1B** → 2026-12 季度末目标 **>$4B**（~85% 已签约）；但大量设备季末上线，GAAP 收入大部分要到 **2027-03 季度**才体现

## 2. 客户与合同（细节见 `../合同/AI算力合同.md` §1/§2）

| 合同 | 规模 | 状态（2026-08） |
|---|---|---|
| Microsoft $9.7B / 5 年 / GB300 | Horizon 1–4 共 200MW critical IT | **Horizon 1（50MW / ~264 柜）已交付验收**；H2 commissioning；H3–4 late-stage；**全部 2026 Q4 交付** [5][11] |
| NVIDIA $3.4B / 5 年 / 风冷 Blackwell 60MW | 含 Mirantis 编排 + $2.1B 认股权证 | 2027 初 ramp |
| 2026-07 新增 ≈$2.8B AI 客户合同 | — | — |
| 客户名单 | Microsoft、NVIDIA、Perplexity、Figure AI、Together AI、Fluidstack、Fireworks AI、Fal AI、Hume AI | 2026 产能基本卖完 |

截至 2026-03 已安装/订购 ~15 万张 GPU [2]。

## 3. Microsoft 项目 CapEx 全拆解（[6]）

**$14–16M/MW IT 不是模糊的"行业成本"，IREN 官方拆成三部分**：

| 每 1MW IT | 金额 | 内容 |
|---|---:|---|
| 基础数据中心基础设施 | **$9–11M** | Tier III 级机房（细项见下） |
| 100MW supercluster / 高密度架构升级 | **+$3M** | 支持 130–200kW/rack 灵活密度的集群架构升级 |
| 赶工费（2026 交付 200MW） | **+$2M** | 项目特有的非正常成本 |
| **合计** | **$14–16M** | × 200MW = **$2.8–3.2B** |

### ① $9–11M/MW = 真正的"数据中心"

IREN 原文定义：**data center infrastructure, Tier III equivalent concurrent maintainability**——把一块有电的土地变成能放 AI 服务器的数据中心所需的全部基础设施。IREN 未进一步公开 BOM，但结合 Horizon 1 已披露规格（full UPS + 柴发备份、direct-to-chip 液冷、200kW/rack），主要包括：

- 数据中心建筑/机房、土建、施工、工程设计
- 高压/低压配电系统、变压器、switchgear
- UPS、柴油发电机备用电源
- 母线、PDU 等机房配电
- 液冷基础设施（水泵、管路、CDU、换热设备）+ HVAC 辅助冷却
- 消防、控制系统、光纤及机房基础网络

一句话：**$9–11M/MW = 不含 GPU 计算设备，把 1MW AI IT 负载"托起来"的机房、电力、冷却和冗余基础设施**。

### ② +$3M/MW = supercluster 架构升级（Microsoft 特有）

IREN 原话："**$3m: deployment of 100MW supercluster architecture and flexible rack densities (130–200kW)**" [6]。Microsoft 要的不是一排排独立 GPU 柜，而是 100MW 级超大 GPU supercluster + 130–200kW/rack 极高密度。增量投资对应：更强的配电容量和母线设计、液冷能力、高密度机柜供电、集群拓扑相关机房布局、冗余和故障隔离、大规模集群布线的物理基础设施。

⚠️ **边界警示：不要把 InfiniBand 网络设备重复算进这 $3M**——IREN 明确 $5.8B GPU CapEx 里已含 servers、InfiniBand、cabling、deployment services、software、licensing [6]。$3M 只是数据中心侧为容纳 supercluster 做的架构升级，不是服务器/网络硬件本身。

### ③ +$2M/MW = 赶工费（项目特有的非正常成本）

IREN 原话："**$2m: acceleration costs to achieve 2026 delivery of full 200MW capacity**" [6]。构成：多施工面并行、加班/夜班、提前订长交期设备、expedited shipping、施工承包商加价、供应链排期溢价、设计与施工并行的额外成本。200MW × $2M = **$400M** 纯加速费——不是数据中心本身永久需要这么贵。

### 全项目口径

| | 金额 |
|---|---:|
| 基础数据中心（$9–11M × 200MW） | $1.8–2.2B |
| supercluster/高密度设计（$3M × 200MW） | $0.6B |
| 赶工（$2M × 200MW） | $0.4B |
| **数据中心 CapEx 小计** | **$2.8–3.2B** |
| GPU 相关 CapEx（GPU+服务器+InfiniBand+布线+部署+软件许可） | $5.8B |
| **总项目 CapEx** | **$8.6–9.0B** |
| Microsoft 5 年合同收入 | $9.7B |

**单柜账（≈1,056 柜，反推值）**：

| 每柜（约 5 年） | 金额 |
|---|---:|
| 分摊 GPU/网络等 CapEx（$5.8B÷1,056） | ≈$5.49M |
| 分摊数据中心 CapEx（$2.8–3.2B÷1,056） | ≈$2.65–3.03M |
| **全口径项目 CapEx** | **≈$8.1–8.5M** |
| 合同收入 | ≈$9.19M |
| 直接 Opex（15%） | −≈$1.38M |
| **项目 EBITDA（85% margin）** | **≈$7.81M ≈ CapEx 的 0.92–0.96×** |

> **修正纪律**：不要再说"$5.5M 买一柜、$9.2M 卖出（1.67×）"——那漏掉了 $2.8–3.2B 数据中心投资。正确理解：**首份合同 EBITDA 甚至不能完整覆盖全部初始 CapEx；投资逻辑是收回绝大部分成本后，IREN 仍拥有数据中心/电力/土地/冷却基础设施，换 Rubin/Feynman 继续赚钱。**
>
> **历史对比**：2025 Q3 Horizon 1 原设计仅 **$6–7M/MW**（已含 200kW/rack、UPS、柴发、液冷）；Microsoft 单的 Tier III 冗余 + supercluster 架构 + 赶工把它推到 $14–16M/MW。**估 1GW 建设成本时不能直接拿 $15M/MW × 1,000**——会把数据中心基建严重高估。

## 4. 单柜收入的两层拆解：$210/柜·h = $34 机房 + $176 算力（[16]）

**内部计价机制**：IREN 管理层披露，内部评估 Microsoft 项目时给 Horizon 数据中心单独计了一个 **~$130/kW/月的 internal colocation charge**（arm's-length、逐年上调），算 GPU Cloud IRR 时先扣掉它——即公司内部把业务拆成**数据中心/场地层 + GPU Cloud/算力层**分别计算回报 [16]。这是管理层自己的模型，不是外部估算。

换算（200MW = 200,000kW；1,056 柜 → ~189.4kW/柜）：

| 层级 | 每柜·小时 | 每柜·月 | 每柜·年 | 200MW 合计/年 |
|---|---:|---:|---:|---:|
| 数据中心/colo 层（$130/kW/月） | ≈$33.7 | ≈$24.6k | ≈$295k | **≈$312M** |
| GPU Cloud/算力层（剩余） | ≈$176 | ≈$128.5k | ≈$1.542M | ≈$1.63B |
| **Microsoft 全包价** | **≈$210** | **≈$153.1k** | **≈$1.837M** | **$1.94B ARR** |

四个要点：

1. **$312M/年 ≈ Microsoft ARR 的 ~16% 归场地层**——"数据中心值多少钱"有了公司自己的锚
2. **推论**：已有数据中心/电力/冷却、只想租整个 GB300 NVL72 算力柜的大客户 5 年长约隐含价 ≈ **$125–130k/柜/月（$175–180/柜·h）**——注意这是经济分拆价，不是对外挂牌的 rack rental price
3. **市场价 cross-check**：CoreWeave GB200 NVL72 on-demand $10.50/GPU·h = **$756/柜·h**（零售、按需、零长期承诺）[17]；IREN×Microsoft $210 是 5 年、1,000+ 柜、近 100% 利用率、带预付款的批发长约——口径完全不同，不构成"Microsoft 买便宜了"
4. **速记模型**：1 个 GB300 NVL72 柜 ≈ **$176 算力 + $34 机房 = $210 全包 / 小时**；以后估 1GW / 5,000 柜级项目收入直接乘机柜数，不必回到单 GPU 口径

## 5. 一个厂房的两本账：建成矿场 vs 建成 AI 数据中心（每 1MW IT）

口径：土地/电网已接通（这是矿企真正的存量资产，两种方案都从这里起步）；矿场 = 简易风冷厂房 + ASIC；AI = Tier III 数据中心 + GB300 集群（Microsoft 规格）。项目层面现金流，不含融资/税/折旧。矿场侧以行业口径 + HIVE 实测为锚（IREN 未单独披露矿场厂房造价）。

| 每 1MW IT | 建成比特币矿场 | 建成 AI 数据中心（GB300） |
|---|---:|---:|
| 厂房/机电建设 | **~$0.2–0.45M**（被动风冷"鸡舍"级，无冗余、无洁净要求 [13][14]） | **$14–16M**（Tier III + supercluster + 赶工，§3） |
| IT 设备 | **~$0.93M**（S21+ 级 ASIC：15 J/TH × $14/TH） | **~$29M**（GPU+服务器+InfiniBand+布线，$5.8B÷200MW） |
| **合计 CapEx** | **~$1.1–1.4M** | **~$43–45M**（≈矿场的 **30–40×**） |
| 年收入 | **~$0.75M**（HIVE FY27Q1 实测年化，⚠️ 无合同、随币价波动） | **$9.7M**（Microsoft 5 年长约）→ **>$20M**（2026 新签 3 年约） |
| 年现金利润 | **~$0.22M**（margin 近几季 49%→24% 剧烈波动） | **~$8.3M**（老合同 85% margin）→ **~$17M+**（新合同价） |
| 静态回本 | ~5–6 年（且收入端无保障） | 老合同 ~5 年（刚好回本）；新合同 GPU 投资 **~2 年回本**（管理层口径） |

**换算成一个 100MW 厂房**：

| 100MW | 矿场 | AI 数据中心 |
|---|---:|---:|
| 总 CapEx | ~$1.1–1.4 亿 | **~$43–45 亿** |
| 年收入 | ~$7,500 万 | $9.7 亿（老合同价）/ **>$20 亿**（新签价） |
| 年现金利润 | ~$2,200 万 | ~$8.3 亿 / **>$17 亿** |

四个要点：

1. **厂房本身在 AI 方案里只是零头**：矿场厂房 $0.2–0.45M/MW vs AI 机房 $14–16M/MW 差 ~40–70 倍听起来夸张，但两边真正的大头都是 IT 设备（ASIC $0.93M vs GPU $29M/MW）——"矿场转 AI"的本质是**在同一个电力壳里把设备投资放大 ~31 倍**
2. **收入差 ~13–27 倍，现金利润差 ~38–77 倍**：同样的 1MW，挖矿挣 $0.22M/年且无合同保障，AI 挣 $8.3–17M/年且有 3–5 年 take-or-pay
3. **风险结构相反**：矿场 CapEx 小、回本看似不慢，但收入完全暴露于币价/难度；AI CapEx 大两个数量级，但有长约 + 客户预付款覆盖 45–55% GPU CapEx（§7）对冲
4. **IREN 自己就是对照实验**：2025-05 公司还以 50 EH/s（×15 J/TH ≈ 750MW）为傲，给出 $588M illustrative Adj EBITDA ≈ **$0.78M/MW/年**（当时 hashprice 高点的乐观口径）[15]——15 个月后直接计提 $638.8M 减值、2026 年底全部退出挖矿。市场用脚投票的结论已写在财报里

> 口径注意：`HIVE.md` §3 的矿场静态回本 ~4.3 年**不含厂房建设**（只算 ASIC）；本节含厂房（+$0.2–0.45M/MW）后矿场回本拉长到 ~5–6 年。两节口径不同，引用时注意。

## 6. 产能规划与 MW 口径（⚠️ FY26 财报修正）

| 口径 | 2026 | 2027 | 远期 |
|---|---|---|---|
| **IT Load**（算机柜用这个） | **~300MW** | +~500MW → **~800MW** | — |
| **Gross capacity**（工程/供电侧） | — | **~1.2GW** | ~5GW secured power |

- **修正记录**：2026-05 管理层曾说"2026 480MW、2027 1,210MW"，当时没分清 gross/IT；FY26 电话会（8-27）明确 2026 ~300MW IT、2027 ~800MW IT，**1.2GW 是 gross** [10]。同理 Horizon 1–4 的 "300MW liquid-cooled deployment" 是 campus gross 口径，**Microsoft 合同只对应 200MW critical IT**——不能拿 300MW 算单价 [7]
- 2027 新增构成：Horizon 5–6（+~100MW IT）、Childress 矿场改 AI（先改造 50MW 现有矿场，再改 ~250MW 原风冷容量）、Sweetwater 1 首期（200MW IT，设计支持 Vera Rubin）、加拿大 Canal Flats 30MW 全转 AI、Prince George/Mackenzie 既有设施转 GPU [2]
- 园区储备：Childress 750MW、Sweetwater 1: 1.4GW、Sweetwater 2: 600MW、Oklahoma/Kiowa 1.6GW、加拿大 ~160MW + 西班牙等新项目 → **~5GW secured power**（⚠️ secured ≠ 已建成）[2]

## 7. FY26 财报的价格新信息（最重要）

管理层电话会（2026-08-27，[10]）：

- **3 年长约价格比 2025-11 涨 ~125%；5 年涨 ~70%**
- 最近签的 3 年合同定价 **>$20M/MW IT/年**；谈判中的 **~$25M/MW**；GPU 投资 **~2 年回本**
- 对照：Microsoft 老合同 $9.7M/MW/年 → **新算力单价已是其 ~2 倍**（与 Nebius 2026Q2 的 $20–25M/MW 互相印证 ✅，涨价周期全市场同步）
- **FY27 CapEx 指引 $25–30B**——彻底不是矿企规模
- 融资结构：Microsoft GPU $3.6B 融资 @~6% + 预付款 → 覆盖 ~96% GPU CapEx；其他客户新增 $2.8B（Mackenzie $2.4B @9%）→ ~90%；最近客户预付款覆盖 GPU CapEx **45–55%**；6 月底现金 $5.90B + restricted $1.72B，长期债务 **$7.42B** [11]

## 8. 规模速记（Microsoft 200MW 项目）

**一句话总账**：Microsoft 花 **$9.7B**，向 IREN 长租约 **1,056 个 GB300 NVL72 机柜**（管理层口径：4 批 × 每批 ~19,000 张 GB300 [4][18]），平均约 5 年，2026 年分批交付 ≈ **1.1–1.5 ZFLOPS FP4 算力 ≈ 150MW GPU 计算柜 + ~50MW 配套 = 200MW critical IT**。

| 指标 | 单柜（GB300 NVL72） | 1,056 柜合计 |
|---|---:|---:|
| GPU | 72 × B300（Blackwell Ultra） | **76,032 × B300** |
| FP4 Tensor（稀疏） | 1,440 PFLOPS | **≈1.52 ZFLOPS** |
| FP4（无稀疏） | 1,080 PFLOPS | **≈1.14 ZFLOPS** |
| FP8/FP6 | 720 PFLOPS | **≈0.76 ZFLOPS** |
| FP16/BF16 | 360 PFLOPS | **≈0.38 ZFLOPS** |
| 功耗 | ≤142kW [9] | ≈150MW（+ ~50MW InfiniBand/以太网、存储、管理 = 200MW IT） |

规格来源：NVIDIA 官方 [8][9]；机柜数 = 76,032 ÷ 72 反推。

[1]: https://www.sec.gov/Archives/edgar/data/1878848/000187884826000015/iren-20251231.htm "IREN 10-K（四 tranche、Dell $5.8B、200MW critical IT、Childress 750MW）"
[2]: https://www.sec.gov/Archives/edgar/data/1878848/000187884826000026/iren-20260331.htm "IREN 10-Q FY26Q3（15 万 GPU、2027 项目构成、园区储备、5GW secured power）"
[3]: https://www.sec.gov/Archives/edgar/data/1878848/000114036125037386/ny20053824x4_ars.pdf "IREN FY25 10-K（收入 $511M、97% 来自三个矿池）"
[4]: https://ziven.io/earnings/calls/iren/q1-fy2026 "IREN Q1 FY2026 电话会（76,000 GB300、每批 19,000）"
[5]: https://irisenergy.gcs-web.com/news-releases/news-release-details/iren-delivers-horizon-1-microsoft-and-achieves-nvidia-exemplar "IREN 交付 Horizon 1 给 Microsoft（2026-08，NVIDIA Exemplar Cloud）"
[6]: https://www.sec.gov/Archives/edgar/data/1878848/000114036125040072/ef20058139_ex99-2.htm "IREN Microsoft 项目投资者材料（$14–16M/MW 三分拆、$5.8B GPU CapEx 边界、85% margin 口径、300MW gross 标注）"
[7]: https://www.sec.gov/Archives/edgar/data/1878848/000187884826000028/irentranscript.htm "IREN 2026-05 业绩会（Horizon 1–4 "300MW liquid-cooled" = gross 口径）"
[8]: https://www.nvidia.com/en-us/data-center/gb300-nvl72/ "NVIDIA GB300 NVL72 规格（72×B300、FP4 1,440/FP8 720/FP16 360 PFLOPS/柜）"
[9]: https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html "NVIDIA NVL72 AI Factory 文档（单柜最高 ~142kW）"
[10]: https://earningsapi.io/transcripts/iren-limited_iren_earnings_call_transcript_2026-08-27 "IREN FY26 电话会（2026-08-27：矿机年底退出、$638.8M 减值、300/800MW IT 口径、3 年价 +125%、>$20M/MW、FY27 CapEx $25–30B）"
[11]: https://irisenergy.gcs-web.com/news-releases/news-release-details/iren-reports-fy26-results "IREN FY26 Results（AI Cloud Q4 $70.5M/87% 直接毛利、ARR 轨迹、融资结构、现金 $5.9B、债务 $7.42B）"
[12]: https://www.sec.gov/Archives/edgar/data/1878848/000187884826000025/irenreportsq3fy26results.htm "IREN Q3 FY26 Results（480MW/1,210MW 原始口径——后被 FY26 电话会修正为 gross）"
[13]: https://www.madrona.com/the-infrastructure-of-intelligence-inside-crusoes-ai-factory-in-texas/ "Madrona×Crusoe（2026-02：Tier IV 数据中心 $10–15M/MW vs 比特币矿场被动风冷 ~$0.2M/MW，CapEx 差 98–99%）"
[14]: https://www.miners1688.com/immersion-cooling-roi-for-bitcoin-miners-in-2026/ "Miners1688（2026-01：风冷矿场基础设施 $180k–450k/MW；⚠️ 行业博客口径，非一手披露）"
[15]: https://irisenergy.gcs-web.com/news-releases/news-release-details/iren-reports-q3-fy25-results/ "IREN Q3 FY25（2025-05-14：50 EH/s 目标、15 J/TH、3.3¢/kWh Childress 电价、$588M illustrative Adj EBITDA）"
[16]: https://www.investiment.io/symbols/IREN/earnings/transcripts/2026/1 "IREN Q1 FY2026 电话会（$130/kW/月 internal colocation charge、arm's-length、逐年上调）"
[17]: https://coreweave.com/pricing "CoreWeave 公开定价（GB200 NVL72 on-demand $10.50/GPU·h = $756/柜·h；GB300 仅 Contact Sales）"
[18]: https://www.sec.gov/Archives/edgar/data/1878848/000187884825000081/iren-20250930.htm "IREN 10-Q Q1 FY26（2025-09-30：Microsoft 合同 4 批、200MW critical IT、2026 分批交付）"
