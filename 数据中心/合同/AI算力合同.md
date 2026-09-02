# AI 算力合同数据库（IREN / HIVE / Nebius / CoreWeave）

> 整理/核对日期：2026-08-26（由 IREN/HIVE 两份合同文档合并为一，并加入 Nebius 披露数据；同日补服务范围分层与 colo 经济性、CoreWeave 合同池；原文档已删除）。2026-08-28 更新：IREN FY26 财报（新签 3 年合同 >$20M/MW、+125%）；修正 IREN 回本口径（全口径 CapEx $8.1–8.5M/柜，EBITDA 0.92–0.96×，替换原 1.67× 误算）。
> **六字段口径规则（固定）**：一条算力合同 = **签约月份 + 设备代际 + 合同期限 + 交付月份 + $/柜/年 + $/MW·年**，缺一个（尤其期限）就不做横向价格比较。rack-scale 合同（GB200/GB300/Rubin 等）**按 NVL72 机柜统计**；B200 及更早按单 GPU 租赁的才用 $/GPU·h；colo 用 MW。**价格绑定签约日期，交付单列**。期限是价格公式的核心变量（Nebius×Microsoft 的 SOW 定价表即按 GPU Type + Service Term + $/GPU-hour 定义），不是备注。
> 关联：`../数据中心运营.md`（$/GPU·h 口径与收入侧分层）、`../数据中心1GW.md`（机柜密度口径）、`../../Nebius公司研究/research/合同披露情况.md`（Nebius 电力/园区/财务细节）。

**一句话结论**：2025-11 至 2026-08 的可核实合同拼出一条完整价格阶梯——**5 年 GB300 长约 $1.84–2.50M/柜/年（IREN 超级批发 → HIVE 企业单，+36%）→ Nebius 1–3 年中期单 $20–25M/MW/年 → Nebius 3–6 月短期 $40–50M/MW 年化 → 零售 $7–10/GPU·h**。价差由期限、签约时点、客户规模三个变量解释，与公司品牌无关。

## 1. 六字段总表

| 签约 | 公司 → 客户 | 设备 | 期限 | 交付 | TCV | **$/柜/年** | **$/MW·年** | 备注 |
|---|---|---|---|---|---|---:|---:|---|
| 2025-09 | **Nebius → Microsoft** | dedicated GPU clusters（型号未披露） | 5 年（至 2031） | 分批 | **$17.4B**（追加后 ≤$19.4B） | — | **≥$11.6M**（Vineland ≤300MW，下限） | **预付款 ~$6.96B ≈ 40%**（[19][21]） |
| 2025-11 | **IREN → Microsoft** | GB300 NVL72 ≈1,056 柜（反推） | 5 年 | 2026 分批 | **$9.7B** | **≈$1.84M** | **≈$9.7M**（critical IT）/ $13.6M（柜功率） | 预付 ~20%（[1][2][3]） |
| 2025（月未核） | Nebius → Meta | 2 个 dedicated GPU clusters + 存储/连接 | 5 年 | 分 2 批 | **~$2.9B** | — | — | （[23]） |
| 2026-02-13 | HIVE → 多名客户 | B200 ×504（单 GPU 口径） | 2 年 | 2026-05 已上线 | ~$30M | —（$2.90/GPU·h） | — | 公司直接披露单价（[9][10][11]） |
| 2026-03-16 | **Nebius → Meta** | **Vera Rubin** dedicated capacity | 5 年 | 2027 初起量 | **$12B** + ≤$15B 剩余容量兜底 | — | — | 兜底部分非锁死收入（[22]） |
| 2026-05-07 | IREN → NVIDIA | 风冷 Blackwell 60MW（含 Mirantis 编排软件） | 5 年 | 2027 初 ramp | **$3.4B** | —（非 NVL72） | **≈$11.3M** | +5GW 战略合作、$2.1B 认股权证（[6]） |
| 2026-06-18 | HIVE → Cohere/Bell | GB200 NVL72 ×32 柜 | 3 年 | 2026 Q4–2027 Q1 | ~$220M | **≈$2.29M** | ≈$17.0M（135kW 口径） | FY27Q1 更新口径 $2.34M（[12]） |
| 2026-06-25 | HIVE → 瑞典企业（Boden colo） | ~25MW critical IT | ≤10 年 | 未披露 | 潜在 ~$45M ARR | — | **$1.80M**（纯机房） | ⚠️ non-binding LOI（[15][16]） |
| 2026-08-17 | HIVE → 匿名投资级企业 | GB300 NVL72 ×28 柜 | 5 年 | 2026 Q4 | $350M | **$2.50M** | ≈$18.5M（135kW 口径） | CapEx $6.61M/柜、deposit 10%（[13][14]） |
| 2026Q2 | Nebius → Reflection/Cohere/AI neolab/量化（4 单） | next-gen NVIDIA（含 GB300） | **1–3 年** | — | 平均 TCV >$1B | — | **$20–25M**（2026 base 仅 ~$12M） | 预付款覆盖 50–60% CapEx（[20]） |
| 2026Q3 起 | Nebius 短期 dedicated（已签首单） | 含 GB300 clusters | **3–6 个月** | — | — | — | **$40–50M 年化** | 训练/RL/发布冲刺，不能当年收入（[20]） |
| 2026-08 | **IREN → 新客户（管理层口径）** | 未披露 | **3 年** | — | — | — | **>$20M（谈判中 ~$25M）** | FY26 电话会：3 年价 +125%、5 年 +70% vs 2025-11；GPU ~2 年回本（[35]） |
| 2025-03 起 | **CoreWeave → OpenAI/Meta/Jane Street 等** | 含 Vera Rubin | ~4–6 年（加权 ~5 年） | 2025–2032 分批 | **订单池 $104.2B backlog**（2026-06-30） | — | — | **MW/GPU 数全部未披露，按六字段规则不做价格比较**，明细见 §5（[24]–[34]） |

