# 三星电子 Memory：FY2026H1 数据与 HBM–Foundry 协同

> 整理日期：2026-09-16  
> 财务数据截止：2026-06-30（2026Q2）。三星财年与自然年一致，FY2026 尚未结束；截至本文件日期，Q3 和全年数据均未披露。  
> 金额单位：万亿韩元（KRW T）。除特别说明外为三星官方季度业绩材料中的口径。

## 先给结论

此前项目启动页把“Memory 销售额没有单列”写得过宽，这是不准确的，现已更正。三星在季度业绩材料中披露 Memory 销售额：FY2025 全年可由四季相加复算为 **104.1**；FY2026 Q1、Q2 分别为 **74.8**、**120.8**，上半年合计 **195.6**，同比 **+385%**。

但这不是“内存业务已经完整可建模”——公司仍未单列 Memory 营业利润，也未披露 DRAM 与 NAND 各自销售额、ASP、bit 出货、HBM 收入或客户。Q2 DS 营业利润 **89.2** 不能直接赋给 Memory；DS 同时含 Foundry、System LSI，且各业务单元销售额包含内部交易。

FY2026 的正确表述是 **“已披露 H1，非完整年度”**。在没有 Q3/Q4 数据和公司全年指引时，将 H1 或 Q2 年化为 FY2026 正常利润，会把存储器价格、产品组合和资本开支周期误当作稳态。

## 1. 数据可得性与口径

| 项目 | 是否已披露 | 本研究如何使用 |
|---|---|---|
| Memory 季度销售额 | 是 | 可建立收入时间序列；注意其含内部交易，不能与其他单元简单加总。 |
| DS 季度销售额、营业利润 | 是 | 用于观察半导体分部景气与盈利杠杆；不等于 Memory 利润。 |
| Memory 营业利润 | 否 | 不用 DS 利润替代；只能标为 ⚠️ 无法复算。 |
| DRAM/NAND 销售额、ASP、bit 出货 | 否 | 后续使用第三方数据时必须另标注来源、日期和估算性质。 |
| HBM 收入、份额、客户合同 | 否 | 产品公告可确认阶段，不能反推收入或绑定客户金额。 |
| FY2026 Q3、FY2026 全年 | 截至 2026-09-16 未披露 | 保持空白；下一次更新读取 Q3 业绩材料。 |

三星的季度材料明确说明：各业务单元销售额包括 intersegment sales（内部交易）。因此，以下“Memory 销售额”是最有用的公开经营指标，但不等同于外部客户收入，也不能与 DS / DX 等业务单元收入机械相加。[2026Q2 业绩材料](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_2Q_conference_eng.pdf)

## 2. FY2025 已审视基准：Memory 进入高景气前的爬坡

| 期间 | Memory 销售额 | QoQ | DS 销售额 | DS 营业利润 | 当期主要经营信息 |
|---|---:|---:|---:|---:|---|
| 2025Q1 | 19.1 | -17% | 25.1 | 1.1 | ASP 下滑、HBM 销售受出口限制等因素拖累公司表述的存储盈利。 |
| 2025Q2 | 21.2 | +11% | 27.9 | 0.4 | 仍为低利润季度；不能仅从收入推断 DRAM/NAND 结构。 |
| 2025Q3 | 26.7 | +26% | 33.1 | 7.0 | HBM3E 销售增长、全应用需求与价格上行改善盈利；公司也提到部分库存估值调整减少。 |
| 2025Q4 | 37.1 | +39% | 44.0 | 16.4 | HBM、服务器 DDR5、企业 SSD 等高附加值产品与行业价格上升共同驱动。 |
| **FY2025（复算）** | **104.1** | — | **130.1** | **24.9** | Memory 销售额占 DS 销售额约 **80.0%**；这不是独立的 Memory 利润率。 |

**复算：**`19.1 + 21.2 + 26.7 + 37.1 = 104.1`；`104.1 ÷ 130.1 = 80.0%`。四舍五入可能造成 0.1 的尾差。来源：[2025Q1](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_1Q_conference_eng.pdf)、[2025Q3](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_3Q_conference_eng.pdf)、[2025Q4](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_4Q_conference_eng.pdf)。

这一序列说明 FY2025 已在 Q4 出现明显加速，但它本身也说明周期风险：季度销售额从 Q1 的 19.1 到 Q4 的 37.1，变动幅度很大。把 Q4 × 4 当作正常化收入，同样不合适。

## 3. FY2026H1：已披露数据，不是全年预测

