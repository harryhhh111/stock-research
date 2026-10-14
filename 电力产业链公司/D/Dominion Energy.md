# Dominion Energy（NYSE: D）研究

> 初稿整理：2026-09-15 ｜财务数据截至：2026Q2（2026-07-31 披露）｜数据中心合同与项目进度截至：2026-09-15
>
> 研究目的：将 Dominion 的大型负荷合同、输电/变电站工程和园区接电进度纳入数据中心电力台账。它不是设备供应商；它直接决定许多 Virginia 园区能否获得电力，但公开容量也不能直接视为已上线 IT。

## 结论先行

1. **Dominion 是“设备商订单”之外最值得研究的验证方。** 其 Virginia 公用事业业务覆盖从并网、输电到配电的接电流程；对超过 50MW 的新数据中心，通常需要延伸输电线路并新建变电站。[数据中心接电流程][4]
2. **“合同 51GW”不能用于 2027 新增 GW 估算。** 截至 2026-03，Dominion Energy Virginia 披露的 51.0GW 数据中心合同容量由 SELOA 29.5GW、CLOA 11.1GW、ESA 10.4GW 构成。SELOA 只是详细工程计划与费用补偿安排；CLOA 才授权施工；ESA 才约定取电方式及回收机制。即便 CLOA/ESA 也不等同已接电、机房调试或 Active IT。[2026Q1 材料][1]
3. **应以“已接入园区”和“指定工程投运”来落地。** 公司 2025 年预计全年新接入 8 个数据中心园区，最终规划容量 561MW；这是已完成接入的园区容量口径，仍不代表 561MW 已被 IT 实际消化。到 2027 年，Edsall 变电站项目计划于 10 月 energize，明确服务 Fairfax 的增长数据中心负荷，但未公开其专属 MVA，因此暂不计入 GW。[2025 IRP][2] [Edsall 项目页][5]
4. **对 D 股票而言，数据中心带来受监管资本开支机会，也带来监管、融资和并购不确定性。** 2026 年 5 月，NextEra 与 Dominion 宣布全股票合并，仍须多方监管和股东批准，目标于 2027 年下半年完成；因此当前不能把 D 当作独立、长期不变的估值主体。[合并公告][7]

---

## 1. 公司定位：它在数据中心电力链中做什么

```text
数据中心开发商提交站点、负荷信和负荷爬坡计划
                 ↓
Dominion 制定短期/长期供电方案
                 ↓
输电线路、变电站、配电网络的设计、土地、许可、采购、施工
                 ↓
园区分阶段接电 / 可 commissioning
                 ↓
UPS、液冷、IT 机柜上架并运行
```

Dominion Energy Virginia（DEV）是垂直整合的受监管电力公用事业，运营发电、输电和配电系统；2025 IRP 口径覆盖 Virginia 和 North Carolina 约 280 万电力客户。对数据中心研究而言，它最有价值的不是卖出多少电，而是公开的**接电合同分层、监管许可和输电/变电站进度**。[2025 IRP][2]

公司自己的接电说明明确：

- 小于 50MW 的新数据中心常可利用既有配电设施，典型需要 1–2 年；
- 超过 50MW 的项目通常需要新输电线路和新变电站；
- 服务通常按园区负荷爬坡分阶段提供，可能存在使早期 commissioning 先进行的 bridging solution；
- 具体时间取决于站点、既有电网、路权、地方许可、材料供应与监管申报。

这解释了为什么单独知道“某厂商卖出主变”或“某开发商签下 1GW 土地/电力”均不足以确认 Active IT。[数据中心接电流程][4]

## 2. 数据中心合同漏斗：必须按阶段拆开

### 2.1 当前可用的正式披露

| 截止点 | ELOA/SELOA | CLOA | ESA | 合计 | 正确解读 |
|---|---:|---:|---:|---:|---|
| 2025-07-31 | 30.132GW | 7.098GW | 9.815GW | 47.045GW | IRP：ESA+CLOA 的 firm capacity 为 16.913GW；ELOA 仍处工程研究阶段 |
| 2026-03 | 29.5GW | 11.1GW | 10.4GW | **51.0GW** | Q1 投资者材料；名称从 ELOA 改为 SELOA，含义为变电站详细工程计划 |

合同定义：

| 阶段 | 公司定义 | 在模型中的状态 |
|---|---|---|
| ELOA / SELOA | 详细工程计划，客户补偿 Dominion 相应成本 | **研究/设计**，不计接电容量 |
| CLOA | 授权建设；客户若退出，须补偿 Dominion 已支出成本 | **已授权施工**，进入项目台账候选，但仍不计 Active IT |
| ESA | 界定客户如何取电与成本回收机制，含客户不取电时的收入要求 | **供电合同**，是较强承诺，但仍必须核对物理投运和上架 |

