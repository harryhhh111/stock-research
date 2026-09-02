# Bitdeer（BTDR / 比特小鹿）：矿企、ASIC 制造商到 AI 托管的早期转型样本

> 整理/核对日期：2026-08-29；数据截止：2026-08-10 财报与 2026-08-04 Tydal 合同披露。
> 研究定位：与 `IREN.md`、`HIVE.md` 对照。BTDR 的核心不是纯粹的“有电矿场”，而是 **自有电力/矿场 + 自研 SEALMINER ASIC + 自营挖矿 + 正在起步的 AI Cloud 与 AI 托管（colo）** 的垂直一体化平台。

**一句话结论**：比特小鹿有接近 **3.0GW** 的全球电力容量，但截至 2026 年 Q2 仍是一家以比特币挖矿为绝对主体的公司；真正将矿场电力转成长期 AI 收入的首个大规模验证，是挪威 Tydal 的 **121 IT MW、16 年、约 $4.7B** 托管合同。不能把“3.0GW global electrical capacity”直接当作“3.0GW 可出租 AI 数据中心容量”。

## 1. FERC、RTO 与 ISO：为什么它们影响美国数据中心接电

- **FERC**（Federal Energy Regulatory Commission，联邦能源监管委员会）：美国联邦独立监管机构，主要管跨州输电、批发电力市场和输电费率。大型数据中心若接到输电网、影响区域可靠性，相关规则可能来自 FERC 批准的 tariff；但零售电价、配电接入、选址许可等大量事项仍由州 PUC（公共事业委员会）及当地 utility 管。
- **RTO / ISO**：不以营利为目的的区域电网调度和市场运营者。它们通常不拥有大部分电线，却负责电网实时调度、输电规划、可靠性研究和批发市场。RTO（Regional Transmission Organization）与 ISO（Independent System Operator）功能相近，名称主要反映历史与监管结构差异。
- 本文前述的“六大 RTO/ISO”是 FERC 在 2026 年大负荷规则行动中涉及的六个区域：**PJM、MISO、SPP、CAISO、ISO New England、NYISO**；这不是美国全部电网。**ERCOT（得州大部）**因基本不跨州，主要受得州 PUCT/ ERCOT 规则管理；东南部许多地区则由垂直一体化 utility 或 TVA 主导。

对 BTDR 尤其重要：Rockdale, Texas 处在 ERCOT 语境；Ohio 项目则处于 PJM 市场区域。相同的“已签 MW”在不同区域，可能面对不同的大负荷研究、网络升级、容量与限电规则。FERC 正在推动区域运营商完善大负荷接入和成本分摊机制，规则尚在变化中 [5]。

## 2. 公司与商业模式

- **主体**：Bitdeer Technologies Group，Cayman 注册、总部在新加坡，NASDAQ: **BTDR**；创始人、董事长兼 CEO 为吴忌寒（Jihan Wu）。吴忌寒此前共同创立比特大陆，2021 年后不再担任其管理职务 [1]。
- **电力/机房层**：取得土地、变电和接电容量，建设并运营矿场/数据中心。
- **硬件层**：自研和制造 SEALMINER ASIC；既销售，也更多用于自己的 self-mining 与 co-mining。
- **挖矿层**：自营挖矿、第三方机房 co-mining、云算力和客户托管。
- **AI 层**：小规模 GPU Cloud（H100/H200/B200/GB200/GB300）和把矿场改造成 AI/HPC colocation。AI 的商业模式仍在从“卖 GPU 算力”向“出租数据中心、电费 pass-through”扩展。

这使 BTDR 与 IREN/HIVE 有一个重要差别：它拥有 ASIC 研发制造能力，因此即使转做 AI，仍有很强的矿业设备资产与产能配置选择权；同时也意味着资本开支、存货/固定资产和挖矿周期风险更重。

## 3. 当前经营：矿业仍是收入主体（Q2 2026）