⚠️ **$/MW·年 两种分母不能混**：critical IT 口径（IREN 189kW/柜 → $9.7M）vs GPU 柜功率口径（135kW → $13.6M）。HIVE/Nebius 的 critical IT MW 未披露，表内 135kW 口径仅用于同口径对比。

⚠️ **合同卖的东西不一样，价格更不能直接比**——每笔合同按服务范围分层：

| 合同 | GPU/网络 | 数据中心 | 云平台/调度/技术支持 | 归类 |
|---|:-:|:-:|:-:|---|
| IREN → Microsoft | ✅ | ✅（自持） | ❌（Microsoft 自带 Azure/软件栈） | **裸算力/基础设施容量** |
| IREN → NVIDIA | ✅ | ✅（自持） | ✅（含 Mirantis 编排软件） | managed cloud（IREN 往上走的第一步） |
| HIVE 三单 | ✅（+Quantum-X800/VAST 存储） | ✅（租 Bell，成本含 colo 费） | 部分（集群交付，平台层弱） | 算力 + 硬件配套 |
| Nebius 中期/短期单 | ✅ | ✅（自有 + colo 混合） | ✅（K8s/存储/AI 软件/white-glove 工程支持） | **全栈 AI Cloud** |
| Nebius → Microsoft/Meta | ✅ | ✅ | 部分（dedicated capacity，大客户自带平台） | 偏向批发（融资锚） |
| CoreWeave → OpenAI/Meta 等 | ✅ | ✅（自有 + landlord 混合） | ✅（K8s 原生全栈；Meta 单强调 inference 优化） | **全栈 AI Cloud（4–6 年批发长约为主）** |

> 含义：**Nebius 的溢价一部分来自服务层而非 GPU 本身**；同一家 Nebius，卖给 Microsoft/Meta 的批发单也比卖给 AI-native 的全栈单便宜。比较价格时先看服务层级是否对齐。

## 2. IREN 明细（Microsoft $9.7B 单 = 最完整的批发样本）

