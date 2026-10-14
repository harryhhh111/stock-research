# Siemens Energy（Xetra: ENR）研究

> 初稿整理：2026-09-17 ｜财务数据截至：FY2026 Q3（截至 2026-06-30，2026-08-05 披露）｜数据中心订单与项目进度截至：2026-09-17
>
> 研究目的：核验 Siemens Energy 在 AI 数据中心电力链上的两条路径——**电网接入侧的变压器/开关设备/变电站**，以及**表后或电网侧的燃机、汽轮机与发电厂**。订单、reservation、设备出货和园区 Active IT 必须逐层区分。

## 结论先行

1. **Siemens Energy 是目前最完整的 P0 交叉验证标的。** Grid Technologies（GT）覆盖大型变压器、高压开关设备、变电站与 HVDC；Gas Services（GS）覆盖重型燃机、航改燃机、大型汽轮机和发电机。它既可能供给 utility 的接电工程，也可能为数据中心提供表后发电。[2025 年报][1]
2. **公司披露的“22GW data-center-related commitments”不能用作 22GW 上线或出货。** FY2026 Q1，GS 披露当季 13GW 已 booked、80GW total commitments，其中 22GW 与数据中心有关；公司未按项目披露 22GW 的客户、国家、设备型号、合同成熟度与交付/投运日期。正确处理是“燃机需求线索”，而非 2027 电力供给。[Q1 分析师材料][2]
3. **订单确实在转化为可追踪的设备业务，但对 2027 仍缺园区级落点。** GS 在 FY2026 Q3 的订单为 €9.967bn、backlog €73bn；GT 订单 €5.367bn、backlog €51bn，后者主要由变压器产品和美国需求带动。两项均说明供给瓶颈与定价能力强，却没有公开按数据中心拆分的 MVA/GW 与 SAT 日期。[Q3 业绩材料][3]
4. **公开可定位的 B&W 订单也不支持 2027。** 2026-08，B&W 与 Siemens Energy 启动 20 台 SST-300 汽轮发电机组、合计 1GW、服务其 FastPower 数据中心项目；客户、地点、商业运行日期均未披露。此前 B&W/Applied Digital 相关项目的公开目标为 2028 年底供电。因此均暂记为“表后发电候选”，2027 Active IT 为 **0GW（待核）**。[B&W 1GW 公告][4] [B&W/Applied Digital][5]
5. **产能扩张是供给侧佐证，不是新增 GW 的计量器。** 公司 2026 年宣布在美国投入 $1bn，扩张大型变压器生产/维修和大型燃机制造，并在 Mississippi 新建高压开关设备工厂；但未公布对应年产 MVA、燃机 GW、满产时点或数据中心专属份额，故不能以产能投资反推 2027 上线量。[美国投资公告][6]

---

## 1. 公司在电力链中的位置

```text
utility / 园区开发商的负荷与供电方案
                   ↓
  A. 电网接入：主变、GIS/AIS、变电站、HVDC、保护控制（GT）
                   ↓
          utility / 输电网 energize
                   ↓
  B. 供电补充：燃机、汽轮机、发电机、控制系统、长期服务（GS）
                   ↓
      园区机电 commissioning → IT 机柜上架 → Active IT
```

| 业务 | 与数据中心相关的产品 | 能提供的证据 | 不能单独证明的事项 |
|---|---|---|---|
| **Grid Technologies** | 大型电力变压器、GIS/高压开关、变电站、HVDC、FACTS、数字化电网 | utility/EPC 的采购、设备 MVA、电压等级、出厂/到场/SAT | 该园区实际运行的 IT MW |
| **Gas Services** | 重型燃机、航改燃机、汽轮机、发电机、控制与长期服务 | 表后/电网侧发电项目的机组数量、名义 MW、商业运行日 | 项目发电量是否全供数据中心、IT 的实际负荷 |
| Transformation of Industry | 工业汽轮机、压缩机、电气化等 | 个别工业/能源项目 | 不是本研究的主要数据中心接电设备；公司正筹备分拆该业务 |
| Siemens Gamesa | 风机和服务 | 远期清洁电源配套 | 不构成数据中心短期 firm power 或接电证据 |

FY2025 年报明确把 data-center operators 列为 GT 的客户类型，也把数据中心列为 GS 典型的大型、可调度基荷需求行业之一。这个“覆盖全链条”是其研究价值所在；但两项描述均是公司组合能力，而非项目级订单披露。[2025 年报][1]

## 2. 订单漏斗：必须拆开 booked、commitment 与已投运

