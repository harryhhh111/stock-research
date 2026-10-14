# 数据中心供给端：未来 3 年新增多少 GW

**整理日期**：2026-09-02 | **数据截止**：2026-08-31
**用途**：《coding 需求模型》（统一版）的供给侧对照
**信息标注**：【一手】机构原始报告/官方披露；【二手】媒体转述

---

## TL;DR

| 口径 | 未来 3 年（2026–2028/29）新增 |
|---|---|
| **全球总数据中心（JLL，2026–2030 共 ~97 GW）** | 3 年约 **50–60 GW** |
| **美国（Goldman Sachs，按排期风险调整）** | 2026 约 **13.7 GW** + 2027 约 **18 GW**（排期 36.3 GW 打折）+ 2028 更多，**3 年 ~35–50 GW** |
| **北美在建管线（JLL，2026 年 8 月实测）** | **66 GW under construction**，95% 已预租，多数 2027–2029 交付 |
| **全球 AI 专用容量（McKinsey 需求模型）** | 2026–2029 累计约 **60–90 GW**（年增量从 ~17 GW 爬升到 ~27 GW） |

**一句话：全球未来 3 年新增数据中心容量约 50–90 GW（取决于口径），仅北美在建就有 66 GW；这是人类历史上最大的基础设施扩建周期之一，但交付风险真实存在（排期兑现率约 50–60%）。**

---

## 1. 最硬的近期数据：Goldman Sachs 美国排期（2026 年 5 月）【一手】

基于 Aterio 的逐设施数据（许可进度、施工状态、卫星图像）：([Goldman Sachs](https://www.goldmansachs.com/insights/articles/us-data-center-power-demand-projected-to-double-by-2027 "citation"))

| 年份 | 新增容量 |
|---|---|
| 2024 实际 | 6.4 GW |
| 2025 实际 | 8.5 GW |
| **2026 排期** | **13.6 GW**（Q1 已交付 2.2 GW，Q2–Q4 预计 11.5 GW） |
| **2027 排期** | **36.3 GW** |

**关键折扣**：历史上排期 4 个季度内的项目只有 ~72% 按时上线；Goldman 调整后假设次年兑现率 ~60%、两年后 ~50%。典型建设周期：拿许可后 18–24 个月。

## 2. 在建管线实测（2026 年中）【一手】

- **JLL（2026-08-11）**：北美 **66 GW 在建**，95% 已预承诺；空置率连续 3 年 1%；H1 2026 吸纳量创纪录 25 GW；现在签约的租户锁的是 **2028 年交付**。德州 26 GW（存量+在建）居首，弗吉尼亚 13 GW；77% 在建容量在 frontier 市场（西德州、俄亥俄、路易斯安那、卡罗来纳）。 hyperscaler 占需求 59%（28 GW 自建），neocloud 11%，纯 AI 公司 7%。([JLL](https://www.jll.com/en-us/newsroom/data-center-demand-exceeds-expectations-in-h1-2026 "citation"))
- **追踪器分歧注意**：2025 年全球在建，Cushman & Wakefield 数 31.7 GW，BloombergNEF 只数 23.1 GW，CBRE 主要市场口径甚至同比下降（许可/电力延迟）——**不同机构口径差异可达 40%**。([UVRN](https://www.uvrn.org/research/global-data-center-construction-2025-record-trackers-diverge-cbre-decline "citation"))【二手】
- **Currence（2026-02）**：2026 年官宣投产 16 GW（约 140 个项目），但实际在建只有 ~5 GW——**官宣管线 30–50% 年内无法兑现**。([Currence](https://www.currence.ai/blog/data-center-outlook "citation"))【二手】

## 3. 中长期预测框架【一手】

| 来源 | 预测 |
|---|---|
| **JLL 全球展望（2026-01）** | 2026–2030 全球新增 **~97 GW**，2030 年总容量 ~200 GW（翻倍），CAGR 14%；美洲占 50%、CAGR 17%；2027 年推理负载超过训练。([JLL](https://www.jll.com/en-us/insights/market-outlook/data-center-outlook "citation")) |
| **McKinsey（2025-05）** | AI 容量 44 GW（2025）→ **156 GW（2030）**；年增量从 13 GW（2025）爬升至 31 GW（2030），2025–2030 累计新增 AI 容量 **124 GW**；总投资 $6.7T。([McKinsey](https://www.mckinsey.com/featured-insights/charts/data-center-demands "citation")) |
| **Goldman Sachs（全球）** | 全球 55 GW → **84 GW（2027）**；美国 30 GW（2025）→ 90 GW+（2030），CAGR 22%。([Goldman Sachs](https://www.goldmansachs.com/insights/articles/ai-to-drive-165-increase-in-data-center-power-demand-by-2030 "citation")) |
| **ClusterBid 管线（Q2 2026）** | 全球 AI 设施在建/开发 85.4 GW（美国 38.2 GW 占 45%）；只有 28% 完全去风险；风险调整后 2030 年前可交付 **62–68 GW**。([ClusterBid](https://clusterbid.com/blog/ai-data-center-construction-pipeline-2026-2028-planned-capacity-region "citation"))【二手】 |

## 4. 约束条件（决定兑现率）

- **电力接入是瓶颈**：美国数据中心并网排队请求达 380 GW（远超管线本身），平均并网周期从 2.4 年（2022）拉长到 **4.8 年（2026）**；ERCOT 收到 474 GW 接入请求、其中 ~90% 是数据中心，德州已开始审计。应对：美国管线 35% 带现场天然气发电、8% 核电 PPA/共址（微软三里岛 835 MW、AWS-Susquehanna 960 MW）。【二手】
- **政策阻力开始出现**：纽约州 2026 年 7 月对新建 hyperscale 数据中心实施最长一年的许可暂停；宾州把 AI 数据中心移出快速审批通道；美国被社区反对阻止/延迟的项目估 $64B。【二手】
- **GW 级项目清单仍在膨胀**：Stargate 五个新园区 ~7 GW / $400B+；AMD-Anthropic 最多 2 GW（首个 1 GW 2027 H1）；DOE 肯塔基 1.8 GW 园区；欧盟 7 个 AI Gigafactory 招标。([AI 2027 Tracker](https://ai2027-tracker.com/predictions/datacenter-buildout/ "citation"))【二手】

## 5. 与我们 coding 需求模型的对照

2029 年 coding 推理装机需求（《coding 需求模型》统一版 v3.2）：基准 **2.3–3.2 GW**、激进 4.5–6.3 GW。

**结论：coding 一个用途在供给面前是零头**——即使激进情景（4.5–6.3 GW 装机）也只相当于北美在建管线（66 GW）的 7–10%、3 年全球新增（50–90 GW）的 5–13%。供给故事的主导变量是训练 + 全部推理（消费 chat、企业 agent、视频生成），coding 只是其中增长最快但绝对值尚小的一条曲线。**这也意味着：如果数据中心/电力标的出现供需错配，不会是 coding 需求缺席造成的；反过来，coding 需求的爆发不需要新增供给专门为它建设。**