| 期间 | Memory 销售额 | QoQ | YoY | DS 销售额 | DS 营业利润 | Memory/DS 销售额 | 公司给出的主要驱动 |
|---|---:|---:|---:|---:|---:|---:|---|
| 2026Q1 | 74.8 | +102% | +292% | 81.7 | 53.7 | 91.6% | 有限供给下满足高附加值 AI 需求；行业价格上升；开始销售 HBM4 和 SOCAMM2。 |
| 2026Q2 | 120.8 | +62% | +471% | 127.5 | 89.2 | 94.7% | 服务器优先、DRAM 与 NAND bit 销量均创新高、价格继续上行、扩大 HBM4 销售。 |
| **2026H1（复算）** | **195.6** | — | **+385%** | **209.2** | **142.9** | **93.5%** | 高端 DRAM/HBM/eSSD 组合、供给约束和价格共同作用。 |

**复算：**

- Memory H1：`74.8 + 120.8 = 195.6`；去年同期 `19.1 + 21.2 = 40.3`，故同比 `(195.6 ÷ 40.3 - 1) = 385.4%`。
- Q2 环比：`120.8 ÷ 74.8 - 1 = 61.5%`；Q2 同比：`120.8 ÷ 21.2 - 1 = 469.8%`。与三星展示的 +62% / +471% 为四舍五入差异。
- DS H1：销售额 `81.7 + 127.5 = 209.2`，营业利润 `53.7 + 89.2 = 142.9`；**这不是 Memory H1 营业利润**。

数据来源：[2026Q1 业绩材料](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_1Q_conference_eng.pdf)、[2026Q2 业绩材料](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_2Q_conference_eng.pdf)。

### 需要避免的两个误读

1. **“195.6 是 FY2026 的收入”——错误。**它只覆盖前六个月；Q3/Q4 的价格、bit、手机/PC 需求、客户认证和扩产节奏尚未知。
2. **“DS 142.9 是 Memory H1 利润”——错误。**它包含 Foundry 与 System LSI 的利润/亏损，也可能包含内部交易影响；只能把它视为 DS 整体高景气的上限式背景数据。

## 4. DRAM、NAND 与产品组合：已知和未知要分开

### 已知（公司披露）

- Q2 的 DRAM 与 NAND **bit 销量均创历史新高**；公司没有给出两者的绝对 bit 数、价格或收入拆分。
- DRAM 端：Q1 开始销售 HBM4、SOCAMM2；Q2 继续扩大 HBM4 销售，服务器收入组合占比创新高；HBM4E 已向主要客户送样。
- NAND 端：公司在 H1 推进 PCIe Gen6 eSSD 与 UFS 5.0；PM1763（基于 V9 NAND）在 7 月宣布量产，故该产品的量产公告发生在 H1 结束后。
- 公司对 H2 的表述是服务器 DRAM、企业 SSD 与 HBM 需求加速，供给即使增产仍可能偏紧；这是管理层前瞻判断，不是已实现收入。