- **合同事实**：$9.7B / ≈5 年 / ≈76,000 颗 GB300（4 批 × ≈19,000）/ Horizon 1–4 各 50MW（合计 **200MW critical IT**）/ 2026 分批交付（[1][2][3][4][5]）；Dell 硬件合同 **≈$5.8B**（GPU + ancillary）
- **机柜反推**：19,000÷72 ≈ 264 柜/Horizon × 4 = **≈1,056 柜**（非官方披露值）；密度 **5.3 柜/MW**（低于 Vertiv reference 6.4 柜/MW，因每柜分摊 IT 更重：189kW vs 157kW）
- **机柜经济**：5 年 $9.19M/柜 → **$1.84M/年 ≈ $153k/月 ≈ $210/柜·h**（=$2.91/GPU·h）；分摊硬件 $5.49M/柜 + 分摊数据中心 $2.65–3.03M/柜 = **全口径 CapEx ≈$8.1–8.5M/柜**；项目 EBITDA margin ~85%（扣电费/维保/机房运营，未扣 corporate/融资/D&A，[7]）→ 5 年 EBITDA ≈$7.81M/柜 ≈ **CapEx 的 0.92–0.96×**——首份合同只够基本回本，真正回报靠数据中心资产遗留（换 Rubin/Feynman 继续赚钱）。⚠️ 不要再用"收入/硬件 CapEx ≈1.67×"——那漏掉了 $2.8–3.2B 数据中心投资（拆解见 `../矿场/IREN.md` §3）
- **价格拆解**（IREN 内部 colo charge $130/kW/月）：数据中心层 ≈$34/柜·h（$1.56M/MW/年）+ 算力层 ≈$176/柜·h（$8.14M/MW/年）= 全包 $210/柜·h（$9.7M/MW/年、$808k/MW/月、$1,108/MW·h）（推算过程见 `../矿场/IREN.md` §4）
- **功耗三口径**：GPU rack 135kW / 分摊 critical IT 189kW / 园区取电 220–240MW（PUE 1.10–1.20）；Horizon 设计支持 200kW/rack
- **CapEx 全口径**：GPU $5.8B + 数据中心基建 $14–16M/MW × 200MW ≈ **$8.6–9.0B**（[7]）；数据中心 5 年后仍在，可装下一代 GPU
- **零售对照**：GB200 on-demand $10.50/GPU·h × 72 = $756/柜·h（[8]）vs 本合同 $210/柜·h 批发长约——两种商业模式不能直接比

## 3. HIVE 明细（asset-light 样本：租 Bell 机房做 GPU 运营）

- **四笔合同**（明细见总表）：B200 $2.90/GPU·h（公司直接披露；⚠️ TCV 反算是 $3.40 all-in，不强制除）→ GB200 $2.29M/柜/年 → GB300 $2.50M/柜/年；Boden 为纯机房 LOI（$150/kW/月，不计入 backlog）
- **GB300 单单位经济**：$185M CapEx（$6.61M/柜）→ $70M/年收入 → 5 年 $350M TCV，**TCV/CapEx ≈ 1.89×**（未扣电费/Bell colo 费/网络/维保/融资）
- **订单统计三档**：A. 已签 GPU Cloud **≈$600M TCV / 60 个 NVL72**；B. **年化收入 ≈$180M**（$35M 已上线 + $145M contracted，Q4 2026 上线——最该盯的数）；C. colocation 仅 Boden LOI
- **无订单项目**：Toronto 320MW（CAD $3.5B，按 $150/kW/月 潜在 $360M/年 colo ARR）与 Grand Falls 50MW 均**无 anchor tenant**，不能算 backlog（[17][18]）

## 4. Nebius 明细（价格发现者：三层定价 + 预付款机器）

- **合同结构**：Microsoft $17.4B 是融资锚（40% 预付、多 tranche 交付）；Meta 2026 必须拆开——$12B 是锁死的 Vera Rubin dedicated capacity，≤$15B 是"剩余容量兜底"（第三方不买的 Meta 才买），不能当确定收入；Q2 四大单"平均 TCV >$1B"是组合口径，非每单正式披露（Reflection 单独报道 >$1B）
- **价格曲线（2026 涨价周期实证）**：2026 base ~$12M/MW → Q2 中期新签 $20–25M/MW → Q3 短期 $40–50M 年化；首次 capacity auction 比 Blackwell 历史最高价 +15%；老一代 GPU Q2 环比 Q1 也 +30%；产能售罄（[20]）
- **回本与预付款**：Q2 新签合同 **payback ≈22 个月**（覆盖 associated CapEx + related OpEx；历史水平 2–3 年）；~70% Q2 合同带预付款，覆盖 50–60% CapEx；2026 全年预付款 **>$9B** vs CapEx 指引 $20–25B（覆盖 36–45%）——客户在帮它出 GPU 钱
- **总订单**：**>$40B customer commitments**（已用于融资抵押），但 ≠ GAAP backlog（含 Meta $15B 兜底等特殊结构）
- **电力三口径（不能混）**：Contracted 5GW（2026 底目标）≠ Connected 800MW–1GW（2026 底）≠ Active（2025 底仅 ~170MW）——Connected 到产生收入还差 commissioning/装 GPU/客户 onboarding 数月，故 2026 底 ARR 指引 $7–9B 远低于"1GW×$20–25B"（[19][20]）
- **未披露清单（不要硬猜）**：Microsoft/Meta 的准确 MW、GPU 型号与数量、机柜数、$/GPU·h、单客户项目 CapEx
- 园区与财务细节见 `../../Nebius公司研究/research/合同披露情况.md` §8/§11/§12