### 2.1 Gas Services 的 22GW 数据中心线索

FY2026 Q1 的公司材料给出以下并列数字：

| 指标 | 数值 | 可作何种证据 | 不可作何种证据 |
|---|---:|---|---|
| 当季 Gas Services 已 booked | **13GW** | 已获订单的燃机容量（但仍未披露完整项目表） | 数据中心专属 GW；当年投运 GW |
| Gas Services total commitments | **80GW** | 客户需求与产能槽位的总线索 | 已签硬订单或可用电力 |
| 其中 data-center-related commitments | **22GW** | 数据中心相关的长期需求压力 | 数据中心已建/在建/2027 上线容量 |

公司没有在这张材料中给出 commitment 的逐项法律定义。可以合理判断它包含不同确定性阶段（例如订单、reservation 或客户意向），但这只是**研究者对“commitment”披露层级的判断**，不应自行将其当作有约束力的全部订单。[Q1 分析师材料][2]

用于台账时的正确链条应为：

```text
22GW data-center-related commitments
  → 能定位项目的合同/机组型号/数量
  → EPC、许可、燃气/并网与建设开工
  → 机组交付、并网、商业运行（COD）
  → 数据中心获得可用电 + 机电调试 + Active IT
```

因此目前不能把 22GW 与 NVIDIA 机柜、变压器产能或全球 2027 新增 Active IT 相加。

### 2.2 最新经营数据：强景气，非数据中心容量表

| 口径 | FY2026 Q3 单季 | FY2026 前九个月 | 含义 |
|---|---:|---:|---|
| 集团订单 / backlog | €17.926bn / €162bn | €53.284bn | 订单和在手订单均创新高 |
| 集团收入 / Profit before Special Items | €11.447bn / €1.623bn | €31.416bn / €3.946bn | 财务表现强，但不按数据中心披露 |
| **GS** 订单 / 收入 / P&SI 利润率 | €9.967bn / €3.756bn / **19.9%** | €27.587bn / €10.331bn / 16.6% | 美国大型数据中心相关订单是 Q3 订单驱动之一；GS backlog **€73bn** |
| **GT** 订单 / 收入 / P&SI 利润率 | €5.367bn / €3.624bn / **19.9%** | €18.328bn / €9.744bn / 18.3% | 变压器产品是主要订单驱动，GT backlog **€51bn** |

注：`Profit before Special Items` 为公司使用的调整后指标，不等于 IFRS 净利润；表中 Q3 订单、收入和 segment 口径取公司 FY2026 Q3 材料。GS 和 GT 合计的 backlog 也不能相加后再换算 GW，因为两者可以服务同一座园区的同一条功率流。[Q3 业绩材料][3]

## 3. 可定位的数据中心案例与 2027 判断

| 项目/案例 | 公开事实 | 在模型中的正确位置 | 对 2027 Active IT 的处理 |
|---|---|---|---|
| **B&W FastPower（匿名客户）** | 2026-08 B&W 与 Siemens Energy 启动 20 台 SST-300 汽轮发电机组工作，合计 **1GW**，用于 FastPower 数据中心项目 | 设备已进入较强的前序订单/制造信号；仍无项目地点、客户、锅炉/燃料/并网、COD | **0GW（待核）**：1GW 是发电机组名义容量，不是已上线园区或 IT 负荷。[B&W 1GW 公告][4] |
| **Applied Digital AI Factory** | 2026-01 B&W 选择 Siemens Energy 提供汽轮发电机组，目标为 Applied Digital AI Factory 供应 1GW；当时为 securing turbine sets 的 limited notice to proceed，公开目标在 **2028 年底**供电 | 这是“供应商—EPC—园区”链条较完整的表后发电候选 | **2027：0GW。** 即便设备按计划推进，公开时间表不支持提前计入。[B&W/Applied Digital][5] |
| **Equinix DB5（Dublin）** | 九台 SGT-A05 航改燃机，合计 **45MW**，服务当地调峰和备用电 | 已运行的表后/备用电技术参考案例 | 不属于新增 2027；且备用/调峰 45MW 不等于 45MW Active IT。[Equinix DB5 案例][7] |
| **Morgan Valley Energy Center（Iowa）** | 三台 SGT6-5000F、拟服务大型用户和工业增长；项目仍待监管批准，预计 **2030** 运行 | 电网侧发电供给候选，需求包括但不限于数据中心 | **2027：0GW。** 不应把 Iowa 负荷增长叙事归属单一数据中心。[Morgan Valley][8] |