| 指标 | 数值 | 口径/判读 |
|---|---:|---|
| 总收入 | **$228.8M** | Q2 2026 |
| 自营挖矿收入 | **$168.4M** | 占总收入 **73.6%** |
| Co-mining 收入 | **$25.0M** | 与自营合计 **84.5%** |
| AI Cloud 收入 | **$14.0M** | 占总收入 **6.1%**；不是 $76M ARR |
| AI Cloud 部署 GPU / 利用率 | 4,248 / 95% | 2026-06 月末运营指标 |
| AI Cloud ARR | **约 $76M** | 日合同收入 ×365 的年化 run-rate，不能与当季 GAAP 收入混用 |
| 自营算力 / co-mining 算力 | 73.0 / 15.9 EH/s | 2026-06 月末 |
| 平均矿机效率 / 电价 | 15.8 J/TH / **$44/MWh** | Q2 2026；后者是全球矿业实际平均值，不能直接等同未来 AI 电价 |

公司 Q2 总毛利为 **-$8.5M**、净亏损 **-$92.3M**；AI Cloud 自身收入 $14.0M、成本 $16.3M、毛利约 **-$2.3M**。所以“AI ARR 增长”是早期运营信号，不等于已经验证 AI 业务具备成熟盈利能力 [2]。

## 4. 电力资产：容量很大，但成熟度和用途差异极大

公司在 2026-08 财报口径列示 **1,752MW online + 1,228MW pipeline = 2,980MW** 总全球电力容量。该数字混合了已通电矿场、仅有 utility 合同的项目、租赁容量、建设中容量和拟转 AI 容量。

| 与 AI 转型最相关的场地 | 公司披露容量 | 当前状态（截至 2026-08） | 研究上的正确理解 |
|---|---:|---|---|
| Tydal, Norway | 180MW gross（其中合同 121 IT MW） | 66.5MW + 66.5MW 分别目标 Q4’26/Q1’27；另 47MW H2’27 | 已有大合同，最强证据 |
| Rockdale, Texas | 563MW online + 179MW planning | 评估由 crypto 转 colo/AI | 大容量但尚非 AI 合同容量 |
| Knoxville, Tennessee | 86MW | 矿场改 AI，整体目标 Q3’27 | 项目设计被重做、进度后移 |
| Wenatchee, Washington | 13MW | 已拆矿场、提交设计与建造许可 | AI 设计仍在调整 |
| Molde, Norway | 84MW online | 早期评估能否转 AI | 尚非已承诺 AI 容量 |
| Massillon, Ohio | 174MW online | crypto | 有已建负荷，但非 AI 转化承诺 |
| Clarington, Ohio | 570MW utility contract | colo/crypto，投产日待定 | 受邻近公司诉讼等影响，不能按已交付容量估值 |
| Weathersfield, Ohio | 300MW | 目标 Q4’28，colo/AI | 已有接网开发场地及本地 utility 线路延伸协议，但仍是远期项目 |

因此，应把公司 MW 至少分为四类：**已可供矿业负荷、已具备 AI 机房条件、已签 AI 客户合同、以及仅处于电力/开发储备**。这四类不能相加后以同一 $/MW 估值。

## 5. Tydal：矿场电力变成 AI 基础设施收入的关键验证

2026-08，Bitdeer 子公司与 Volta 子公司签订 Tydal AI/HPC 数据中心的 **16 年 colocation lease and services agreement**：

| 项目 | 披露值 |
|---|---:|
| 面向客户的 IT 负荷 | **121 IT MW** |
| 支撑该负荷的机房 gross power | 约 **133MW** |
| 初始合同期 / 合同收入 | **16 年 / 约 $4.7B** |
| 可选续约 | 一次 8 年；潜在 TCV 约 $8.0B |
| 平均租金 | 约 **$202/kW/月** |
| 隐含年化机房收入 | 约 **$294M/年**（$4.7B ÷16；与 $202×121,000kW×12 基本一致） |
| 电费 | 租户 pass-through reimbursement，不应把该部分当 BTDR 的固定毛利 |
| 保障 | 预计约 $1.3B 信用证支持，仍受惯常条件约束 |

**判读**：Tydal 是“土地/已接电能力 → 高密度 AI colo 长约”的实质性验证，且单位 IT MW 隐含约 **$2.43M/MW/年** 的机房合同收入。不过，它是机房及服务租约，不包含 Bitdeer 自己采购、持有并出租 GPU 的收入模型；与 IREN 的 GPU Cloud 一体化合同不可直接比较 [3]。