## 5. CoreWeave 明细（最大订单池，但价格字段全缺）

**客户合同**（只看终端算力订单，不含上游租赁/融资）：

| 客户 | 签约 | 金额 | 期限 | 硬件/用途 | 备注 |
|---|---|---|---|---|---|
| **OpenAI** | 2025-03 / 05 / 09 三笔 | 累计 **≈$22.4B** | 分别至 2029-04 / 2030-10 / 2031-05 | 训练+推理，reserved capacity | 首笔 $11.9B 专门设 SPV 用合同现金流融资建设（[24][25]） |
| **Meta** | 2025-09 → 2026-03 扩大 | $14.2B → **≈$21B** | 至 2032-12 | **强调 inference，含最早一批 Vera Rubin**，多地点 | 2026-03 扩单含行使 option（[26][27]） |
| **Jane Street** | 2026-04 | **≈$6B** | 未公布终止日 | ML/量化，多设施，含 Vera Rubin | 另有 $1B 股权投资——**不是订单，不能加进 TCV**；扩单前已付 $100M（2025）+ $220.6M（2026Q1）（[28][29]） |
| **NVIDIA** | 2025-09 | **$6.3B**（initial value） | 至 2032-04 | **剩余产能兜底**：CoreWeave 卖不掉的 unsold capacity 由 NVIDIA 购买 | ⚠️ 性质是 backstop/最低收入保证，**不是终端需求，必须单列**（[30]） |
| **Microsoft** | MSA 自 2023-02 | **≈$10B（媒体报道，非披露）** | 2023–2030 | reserved-capacity order forms | RPO/TCV 被 CoreWeave 保密涂黑（$[*]，SEC 问询后仍未公开）；收入贡献：2023 $81M → 2024 $1.2B → 2025 占 ~67%（[31][33]） |

**订单池经济性**：

- **Revenue backlog = $104.2B**（2026-06-30：RPO $103.7B + 其他已承诺 $0.5B）；收入确认节奏：未来 24 个月 40% / 25–48 个月 39% / >48 个月 21% → 典型的 **4–6 年长期锁单**，非一年期现货（[32]）
- 2026-08-11 财报补充：Q3 头几周又获 **>$25B net new commitments**（未含在 $104.2B 内；客户未拆）。严谨表述：**6 月底 backlog $104.2B + Q3 新增 >$25B**，不能说"当前 backlog $129B"（[32]）
- 订单质量：2026Q2 收入 **98% 来自 committed contracts**（reserved + take-or-pay）；active contracts 客户通常**预付 TCV 的 15–25%**；2025 年底 committed 合同加权平均期限 **~5 年**（[33][34]）——这就是"拿客户订单 → 抵押合同现金流 → 借几十亿 → 买 GPU"的飞轮
- **价格字段全缺**：没有任何一单披露 MW / 机柜数 / GPU 数 → **算不出 $/柜/年、$/MW·年**，这是 CoreWeave 与 IREN/HIVE 最大的信息差

**补全价格的线索**（待挖）：客户合同不披露 MW，但**融资抵押物文件和数据中心房东（Core Scientific、Applied Digital 等）的 SEC 文件会泄露容量**——Meta $21B 买了多少 Rubin、OpenAI $22.4B 对应多少 MW，从上游挖比从 CoreWeave 自己挖更现实。

## 6. 横向对比与价差归因

**控制变量的有效比较**（同设备 + 同期限，GB300 NVL72 5 年）：

| | 签约 | $/柜/年 | $/MW·年（135kW） |
|---|---|---:|---:|
| IREN → Microsoft（1,056 柜超级批发） | 2025-11 | **$1.84M** | $13.6M |
| HIVE → 匿名企业（28 柜） | 2026-08 | **$2.50M** | $18.5M |

→ HIVE 高 **+36%**，解释变量只剩：签约时点差 9 个月（涨价周期）、客户规模（1,056 vs 28 柜）、服务内容（HIVE 含 Quantum-X800 + VAST 存储）。