公司有公开项目和数据中心产品页面，不代表每个机组都可用于 2027 估算。最小可计量单元必须是同一园区下的 `机组可用 MW × 供给分配比例 × 已投运证据`，再与其接电、冷却和已上架 IT 容量取最小值。

## 4. 产品与工程能力：为什么它能成为瓶颈验证方

### 4.1 电网接入侧

Siemens Energy 的数据中心方案明确包含低损耗变压器、SF₆-free 开关设备、输电与 grid-connection 方案。GT 的 Q1/Q2/Q3 表现显示美国订单和变压器产品需求持续强劲；但公司没有披露：

- 北美大型电力变压器年产 MVA；
- 数据中心与一般 utility/新能源/工业客户的 MVA 拆分；
- 从接单到工厂 FAT、现场 SAT 的平均交期；
- 单个数据中心项目的主变数量、规格和客户名称。

这些缺口使 GT 可以用于检验“供给紧张与订单压力”，却不能直接推算全球 2027 新增 GW。[Q1 业绩][9] [Q2 业绩][10]

### 4.2 表后/加速供电侧

公司对 AI 数据中心给出的常见配置范围是 60–250MW 的 AI 专用数据中心可采用灵活联合循环配置；产品页列示的机组级名义功率包括 SGT-A35 约 31–37MW、SGT-800 45–62MW、SGT6-5000F 260MW、SGT6-9000HL 440MW。它们是**型号能力**，不是订单量或实际可送至 IT 的电力。[数据中心方案][11]

Siemens Energy 与 Eaton 的模块化 onsite power 合作宣传称，园区可在外部电网尚不可用时先建设表后发电，并将整体建设进度加快 2–4 年。这是潜在解决方案，不是已披露项目的时间表；真正的约束仍包括燃机产能、许可、天然气管线、锅炉/余热系统、变电站、冗余和调试。[模块化表后发电方案][12]

## 5. 产能、竞争与财务判断

### 5.1 美国扩产

2026-02，公司宣布 $1bn 美国制造投资、计划新增逾 1,500 个岗位：

- North Carolina：扩张大型变压器生产/服务，Charlotte 恢复大型燃机制造，Winston-Salem 增加燃机零部件产能；
- Mississippi：新建高压开关设备工厂，计划最多 300 人；
- Florida、Alabama、New York、Texas：分别补足燃机叶片/导叶、发电机零件、压缩设备等环节。

这会改善 2027 之后的设备供给弹性；但公告没有给出新产线的 MVA/GW、SOP、利用率或数据中心份额。因此本研究把它标记为**中长期供给侧正面证据**，而不是 2027 的可计量供给。[美国投资公告][6]

### 5.2 竞争格局与公司风险

| 维度 | Siemens Energy 的位置 | 研究应观察的风险 |
|---|---|---|
| 大型燃机 | 与 GE Vernova、Mitsubishi Heavy 等竞争；GS backlog 高、美国数据中心需求已进入订单驱动 | reservation 向硬订单/交付的转化，燃机 slot、项目许可、燃气与输电是否同步 |
| 大型主变/电网设备 | 与 Hitachi Energy、HD Hyundai、Hyosung、GE Vernova 等竞争；GT 受益于美国产品需求 | 项目被多家设备重复计数，产能投资不等于当年 MVA 出货 |
| 业务组合 | GS+GT 是本轮数据中心电力的核心；公司计划将 Transformation of Industry 分拆为独立实体，同时正逐步启动 Omterra 新品牌 | 组织调整、风电业务遗留风险、执行/供应链、现金预收能否持续 |
| 财务与资本效率 | FY2026 集团指引为可比收入增长 14–16%、P&SI 利润率 10–12%（预期接近上限）、净利润约 €4bn、税前 FCF 约 €8bn | 高 backlog 并非无风险收入；大项目交付、质保、营运资本和客户集中度需跟踪 |

FY2025 是公司修复后的基线：订单 €58.9bn、收入 €39.1bn、P&SI €2.355bn、净利润 €1.685bn、税前 FCF €4.663bn、期末 backlog €138bn。GS 与 GT 的高增长是主因之一，但股东回报仍要扣除项目执行、风电业务和资本结构风险。[FY2025 业绩][13]

## 6. 与 2027 新增数据中心电力台账的连接

```text
GS 22GW 数据中心相关 commitments   → 需求/预留线索，不计入
GS 13GW booked（Q1）                → 设备订单总量，未按 DC / 年份拆分，不计入
GT €51bn backlog                    → 设备供给紧张/订单景气，不计入
B&W FastPower 1GW steam sets       → 客户与 COD 未披露，2027 记 0GW（待核）
Applied Digital 相关供电目标 2028   → 2027 记 0GW
```