## 6. 对“美国电网接入”研究的含义

1. **Rockdale 和 Ohio 的 MW 最值得逐个核实接入权**：需要查的是 interconnection/service agreement、变电站/输电路径、所需网络升级及 firm service 条件，而非只看公司称“online”或“under contract”的容量。
2. **矿场已有接电不代表 AI-ready**：AI 机房需高密度配电、UPS/柴油备电、液冷、光纤及更高可靠性。Knoxville 的整体 redesign、Wenatchee 拆矿场后仍在许可阶段，都证明转换并非“把 ASIC 换成 GPU”。
3. **MW 口径必须分 IT 与 gross**：Tydal 121 IT MW 由约 133 gross MW 支撑，PUE 约 1.1；矿场、园区和变电站 MW 若混用，会高估可售 AI IT 容量。
4. **市场/监管不确定性可影响日期和成本**：FERC 正在要求 PJM、MISO、SPP、CAISO、ISO-NE、NYISO 改进大负荷规则；ERCOT 也有其单独的大负荷流程。因此，未来美国项目尤其是 Ohio/Texas 的增容，不能仅按公司时间表视作确定性现金流 [5][6]。

## 7. 投资观察清单与主要风险

- **最重要的转化率指标**：AI 合同覆盖的 IT MW / 公司总 MW，而不是总 MW 本身。
- **客户与信用**：Tydal 的最终终端客户未在披露中具名；信用证安排仍有条件，需跟踪正式生效、交付和起租。
- **融资压力**：截至 2026-06-30，现金、现金等价物及受限现金 $496.3M，借款 **$1.8B**；Q2 经营现金流为 -$158.5M，投资现金流中的 CapEx 为 $266.0M。AI 转型需要持续融资与工程交付能力 [2]。
- **矿业周期仍主导近端业绩**：Q2 约 84.5% 收入来自自营挖矿与 co-mining，币价、难度、ASIC 折旧和电价仍比 AI 业务更能左右报表。
- **容量不是收入**：Clarington 570MW 的供电时点待定，Weathersfield 300MW 要到目标 Q4’28；它们应分别按开发阶段和接网风险折价。

## 8. 与 IREN、HIVE 的位置对比

| 公司 | 当前主线 | AI 转型证据 | 最容易犯的误读 |
|---|---|---|---|
| IREN | 自持电力/机房 + 大规模 GPU Cloud | Microsoft/NVIDIA 等大规模合同 | 忽略 GPU 与机房的巨额 CapEx |
| HIVE | 挖矿为现金流，部分 AI 租赁/改造 | Bell/Cohere 合同、加拿大/瑞典改造 | 把租 Bell 机房误认为自有矿场已转 AI |
| **BTDR** | **ASIC 制造 + 自营矿业 + 早期 AI colo/Cloud** | **Tydal 121 IT MW、16 年 $4.7B 合同** | **把近 3GW 电力储备当作已签/AI-ready 的收入容量** |

## 来源

[1] [Bitdeer 2025 Form 20-F（公司、管理层与吴忌寒履历）](https://www.sec.gov/Archives/edgar/data/1899123/000121390026049770/ea0282628-20f_bitdeer.htm)

[2] [Bitdeer Q2 2026 业绩，SEC 6-K 附件](https://www.sec.gov/Archives/edgar/data/1899123/000121390026086938/ea030131301ex99-1.htm)

[3] [Tydal：$4.7B、16 年 AI/HPC colo 合同，SEC 6-K 附件](https://www.sec.gov/Archives/edgar/data/1899123/000121390026085655/ea030075201ex99-1.htm)

[4] [Bitdeer 2026-06 运营更新（GPU、ARR 与项目早期状态）](https://ir.bitdeer.com/news-releases/news-release-details/bitdeer-announces-june-2026-production-and-operations-update)

[5] [FERC：大负荷接入改革行动，2026-06-18](https://www.ferc.gov/news-events/news/ferc-launches-aggressive-targeted-action-speed-large-load-integration)

[6] [ERCOT：Large Load Integration](https://www.ercot.com/services/rq/large-load-integration)