**分桶规则**：

- HIVE GB200 3 年 $2.29M/柜/年 → "2026 年 3 年期 Blackwell"bucket，**不与 5 年 GB300 直接比**
- 代际价差（同公司、签约差 2 个月）：GB200→GB300 仅 **+9.1%**，且 GB300 拿到 5 年长约（GB200 只有 3 年）——客户对新一代资产老化风险并不担心
- 5 年长约不论谁家都落在 $9.7–11.6M/MW（IREN $9.7 / IREN×NVIDIA $11.3 / Nebius×Microsoft ≥$11.6）——**$20–25M 是"中短约+涨价周期"的价格，不是 Nebius 的公司定价能力**

**商业模式对照**：

| | IREN | HIVE | Nebius | CoreWeave |
|---|---|---|---|---|
| 服务内容 | 裸算力/基础设施（客户自带平台） | 算力 + 硬件配套（平台层弱） | 全栈 AI Cloud（调度/存储/工程支持） | 全栈 AI Cloud（K8s 原生，inference 优化） |
| 模式 | 自持土地/电网/变电站（矿场出身），GPU 批发 landlord | asset-light：租 Bell AI Fabric | asset-light：租 colo + 伙伴代建 + 全栈 AI Cloud | 自有 + landlord 容量混合（Core Scientific/Applied Digital 是房东） |
| 长约价格 | $9.7–11.3M/MW | $2.29–2.50M/柜/年 | ≥$11.6M/MW（Microsoft 单） | **未披露**（backlog $104.2B、加权 ~5 年） |
| 现金成本 | ~$1.5M/MW（无第三方 colo） | 租金含 Bell colo 费 | ~$11M/MW（含 colo 租金） | 未披露（含 landlord 租金） |
| EBITDA margin | 项目级 ~85% | — | AI Cloud ~50% | —（98% 收入来自 committed contracts） |
| 回本 | 首份 5 年合同 EBITDA ≈ 0.92–0.96× 全口径 CapEx（$8.1–8.5M/柜）；回报靠资产遗留 | TCV/CapEx ≈ 1.89× | **22 个月**（含 OpEx），预付款覆盖 50–60% CapEx | 合同现金流抵押融资（SPV），客户预付 15–25% TCV |
| 资产逻辑 | 数据中心 5 年后仍在，可装下一代 GPU | 轻资产快速扩张 | 高价短约快速回本 → 下一代重新定价 | 4–6 年 take-or-pay 锁单 → 抵押订单借钱买 GPU 的飞轮 |

**colo 对价格的双向影响**（示意量级，非公司披露）：自建时基础设施层成本 ~$1M/MW/年；colo 要多付房东层（场地+电力容量+制冷+配电+运维+房东利润）≈ **+$2–4M/MW/年**——所以 Nebius/HIVE 必须比 IREN 卖得更贵才有同等利润。但 colo 的另一面是**快**：自建 100MW 需 2–3 年（土地→电网审批→变电站→建筑→冷却→commissioning），colo 现成容量几个月即可装机——算力紧俏时"早一年上线卖 $20M/MW"比"等两年卖 $10M/MW"更划算，这是 asset-light 模式成立的时点逻辑。

> 四家的正确比较框架不是 Revenue/MW，而是 **每 MW 收入 − colo/电费/运维 − GPU 折旧 = 每 MW 真正赚多少钱**（CapEx/MW → Revenue/MW → EBITDA/MW → 回本年限/ROIC 全链条，详见 `../数据中心运营.md` §三.8）。IREN 买 Mirantis 上软件、Nebius 自建大机房下基础设施——模式正在互相靠近。

## 7. 待办

- **期限折价系数**：完整的"5 年等效价"（P_5yr-equiv = P_3yr × 折价系数）所需系数**不能拍脑袋**——应从 Nebius 同期同代 3 年/5 年合同实际价差提取（其 SOW 确认期限入价，但 Microsoft 定价字段被保密涂黑，需找其他披露）
- Nebius×Meta/Microsoft 若披露 GPU 数或 MW → 补上两家大单缺失的 $/柜/年 字段
- **CoreWeave 价格字段挖掘**：客户合同不披露 MW，改从上游挖——融资抵押物文件（SPV）、数据中心房东（Core Scientific/Applied Digital）的 SEC 文件会泄露容量；目标：Meta $21B 的 Rubin 机柜数、OpenAI $22.4B 的 MW
- HIVE Toronto/Grand Falls 若签 anchor tenant → colo 价格从 LOI 口径变合同口径