因此，51GW 不是“2027 可接电 51GW”，更不是“2027 新增数据中心 IT 51GW”。它是不同成熟度项目的**终态请求容量总和**。即使只使用 2026-03 的 CLOA+ESA，也只是 21.5GW 的较强合同承诺，仍跨越多个投运年份、多个园区与负荷爬坡阶段。[2026Q1 材料][1]

### 2.2 实际接入是更强、但仍非 Active IT 的证据

2025 IRP（截至 2025-10-01）记录：当年已接入 6 个新数据中心园区、最终容量 456MW；预计年底再接入 2 个，合计 **8 个园区 / 561MW 最终容量**。2024 年则接入 15 个园区、最终容量 977MW。

这是可用于核验年度“新增园区接电”的重要锚点，但需保留三个限制：

1. `ultimate capacity` 是园区最终可服务容量，未披露当年首期实际 MW；
2. 它是电力服务容量，不是 IT MW，不能不经 PUE/冗余/负荷因子处理便与 Active IT 对比；
3. 单个园区、客户和阶段没有在 IRP 公布，无法直接与 GPU 或变压器订单一一匹配。

## 3. 2027 可验证的输电/变电站节点

| 项目 | 公开状态与日期 | 数据中心关联 | 能否计入 2027 新增 Active IT |
|---|---|---|---|
| **Edsall（Fairfax）** | 新变电站连接既有 Van Dorn；2026Q2–2027Q4 建设，计划 **2027-10 energize** | 公司明确称其用于服务当地增长的数据中心负荷 | 否。是 2027 “接电路径将投运”的硬节点，但未披露专属客户、MVA、园区调试或 IT 上架。[Edsall][5] |
| **Centreport（Stafford）** | 新变电站 + 双回 230kV 线路；已获 SCC 最终令，2026 夏开工，计划 **2027 夏完工** | 面向 Stafford 增长负荷，公告未点名数据中心 | 否。记录为 2027 输电工程候选；没有项目专属 DC/MVA，不分配给数据中心。[Centreport][6] |
| **Culpeper Tech Zone** | 四座新变电站 + 230kV 线路；2026 秋开始变电站建设、2027 春输电线预施工，预计 **2029 春完成** | 公司明确支持数据中心负荷增长 | 否。证明 2027 仍在建设，而非已投运；不应提前计入。[Culpeper][8] |

这些项目说明：真正决定 2027–2029 节奏的是变电站、输电线路、监管许可、土地/路权和材料的组合，而非单个电力设备厂的订单金额。下一轮应从每个项目的 SCC docket、项目概览和设备供应商记录中补足 MVA、主变数量、SAT 与园区客户。

## 4. 财务、资本开支与回报框架

| 项目 | 已披露数据 | 备注 |
|---|---:|---|
| 2026 年 operating EPS 指引 | $3.45–3.69/股，中点 $3.57 | 非 GAAP；Q2 维持指引 |
| 2026–2030 资本投资计划 | 约 $65bn | 是受监管资产增长的基础，不等于全部数据中心支出 |
| 2026Q2 operating EPS | $0.79/股 | 同比 +$0.04 |
| 2026Q2 GAAP EPS | $0.37/股 | 与 operating EPS 差异大，应区分 |
| Dominion Energy Virginia 2026Q2 operating earnings | $670m | 同比 $549m；包含天气、用量、费率审查、资本回报等多因素 |
| 季度股息 | $0.6675/股 | 2026-07-28 宣布；并购完成前政策仍由董事会决定 |

受监管 utility 的核心不是把“数据中心合同容量 × 电价”直接计算成利润，而是：允许的 rate base、监管批准的回报率、资本成本、需求是否如期兑现，以及大型客户是否承担其造成的增量系统成本。2026Q2 的 DEV 经营利润同比增加 $121m，其中包含 2025 biennial review、rider equity return、客户使用量等多重因素，不能全部归因于数据中心。[2026Q1 材料][1] [2026Q2 业绩][3]

## 5. 客户、竞争、风险与治理

- 2025Q4 材料称 DEV 服务 50 多家客户的 450 多个数据中心，并展示 Alphabet、Amazon、Microsoft、Meta、Equinix、Digital Realty 以及 CoreWeave、CyrusOne、CoreSite、QTS 等为“select”客户/平台；这不是逐项目供电合同清单，也未披露各自 MW。[2025Q4 材料][9]
- 同区域直接竞争不是另一台变压器，而是可替代站点与其他 utility/PJM 接入区；对设备商而言，Dominion 是潜在采购方和项目推进方。
- 主要运营风险是大负荷集中于 Northern Virginia/Loudoun、输电材料与许可、PJM 容量充裕度、资本开支和融资成本、以及大客户的建设节奏。
- **治理/交易风险必须单列。** NextEra 与 Dominion 于 2026-05 签署全股票合并协议，2026-07 已向各主管机构提交申请，预计 2027 年下半年完成但取决于股东及 Virginia、North Carolina、South Carolina、FERC、NRC 等批准。完成后 D 将不再独立上市，故独立公司估值的时间窗口和交易换股条款是第一层问题。[合并公告][7] [监管申请][10]