来源：[2026Q2 业绩材料](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_2Q_conference_eng.pdf)、[HBM4E 公告](https://news.samsung.com/global/samsung-electronics-begins-shipment-of-industry-first-hbm4e-samples)、[PM1763 公告](https://news.samsung.com/global/samsung-begins-mass-production-of-pm1763-ssd-optimized-for-next-generation-ai-infrastructure)。

### 仍未知（不可由现有材料倒推）

| 需要的指标 | 为什么不能从 120.8 直接推出 | 后续解决方式 |
|---|---|---|
| DRAM vs. NAND 销售额 | 二者价格、bit 增长和产品形态不同，且公司未拆分 | 以公司后续披露为主；第三方数据须单独标记。 |
| HBM 收入/毛利 | HBM 属于 DRAM 销售额的一部分，且无收入单列 | 只以“样品→认证→量产→商业出货”的状态跟踪。 |
| ASP 与 bit 增长各贡献多少 | 仅有总销售额和“bit 创新高”的定性披露 | 构建行业价格与供给底表后再估计，不能现在反推。 |
| eSSD 对 NAND 盈利的增量 | 产品量产或认证不披露客户数量、价格和销量 | 追踪客户平台、容量组合、PCIe 代际和公司季度表述。 |

### 4.1 三星的 HBM 份额为何上升：是“先进 DRAM 重新配置 + 首发产品/价格”，不是总 DRAM 产能的简单映射

先校正“份额很高”的表述：据 Counterpoint 数据，三星 **2026Q2 HBM 收入份额为 33%**，从 Q1 的 21% 大幅上升，但仍低于 SK 海力士的 **50%**；这不是 HBM bit 份额、DRAM wafer 份额，也不是 HBM 产线份额。[Seoul Economic Daily 对 Counterpoint 数据的报道，2026-09-03](https://en.sedaily.com/finance/2026/09/03/samsung-doubles-hbm-market-share-to-33-percent-narrowing)

| 因素 | 对三星 HBM 收入份额的作用 | 与普通 DRAM 的关系 |
|---|---|---|
| HBM4 首批商业出货 | 三星 2026-02 已开始 HBM4 量产和商业发货；Q2 首次形成显著收入，故高单价 HBM4 可迅速抬高**收入**份额。 | 不是新增一倍 wafer；是把已有/新增的先进 1c DRAM、base die 和封装能力组合成高价产品。 |
| 先进 DRAM 产品组合再配置 | 公司明确称，为应对 AI 需求，DRAM 产品组合将更多聚焦 HBM 与服务器 DDR；并为 HBM3E、HBM4/4E 扩供及提前投资 1c-nano。 | **是，方向上存在从通用 DRAM 向 HBM/服务器 DRAM 的资源倾斜。**但公司未披露从 DDR5/LPDDR 等产品切走了多少 WPM，不能量化为“X 万片/月转换”。 |
| 大 DRAM 基数与垂直整合 | 大规模 DRAM 制造基础、稳定的 1c 良率、内部 4nm base die 和先进封装，能缩短 HBM 的供货与迭代路径。 | 总 DRAM 基数是必要条件，但并非充分条件；HBM 还受 TSV 堆叠、封测、base die、热管理和客户认证约束。 |
| HBM 的资源消耗和单价 | HBM4 的单栈价值很高，因此较少的出货量即可显著影响收入份额。 | 行业可比口径中，同工艺节点下，HBM3E 生产同等 bit 约耗用 DDR5 的 **3 倍 wafer 资源**；HBM4 的 trade ratio 可能更高。因而 HBM 扩张会压缩可供普通 DRAM 的有效资源。 |

可以用下面的逻辑理解，而不能把“33% HBM 收入份额”理解成“33% DRAM 产能被转成 HBM”：

`先进 DRAM wafer / die → TSV 与堆叠封装 → HBM stack → 客户认证及 GPU/ASIC 平台 → 高 ASP HBM 收入`

其中第一步确实会与 DDR5、LPDDR 等竞争先进 DRAM wafer；但后面三步同样可能成为瓶颈。因此，即使三星总 DRAM wafer 基数大，也不保证 HBM 份额第一。Q2 仍由 SK 海力士以 50% HBM 收入份额领先，正说明客户资格、HBM3E 存量、封装能力和产品代际节奏也决定份额。

**当前最稳妥的结论：**

- **✅** 三星正在把先进 DRAM/产品组合更多投向 HBM 与服务器 DRAM，并扩大 HBM4 供给；这会挤占一部分本可用于通用 DRAM 的资源。
- **✅** Q2 HBM 收入份额的跃升还明显受 HBM4 首发商业出货和高 ASP 影响，不能只归因于产能切换。
- **⚠️** 三星未披露 HBM 占用的 wafer starts、HBM bit 份额、封装产能或由普通 DRAM 转入 HBM 的 WPM，故不能把行业的 3:1 经验比例套算成三星的绝对产能。

三星确认 HBM4 使用 1c DRAM 和 4nm 逻辑 base die，并于 2026-02 开始商业出货；公司还预计 2026 年 HBM 销售同比超过三倍。[三星 HBM4 公告](https://news.samsungsemiconductor.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing/) 公司在 FY2025Q4 电话会上确认，会为 HBM3E 扩供、提前投资 1c-nano 以支持 HBM4/4E，同时维持 HBM 与服务器 DDR 的平衡，而非无限制偏向单一产品。[三星 FY2025Q4 电话会记录](https://irsvc.teletogether.com/sec/pdf/2025Q4_script_eng.pdf?1=) 3:1 为 Micron 提供的行业可比口径，应用于三星时只作方向性参照。[Micron FY2026Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)

## 5. Foundry 为什么要纳入，但不能和 Memory 混为一谈

Foundry 不是 DRAM 或 NAND 业务的一部分，却是三星 HBM 竞争力的一项**必要协同环节**。最具体的交点是 HBM 的逻辑底座（base die / B-die）：三星的披露显示，Foundry 在 2025Q4 开始出货 4nm HBM base die，2026Q2 又将 HBM B-die 需求列为 Foundry 收入增长驱动，并计划扩大 4nm base-die 销售。

| 环节 | 主体 | 对 HBM 的含义 | 研究边界 |
|---|---|---|---|
| DRAM core die 与 HBM 堆叠 | Memory | 决定 HBM 容量、带宽、良率与可供货量 | 第一阶段核心。 |
| 逻辑底座（base die） | Foundry（可内部供给） | 决定接口、控制、功耗以及与客户平台协同；HBM4E 使用 4nm base die 的产品路线。 | 纳入 HBM 供应链、成本、良率与交付追踪；不做 Foundry 独立估值。 |
| 先进封装与集成 | 三星的存储/代工/封装协同 | 影响堆叠、散热、测试和客户认证。 | 追踪技术和产能瓶颈；不把“全栈”宣传直接等同于可持续利润。 |
| 外部客户代工、2nm、System LSI | Foundry/System LSI | 与 Memory 存在资本、工程与客户资源竞争，也可能带来协同。 | 只在影响 HBM base die 的供给/成本或 DS 资本分配时记录。 |

三星的“logic + memory + advanced packaging integration”是战略能力描述，不是量化利润分部。当前应判定为：**✅ HBM base die 是 Foundry 与 Memory 的真实经营交点；⚠️ 该协同为三星带来的 HBM 成本、毛利或客户黏性增量尚无法复算。** [2025Q4 业绩材料](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_4Q_conference_eng.pdf) [2026Q2 业绩材料](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_2Q_conference_eng.pdf) [HBM4E 公告](https://news.samsung.com/global/samsung-electronics-begins-shipment-of-industry-first-hbm4e-samples)

## 6. 资本开支：需要按 DS 观察，不能假装有 Memory 单独 CapEx

| 期间 | 公司总 CapEx | DS CapEx | 可用结论 |
|---|---:|---:|---|
| FY2025 | 52.7 | 47.5 | DS 的先进工艺迁移、产线升级等投入占集团绝大多数；其中同时含 Memory、Foundry 与 System LSI。 |
| 2026Q1 | 11.2 | 10.2 | 公司称 DS 投资聚焦先进节点/工艺的产能扩充与迁移；无 Memory 单独金额。 |
| 2026H1 | 28.0 | 25.6 | 公司半年报的精确值为 27.9864 / 25.6030；继续包含 Memory、Foundry 与 System LSI，不能视作 HBM 或 Memory 单独 CapEx。 |

FY2025 公司表述，Memory 资本开支着重于先进工艺迁移，以支持 HBM、高密度 DDR5 等高价值产品；Foundry 则因以产线转换为主而实行较保守投资。这能说明资本优先级，不足以分别计算两业务的投资回报率。H1 的逐季拆分、资本等值和 2027 产能口径见 [资本开支与产能.md](资本开支与产能.md)。[FY2025 CapEx 公告](https://www.samsung.com/global/ir/reports-disclosures/public-disclosure-view.84547/) [2026 年股东大会材料](https://www.rns-pdf.londonstockexchange.com/rns/9325S_1-2026-2-13.pdf) [2026H1 interim report](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_Half_Interim_Report.pdf)

## 7. 下一次财报的核对清单

| 事件/指标 | 为什么重要 | 什么会削弱当前逻辑 |
|---|---|---|
| 2026Q3 Memory 销售额及环比变化 | 验证 H1 的高收入是否延续 | 收入增速显著放缓且无合理的产品/价格解释。 |
| DRAM/NAND bit、ASP 的任何定量/定性更新 | 区分价格上涨与出货增长 | 只有价格拉动、bit 或服务器组合转弱。 |
| HBM4 放量与 HBM4E 客户认证 | 验证产品状态从送样走向商业规模 | 送样延期、良率/散热问题或客户平台延后。 |
| PCIe Gen6 eSSD / PM1763 客户导入 | 验证 NAND 的高附加值出口 | 仅有产品发布，无订单、认证或产品组合改善迹象。 |
| DS CapEx、Memory/Foundry 产能表述 | 判断未来供给、折旧与内部资源配置 | 高点扩产、库存上升或低效资本投入。 |
| Foundry 4nm base-die 进展 | 验证 HBM 协同是否成为交付优势 | base-die 受限、外部采购、成本恶化或影响 HBM 排产。 |

## 主要来源

1. [三星 2026Q2 Earnings Call 材料](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_2Q_conference_eng.pdf)
2. [三星 2026Q1 Earnings Call 材料](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_1Q_conference_eng.pdf)
3. [三星 2025Q1 Earnings Presentation](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_1Q_conference_eng.pdf)
4. [三星 2025Q3 Earnings Presentation](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_3Q_conference_eng.pdf)
5. [三星 2025Q4 Earnings Presentation](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_4Q_conference_eng.pdf)
6. [三星 FY2025 CapEx 公告](https://www.samsung.com/global/ir/reports-disclosures/public-disclosure-view.84547/)