[1]: https://www.sec.gov/Archives/edgar/data/1878848/000187884826000015/iren-20251231.htm "IREN 10-K（四 tranche rack 数量大致相等、Dell $5.8B、200MW critical IT、Childress 750MW）"
[2]: https://www.investiment.io/symbols/IREN/earnings/transcripts/2026/1 "IREN Q1 2026 财报电话会（每 Horizon ≈19,000 GB300、135kW/rack、$130/kW/月内部 colo charge）"
[3]: https://iren.com/resources/blog/iren-signs97-billion-agreement-with-microsoft-to-deploy-ai-cloud-infrastructure "IREN 官方公告：$9.7B Microsoft 协议"
[4]: https://www.sec.gov/Archives/edgar/data/1878848/000187884825000081/iren-20250930.htm "IREN Q1 FY2026 10-Q（Microsoft 合同见 Subsequent Events，公告 2025-11-03）"
[5]: https://intellectia.ai/stock/IREN/earnings/transcript-FY2026Q1-2025-11-07 "IREN FY2026Q1 电话会转录（Intellectia，2025-11-07，备选源）"
[6]: https://www.finanznachrichten.de/nachrichten-2026-05/68436903-iren-business-update-and-q3-fy26-results-399.htm "IREN Q3 FY26 Business Update（2026-05-07：$3.4B NVIDIA 合同/60MW/风冷 Blackwell、480MW、$3.7B ARR、Mirantis）"
[7]: https://edgar.secdatabase.com/1657/114036125040072/filing-main.htm "IREN 8-K（2025-11-03：数据中心基建 $14–16M/MW、无第三方 colo、85% 项目 EBITDA margin 口径）"
[8]: https://coreweave.com/pricing "CoreWeave Cloud Pricing（GB200 $10.50/GPU·h）"
[9]: https://www.hivedigitaltechnologies.com/news/hives-buzz-signs-30-million-in-ai-cloud-contracts-accelerating-global-hpc-tier-iii-data-center-expansion/ "HIVE's BUZZ Signs $30 Million in AI Cloud Contracts（2026-02，504 B200/$30M/2 年）"
[10]: https://www.hivedigitaltechnologies.com/news/hive-achieves-fy2026-total-revenue-of-2978-million-158-yoy-hives-buzz-hpc-positioned-for-growth/ "HIVE FY2026 业绩（$2.90/GPU·h 披露、$15M ARR、2026-05 上线）"
[11]: https://www.hivedigitaltechnologies.com/static/hivesite/filings/000106299326002973/form10k.htm "HIVE 10-K（B200 合同 $2.90/GPU·h 披露口径）"
[12]: https://www.hivedigitaltechnologies.com/news/hives-buzz-hpc-closes-usd-220-million-sovereign-ai-gpu-contract-with-bell-ai-fabric-for-cohere-inc/ "HIVE's BUZZ Closes $220M Sovereign AI GPU Contract with Bell for Cohere（2026-06-18）"
[13]: https://www.hivedigitaltechnologies.com/news/hives-buzz-hpc-signs-350-million-ai-cloud-services-agreement-with-investment-grade-enterprise-customer/ "HIVE's BUZZ Signs $350M AI Cloud Services Agreement（2026-08-17）"
[14]: https://www.hivedigitaltechnologies.com/static/hivesite/filings/000106299326004522/form8k.htm "HIVE 8-K（$350M 合同：2,016 GB300、28 NVL72、CapEx $185M、$35M deposit、Q4 2026 部署、$180M 年化口径）"
[15]: https://www.hivedigitaltechnologies.com/news/hive-signs-long-term-hpc-colocation-loi-with-investment-grade-swedish-client-at-boden-retrofit-to-support-up-to-10000-gb300-gpus/ "HIVE Boden Colocation LOI（25MW、最长 10 年、~$45M 潜在 ARR）"
[16]: https://www.hivedigitaltechnologies.com/static/hivesite/filings/000106299326003340/form8k.htm "HIVE 8-K（Boden LOI 为 non-binding）"
[17]: https://www.hivedigitaltechnologies.com/news/hives-buzz-hpc-announces-320-mw-sovereign-ai-infrastructure-in-greater-toronto-area/ "HIVE 320MW Toronto Sovereign AI Infrastructure（CAD $3.5B，无 anchor tenant）"
[18]: https://www.hivedigitaltechnologies.com/news/hives-buzz-starts-building-a-digital-superhighway-for-eastern-canadas-first-sovereign-ai-factory/ "HIVE Grand Falls 光纤建设（70MW→50MW AI Factory，无 anchor tenant）"
[19]: https://assets.nebius.com/assets/e59fb92e-9027-473a-8cac-04f9d2e9ea9a/Shareholder%20Letter%20Q4%202025.pdf "Nebius Q4 2025 Shareholder Letter（Active power ~170MW）"
[20]: https://www.fool.com/earnings/call-transcripts/2026/08/19/nebius-nbis-q2-2026-earnings-call-transcript/ "Nebius Q2 2026 财报电话会（2026-08-12：$20–25M/MW、22 个月回本、预付款 >$9B、>$40B commitments）"
[21]: https://nebius.com/newsroom/nebius-accelerates-us-expansion-adding-up-to-300-mw-capacity-at-new-data-center-in-new-jersey "Nebius 新闻稿（Vineland 园区 ≤300MW）"
[22]: https://assets.nebius.com/assets/2e145023-e8ff-45c6-80f5-c12d1edbfcaa/20260316%20Nebius%20signs%20new%20AI%20infrastructure%20agreement%20with%20Meta%3B%20deal%20to%20accelerate%20growth%20of%20Nebius%E2%80%99s%20core%20business%20in%20AI%20cloud%20.pdf "Nebius × Meta：$12B/5 年 Vera Rubin dedicated capacity（2026-03-16）"
[23]: ../../Nebius公司研究/research/合同披露情况.md "Nebius 合同披露情况（Microsoft $17.4B/$6.96B 预付、Meta 2025 $2.9B、电力三口径、园区清单）"
[24]: https://www.sec.gov/Archives/edgar/data/1769628/000176962825000014/crwv-20250331.htm "CoreWeave 10-Q 2025Q1（OpenAI $11.9B reserved capacity + $4B 追加、SPV 融资）"
[25]: https://investors.coreweave.com/news/news-details/2025/CoreWeave-Expands-Agreement-with-OpenAI-by-up-to-6-5B/default.aspx "CoreWeave 官方：OpenAI 追加 $6.5B，累计 ~$22.4B（2025-09）"
[26]: https://www.sec.gov/Archives/edgar/data/1769628/000176962825000050/crwv-20250925.htm "CoreWeave 8-K（Meta $14.2B 至 2031-12，2025-09）"
[27]: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000154/crwv-20260331.htm "CoreWeave 8-K（Meta 扩大至 ~$21B、至 2032-12、含 Vera Rubin，2026-03）"
[28]: https://investors.coreweave.com/news/news-details/2026/Jane-Street-Signs-6-Billion-AI-Cloud-Agreement-With-CoreWeave/default.aspx "CoreWeave 官方：Jane Street $6B（2026-04，含 Vera Rubin）"
[29]: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000191/crwv-20260422.htm "CoreWeave 8-K（Jane Street 历史付款：2025 ~$100M、2026Q1 ~$220.6M）"
[30]: https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm "CoreWeave 8-K（NVIDIA $6.3B order form 至 2032-04，unsold capacity backstop）"
[31]: https://www.theinformation.com/briefings/microsoft-plans-to-spend-10-billion-on-coreweave-servers-through-2030 "The Information：Microsoft 2023–2030 拟付 CoreWeave ~$10B（媒体报道，非 SEC 披露）"
[32]: https://www.marketscreener.com/news/coreweave-second-quarter-2026-q2a-26-earnings-presentation-ce7859dbdf80f520 "CoreWeave Q2 2026 Earnings Presentation（backlog $104.2B、确认节奏、Q3 新增 >$25B）"
[33]: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm "CoreWeave 10-K（committed 加权平均期限 ~5 年、客户预付 TCV 15–25%、Microsoft RPO 涂黑）"
[34]: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm "CoreWeave 10-Q 2026Q2（98% 收入来自 committed contracts）"
[35]: https://earningsapi.io/transcripts/iren-limited_iren_earnings_call_transcript_2026-08-27 "IREN FY26 电话会（2026-08-27：新签 3 年合同 >$20M/MW、3 年价 +125%/5 年 +70% vs 2025-11、GPU ~2 年回本）"