## 6. 与“2027 新增数据中心电力”台账的连接

Dominion 提供的正确证据链为：

```text
SELOA/ELOA（设计） → CLOA（授权建设） → ESA（供电协议）
          → 输电/变电站施工 → energize / 分阶段接电
          → 园区机电 commissioning → Active IT
```

仅最后两步附近的、带有园区专属 MW/MVA 和日期的数据，才可用于年度 Active IT 计算。当前可加入 2027 项目候选池的是 Edsall 的 2027-10 energization；但因为 MVA、客户和上架量缺失，其在全球 2027 新增 Active IT 总量中的数值暂记 **0GW（待核）**，而不是估一个数填进去。

## 7. 下一步研究任务

1. 逐个下载 Dominion 公开项目的 SCC docket 与申请材料，提取主变数量、MVA、电压、投资额、投运日和服务对象。
2. 将 ESAs/CLOAs 按项目地理位置与公开的开发商园区去重，建立“合同阶段—电网施工—客户建设”的单园区行。
3. 每季更新 SELOA/CLOA/ESA，并观察项目由 SELOA 向 CLOA/ESA 的转换，而不是只看合同总量。
4. 查询 2026Q3 及后续 IRP/季度材料是否披露 2027 年实际园区接入数和最终容量。
5. 若合并获批，改以 NextEra（NEE）为投资主体，同时继续将 Dominion Energy Virginia 作为接电证据来源。

---

## 来源与口径记录

[1]: https://s2.q4cdn.com/510812146/files/doc_financials/2026/q1/2026-05-01-DE-IR-1Q-2026-earnings-call-slides-vTC.pdf "Dominion Energy 2026Q1 投资者材料：合同阶段、2026 指引与资本计划；2026-05-01"
[2]: https://cdn-dominionenergy-prd-001.azureedge.net/-/media/content/about/our-company/irp/pdfs/2025-integrated-resource-plan-update.pdf?rev=c656e4bd80184dbc80d4531cb6e9e975 "Dominion Energy Virginia/NC 2025 IRP Update：园区接入、合同阶段、负荷预测与项目计划；2025-10-15"
[3]: https://investors.dominionenergy.com/news/press-release-details/2026/Dominion-Energy-Announces-Second-Quarter-2026-Results/default.aspx "Dominion Energy 2026Q2 业绩；2026-07-31"
[4]: https://www.dominionenergy.com/virginia/large-business-services/data-center-requests "Dominion 数据中心服务申请流程、>50MW 接电要求与分期供电说明；2026-09-15 查阅"
[5]: https://www.dominionenergy.com/about/delivering-energy/electric-projects/power-line-projects/edsall "Edsall 新变电站与 2027-10 energize 时间表；2026-09-15 查阅"
[6]: https://www.dominionenergy.com/centreport "Centreport 230kV 线路/变电站与 2027 夏完工计划；2026-09-15 查阅"
[7]: https://investors.dominionenergy.com/news/press-release-details/2026/NextEra-Energy-and-Dominion-Energy-to-Combine-Creating-the-Worlds-Largest-Regulated-Electric-Utility-Business-and-North-Americas-Premier-Energy-Infrastructure-Platform-Benefiting-Customers/ "NextEra 与 Dominion 合并协议及换股条款；2026-05-18"
[8]: https://www.dominionenergy.com/about/delivering-energy/electric-projects/power-line-projects/culpeper-tech-zone "Culpeper Tech Zone 四变电站/230kV 项目与 2029 完工计划；2026-09-15 查阅"
[9]: https://s2.q4cdn.com/510812146/files/doc_financials/2025/q4/2026-02-23-DE-IR-4Q-2025-earnings-call-slides-vTCI.pdf "2025Q4 投资者材料：客户平台与数据中心数量；2026-02-23"
[10]: https://investors.dominionenergy.com/news/press-release-details/2026/NextEra-Energy-and-Dominion-Energy-file-to-combine-building-a-stronger-company-to-meet-growing-power-demand-across-four-of-Americas-fastest-growing-states-while-keeping-energy-affordable-and-reliable/default.aspx "各监管机构合并申请与预期完成时间；2026-07-15"