因此，Siemens Energy 的当前“硬计量贡献”仍为 **0GW**，不是因为公司没有受益，而是因为尚没有一项公开、可去重且在 2027 投运的 `数据中心园区 + Siemens 设备 MW/MVA + energization/COD + IT commissioning` 组合证据。

下一步最值得追的四件事：

1. 将 GS 的 22GW commitments 与季度订单、交付 GW、客户 reservation 转换逐季做桥接；
2. 追 B&W FastPower 的客户、站点、锅炉/汽轮机 EPC、空气许可、燃气接入和 COD；
3. 在 AEP、Dominion、Entergy、ERCOT/PJM/州监管 docket 中反查 Siemens 主变、GIS 或燃机的项目名称与 MVA；
4. 只在同一园区的 physical commissioning 证据齐全后，再回填至 [2027 上游台账](../../数据中心/电力系统/2027新增数据中心电力上游台账.md)。

---

## 来源与口径记录

[1]: https://assets.siemens-energy.com/dam/32b27e9a-af91-4915-8b51-b3af012d0d98/A-Siemens_Energy_Annual_Report_2025-pdf_Original%20file.pdf "Siemens Energy FY2025 年报：业务边界、客户类别、GT/GS 产品与 FY2025 财务；2025-12"
[2]: https://assets.siemens-energy.com/dam/d5e24758-5d19-44f7-b57d-b3ee0057e335/2026-02-11_Q1_Analyst_presentation-pdf_Original%20file.pdf "FY2026 Q1 分析师材料：13GW booked、80GW total commitments、22GW data-center-related；2026-02-11"
[3]: https://www.siemens-energy.com/global/en/home/investor-relations.html "Siemens Energy 投资者关系页：FY2026 Q3 集团订单、backlog、收入、利润与业绩材料入口；2026-08-05"
[4]: https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-signs-agreement-with-siemens-energy-to-commence-work-on-20-steam-turbines-for-data-center-power-generation "B&W：与 Siemens Energy 为 FastPower 数据中心项目启动 20 台/1GW SST-300 汽轮发电机组工作；2026-08-11"
[5]: https://www.babcock.com/home/about/corporate/news/babcock-and-wilcox-selects-siemens-energy-to-supply-steam-turbine-generator-sets-for-applied-digital-data-center-power-project "B&W：Applied Digital AI Factory 的 Siemens 汽轮发电机组、1GW 目标及 2028 年底供电时间表；2026-01-08"
[6]: https://www.siemens-energy.com/global/en/home/press-releases/siemens-energy-is-investing--1-billion-and-creating-highly-skill.html "Siemens Energy 美国 $1bn 制造扩张、地点与产品范围；2026-02-03"
[7]: https://assets.siemens-energy.com/dam/47e51057-e95f-4dba-9d0f-b29900a43d5a/Reference_TwoPager_Equinix-pdf_Original%20file.pdf "Equinix DB5：9×SGT-A05、45MW 的调峰与备用电参考案例；2025"
[8]: https://www.siemens-energy.com/global/en/home/stories/gas-turbine-iowa-power-demand.html "Morgan Valley Energy Center：三台 SGT6-5000F、待批准且预计 2030 运行；2026-06-03"
[9]: https://www.siemens-energy.com/us/en/home/press-releases/earnings-release-q1-fy-2026.html "FY2026 Q1：美国高三位数百万欧元的数据中心相关 GT 订单、GT backlog €45bn；2026-02-11"
[10]: https://www.siemens-energy.com/global/en/home/press-releases/earnings-release-q2-fy-2026.html "FY2026 Q2：GT 变压器产品增长主要受美国需求驱动；2026-05-12"
[11]: https://www.siemens-energy.com/global/en/home/products-services/solutions-industry/data-center.html "数据中心方案与燃机型号名义功率范围；2026-09-17 查阅"
[12]: https://www.siemens-energy.com/us/en/home/products-services/product/modular-onsite-power-generation-data-center.html "Siemens Energy/Eaton 模块化表后发电解决方案及加速建设的公司主张；2026-09-17 查阅"
[13]: https://www.siemens-energy.com/us/en/home/press-releases/siemens-energy-fulfills-all-commitments---and-increases-mid-term.html "FY2025 订单、收入、利润、现金流与 backlog；2025-11-14"
