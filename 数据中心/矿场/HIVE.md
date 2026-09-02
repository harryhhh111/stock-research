# HIVE：比特币矿场 → AI 算力的转型样本

> 整理/核对日期：2026-08-28（由 5 段问答精简整合；合同口径细节与横向比较已移交 `../合同/AI算力合同.md`，本文只留指针。2026-08-28：§3 补完整推导与新维度，§5 补 Toronto 320MW，§6 补战略分叉对照）。
> 研究定位：HIVE 是"矿场转 AI"的小型样本（对照：IREN 是大型样本），核心问题是**手里的电力资产到底值多少钱**。

**一句话结论**：HIVE 账面仍是比特币矿企（FY2026 挖矿收入占 93%），但 BUZZ HPC 已签 ≈$600M TCV 合同、年化收入能力 $180M（FY2026 HPC 实际收入仅 $19.5M——一个是已确认会计收入，一个是合同年化能力，不能混）。矿场转 AI 的经济实质：**同样 1MW 稀缺电力，AI 能塞进 ~58 倍资本、产生 ~25 倍收入、38–72 倍现金利润**——但 ROIC 并未成数量级提升，矿企真正缺的是钱 + GPU + 客户合同。

## 1. 公司现状（截至 2026-08）

**两块业务**（FY2026，截至 2026-03，[1]）：

| 业务 | FY2026 营收 | 占比 |
|---|---:|---:|
| Bitcoin Mining（挖 2,885 BTC；FY2025 仅 $105.2M） | $278.3M | **~93%** |
| BUZZ HPC / AI Cloud | $19.5M | ~7% |
| **合计**（+158% YoY） | **$297.8M** | |

- 电力资产：运营容量 ~**440MW**（公司称全绿色能源），矿场在加拿大 / 瑞典 / 巴拉圭（巴拉圭 2025 扩 ~300MW）[1]
- BTC 算力：2025-03 6.5 EH/s → 2026-03 **25.1 EH/s**（一年 ~4×）[1]
- 最新季度 FY2027 Q1（至 2026-06-30，[4]）：收入 **$79.1M**（BTC $72.1M + HPC ~$7M）、Adj EBITDA $13.4M、现金 $208M——当前真实结构仍是 **Bitcoin 养 AI**
- 沿革：2017 年起挖矿，原名 HIVE Blockchain，2023 改名 HIVE Digital 并转向 HPC/AI

## 2. AI 合同（细节见 `../合同/AI算力合同.md` §1/§3）

| 签约 | 合同 | 要点 |
|---|---|---|
| 2026-02 | B200 ×504，2 年 $30M | $2.90/GPU·h（公司直接披露），2026-05 已上线 |
| 2026-06 | **GB200 NVL72 ×32 柜**，3 年 ~$220M | ≈$2.29M/柜/年；Cohere 使用，放 Bell Merritt 机房 |
| 2026-08 | **GB300 NVL72 ×28 柜**，5 年 $350M | ≈$2.50M/柜/年；CapEx $185M（$6.61M/柜）+ $35M deposit；Q4 2026 部署 |
| 2026-06 | Boden colo LOI（~25MW IT） | $1.80M/MW/年，⚠️ non-binding，不算 backlog |

- **最该盯的数**：GPU Cloud 年化收入 **≈$180M** = $35M 已上线 + $145M contracted（Q4 2026 上线）[3]
- 模式注意：HIVE 的 GPU 放在 **Bell 的机房**（asset-light，租金含 colo 费），不是"矿场改 AI 数据中心"放自己家里——它是 GPU 资产所有者 + 运营商 + 集成商。推论：Cohere 的 GB200 那单**根本没有占用 HIVE 自有矿场的电力** [12]

## 3. 每 MW 经济账：Bitcoin vs GB300（本文核心）

口径：**同样 1MW IT、土地/电网已接通**；BTC 只买 ASIC，AI = 矿场改造 + GPU 集群；项目层面现金，不含融资/税。

| 每 1MW IT | Bitcoin Mining | GB300 AI |
|---|---:|---:|
| 设备投入 | **~$0.93M**（S21+ Hydro：15 J/TH × $14/TH，[5]） | **~$48.9M**（$185M÷3.78MW，[3]） |
| 矿场→AI 改造 | — | **~$4.9M**（Toronto 案例，见下） |
| **合计投入** | **~$0.93M** | **~$53.8M** |
| 年收入 | ~$0.75M（24 EH/s×16.1 J/TH≈386MW，季度收入年化，[4]） | ~$18.5M |
| 年直接运营成本 | ~$0.53M（电费 $0.475M + 其他 $0.053M） | ~$2.8M（IREN 式自持 85% margin）–10.3M（HIVE 当前 HPC 44.3% 毛利率保守外推） |
| **年现金利润** | **~$0.22M** | **~$8.2–15.7M** |
| 现金收益率 | ~23% | ~15–29% |
| 静态回本 | ~4.3 年 | ~3.4–6.6 年 |
| 收入/设备 CapEx（粗指标） | **~80%/年** | **~38%/年** |
| 5 年收入可锁定性 | **无合同**，随币价/难度波动 | **≈$92.6M/MW**（5 年 take-or-pay 锁定） |

### 推导底稿（BTC 侧，Q1 FY2027 实测，[4]）

- 平均算力 **24.0 EH/s** × 调整后 fleet efficiency **16.1 J/TH** ≈ **386MW** ASIC IT load
- 季度收入 $72.06M → 年化 ÷386MW = **$0.746M/MW/年**
- 季度 Mining O&M $51.0M，其中**电费 $45.9M** → $0.475M/MW/年；其他运维 $5.1M → $0.053M/MW/年；合计 **$0.528M/MW/年**
- 现金毛利 = 0.746 − 0.528 = **$0.218M/MW/年** → 收益率 0.218/0.93 ≈ **23.4%**、静态回本 **4.3 年**
- 当季环境：BTC 均价 ~**$71,682**、网络难度 ~**134.7T**、mining margin **29%**——静态数字对这个环境敏感
- ASIC 投入：S21+ Hydro 15 J/TH → 1MW 跑 66,667 TH/s × $14/TH = **$0.93M/MW**（不含土地/变电站/厂房）[5]

**交叉验证（两条独立路径核对 $0.75M/MW 收入）**：

- **自底向上（不看 HIVE 财报）**：难度 134.7T → 全网算力 = 134.7×10¹² × 2³² ÷ 600s ≈ **964 EH/s**；2024 减半后日产出 = 144 块 × 3.125 BTC = **450 BTC/天**；1MW = 62.1 PH/s 占全网 0.0064% → 0.029 BTC/天 → 10.6 BTC/年 × $71,682 ≈ **$0.76M/MW/年** ✅ 与财报口径 $0.746M 仅差 ~1.6%（差额 = 手续费收入 + 季内算力/难度波动）。隐含 hashprice ≈ **$33/PH/s/天**
- **隐含电价 sanity check**：$0.475M/年 ÷ 8,760 MWh = **$54/MWh ≈ 5.4¢/kWh**，处于巴拉圭水电（~3–4¢）与加拿大/瑞典（~4–5¢+）的合理混合区间 ✅

**币价敏感性公式**：`挖矿利润(P) = 0.746 × (P ÷ 71,682) − 0.528`（$/M$·MW·年）。假设：收入随币价线性缩放、电费/运维固定——两个假设都只是短期近似，**币价大涨会吸引算力涌入推高难度，实际收入弹性 < 1**（难度内生性）。挖矿现金盈亏平衡 ≈ **$51k**（难度不变前提下）。

> 注：若按 **16.5 J/TH** 当前舰队口径（60.6 PH/s/MW），则挖矿侧为投入 $0.85M / 收入 $0.73M / 毛利 $0.21M——与主表差异 ±7% 以内，**结论不变**。

### 推导底稿（AI 侧，HIVE 2026-08 GB300 合同，[3]）

- 28 柜 × 135kW（NVIDIA designed rack power，[13]）= **3.78MW**
- CapEx $185M ÷ 3.78MW = **$48.9M/MW**（$185M 含 accelerated computing cluster + associated hardware + service warranties）
- ARR $70M ÷ 3.78MW = **$18.5M/MW/年**；5 年累计 **≈$92.6M/MW**
- 改造：Toronto 7.2MW 设施（收购后原拟先放 ~5MW 老 ASIC 挖矿）升级 Tier III 预计花 **$35M → ~$4.9M/MW**；⚠️ 单一案例，不同厂房差异大，不可外推
- 运营成本两锚：
  - **乐观锚** = IREN×Microsoft 项目 EBITDA margin 85%（直接成本 ~15%，已扣电费/维保/机房运营）→ 成本 $2.78M、利润 **$15.7M/MW/年** → 收益率 29.3%、回本 3.4 年
  - **保守锚** = HIVE 当前 HPC 毛利率 **44.3%**（收入 $7.06M − O&M $2.877M − marketplace 服务费 $1.055M = 毛利 $3.128M，[4]）→ 利润 **$8.2M/MW/年** → 收益率 15.2%、回本 6.6 年——但 44.3% 混了老 GPU/marketplace/第三方机房，对"专用 GB300 集群 + investment-grade 客户 + 5 年锁定"明显偏保守

### 换算成 100MW 已接电矿场

| 100MW | 继续挖矿 | 全改 GB300 AI |
|---|---:|---:|
| 投入 | ~$93M（ASIC） | **~$4.89B（GPU）+ 数亿改造 ≈ $5.4B** |
| 年收入 | ~$75M | **~$1.85B**（按 2026-08 合同价全部卖出） |
| 年现金利润 | ~$22M（无合同保障） | **~$8.2–15.7 亿** |
| 5 年收入 | 无法锁定 | **~$9.26B 合同锁定** |

### BTC 平价分析：什么价格下挖矿和 AI 收益一致（2026-08-29 补）

用上面的敏感性公式 `利润(P) = 0.746 × (P ÷ 71,682) − 0.528` 求解，**"收益一致"有两个定义，答案完全不同**：

**定义 A：每 MW 绝对现金利润一致**（密度平价，与 CapEx 无关）

| AI 侧口径 | 平价 BTC 价格 | vs 当前 $79.7k（2026-08-28） |
|---|---:|---|
| 保守（$8.2M/MW/年） | **≈ $84 万** | ~10.5× |
| 乐观（$15.7M/MW/年） | **≈ $156 万** | ~19.6× |

⚠️ 因**难度内生性**（币价涨 → 算力涌入 → 难度上调 → hashprice 均值回归），这个价格实际上永远达不到——挖矿的低利润密度是结构性的，不是靠牛市能追平的。

**定义 B：现金收益率一致**（利润 ÷ CapEx）

| 口径 | AI 收益率目标 | 平价 BTC 价格 |
|---|---|---:|
| 全口径（AI 含改造 $53.8M → 15.2–29.3%） | 15.2% / 29.3% | **$64k – $77k** |
| 设备口径（AI 只算 GPU $48.9M → 16.8–32.2%；挖矿只算 ASIC $0.93M） | 16.8% / 32.2% | **$66k – $79.5k** |

即：**当前 BTC ≈ $79.7k 时，挖矿的设备现金收益率（~32%）恰好 ≈ AI 乐观情形——今天就站在收益率平价点上**。挖矿不缺收益率，缺的是绝对利润密度（38–72× 差距）和收入锁定（2028 减半 + 难度竞争可随时打下来；AI 侧 5 年 take-or-pay）。挖矿现金盈亏平衡 ≈ $51k（难度不变前提下）。

### 三个要点

1. **反直觉结论**：AI 的吸引力不是 ROIC 高一个数量级（23% vs 15–29%；收入/设备 CapEx 粗指标甚至 ASIC 更高：~80% vs ~38%，BTC 牛市时挖矿短期 ROIC 可以更高），而是**同样 1MW 电力能塞进 ~58 倍资本**，把 $0.22M/MW/年的现金利润放大到 $8–16M/MW/年（38–72×；收入 ~25×）
2. **BTC 的致命弱点**：$0.22M 没有任何合同保障——mining margin 近几季度在 49%→35%→24%→29% 剧烈波动 [4]；BTC 跌、全网算力涨、halving 都会直接改变它。AI 侧是 5 年 take-or-pay 锁定
3. **矿企真正缺的不是电**：对 IREN/HIVE 这种已控制大量 MW 又能拿到几十亿融资的公司，缺的是**钱 + GPU + 客户合同**。这也解释了为什么没有客户就不会一口气拆矿机——**先拿 Microsoft/Cohere 级 3–5 年合同，再砸几十亿买 GPU，经济逻辑才成立**

## 4. 矿场 ≠ AI 数据中心（能继承什么、要重做什么）

**五个不可直接复用的原因**：

1. **功率密度**：矿场是大量 ASIC 分散铺开；GB300 NVL72 单柜 ~135kW，原配电/母线/PDU 扛不住
2. **冷却**：矿场风冷为主；NVL72 必须 direct-to-chip 液冷（CDU/管路/冗余）
3. **可靠性**：矿机掉一批只是少挖点；几万卡训练要求 Tier III 级冗余供电/UPS/监控
4. **网络**：挖矿对外网需求极低；AI 集群要 InfiniBand 互联 + 大量光纤（Grand Falls 专门签 100/400Gbps 光纤合同，[6]）
5. **GPU 成本**：1MW ASIC ~$0.93M vs 1MW GB300 集群 ~$49M——不是"换机器"，是"再融资 ~$50M/MW 买全套设备 + 改造机房"

**矿场真正值钱的是"壳"**：

- 可继承：土地 + 电网排队权 + 变电站 + 已接通的 MW + 部分建筑
- 必须重做：高密度配电 + 液冷 + UPS/冗余 + 光纤 + IB/以太网 + 存储 + GPU 服务器

> 护城河表述：不是"矿场可以直接变 AI 数据中心"，而是**"别人拿 200MW 电力要排队几年，我手里的今天已经通电，只需改造后半段"**。案例：Grand Falls 70MW 已通电矿场 → 改 ~50MW Tier III+ AI Factory（利用现有建筑和核心电气，非推倒重建）[6]。
>
> 推论：**客户合同必须先签**——没有 Microsoft/Cohere 这种 3–5 年合同，矿企不敢先砸几十亿把几百 MW 改成 GPU。

## 5. 转型时间线与分场地现状（2025 → 2026）

HIVE 的转型**不是一次性动作**，而是持续约两年的资产重新配置，容易把"矿机迁移"和"矿场转 AI"误读成同一件事——实际是两个不同时间、不同设备、不同地点的动作：

**三步过程**：

1. **挖矿重心移往巴拉圭（2025）**：新建/扩 ~300MW 水电矿场 + 大量采购新 ASIC + 重新部署部分旧设备。2025-04 披露将一批 BuzzMiners 从瑞典迁往巴拉圭；但瑞典空出的位置当时又补入了 Iceland 退役设备和新一代 Canaan 矿机——**2025 年当时的动作是优化全球矿机部署，不是"瑞典矿场立刻转 AI"**。最终算力 6.5 → 25 EH/s [7]
2. **加拿大/瑞典老矿场逐步腾出电力（2025 下半年起）**：2025 年晚些时候 Grand Falls 仍是 70MW Bitcoin 矿场在满负荷供电 [8]
3. **老矿场改造转 AI（2026）**：不是原样塞 GPU，而是做 Tier III / 液冷 / 网络改造（见 §4）

公司自己的战略表述：**Paraguay 扩张 Bitcoin mining，Bitcoin 产生的现金流再投入加拿大 Tier III+ AI 数据中心转型** [10]。

**分场地现状**（截至 2026-08）：

| 地点 | 原来 | 现在/计划 | 状态 |
|---|---|---|---|
| **Grand Falls，加拿大 70MW** | Bitcoin mining | 改 ~50MW Tier III+ AI Factory | **正在改，未完工**（光纤 2026 Q3 起交付）[6][9] |
| **Boden，瑞典 32MW** | GPU/ASIC 挖矿 | ~25MW AI/HPC | **逐步退出 ASIC**（"progressively phasing down ASIC-based hashrate production"）、推进改造；2026-06 签 25MW colo LOI（最长 10 年、支持 ~10,000 GB300、需液冷改造）[9] |
| **Lachute，加拿大 30MW** | Bitcoin mining | 仍为 Bitcoin mining | 未改 |
| **Paraguay 300MW+** | 新建/收购扩建 | Bitcoin mining | 主要是**新增**挖矿基地，非"旧矿机搬过去" |
| **Greater Toronto 320MW** | —（新增电力） | **全新 AI 基础设施项目**（320MW utility，支持 100,000+ GPU） | 规划中，**不是矿场改造** [11] |

两个表述纪律：

- **不能说"Grand Falls 的矿机全部搬去了 Paraguay"**——HIVE 未披露原场地 ASIC 的逐台去向（卖掉/退役/搬迁不明）
- **不能说"矿场已全部改完"**——Grand Falls 的准确状态是：70MW 矿场真实存在过 → 现在真在改 AI → 50MW AI facility 仍处于建设/改造中，三个阶段都真实存在

## 6. HIVE vs IREN：战略已经分叉

| | HIVE | IREN |
|---|---|---|
| 起家 / 核心资产 | Bitcoin Mining / 电力+数据中心 | 同左 |
| AI 客户 | Bell/Cohere + 匿名企业 | Microsoft、NVIDIA |
| 机房 | **租 Bell（asset-light）** | **自持** |
| 规模 | 小（440MW 运营） | 大（Childress 750MW 等） |
| **Bitcoin 最终方向** | **继续保留**（Paraguay 甚至还在扩张） | **正在退出**（2026 年底基本拆完） |
| **AI 容量来源** | 部分老矿场转换 + **Toronto 320MW 新增电力** | 大量转换（Childress/Canal Flats/Prince George/Mackenzie）+ 大量新建（Horizon、Sweetwater） |

一句话概括分叉：

- **IREN**："AI 的 MW 价值高得多，那就拆矿机，电力全部往 AI 转"——`Bitcoin → AI`，老矿场能改尽改
- **HIVE**："靠近 AI 客户的加拿大/欧洲电力做 AI，极便宜的 Paraguay 电力继续挖"——**电力资产重新分工**：加拿大/瑞典 `Bitcoin → AI`，Paraguay `Bitcoin → Bitcoin`，Toronto `新增电力 → AI`

共同投资逻辑：市场原按"比特币矿企"估值，若电力资源能转成 AI 算力，**单位 MW 的资产价值发生数量级重估**（见 §3 的 38–72×）。

> ⚠️ **宏观口径提醒**（对 2026/2027 AI 新增 GW 统计重要）：IREN/HIVE 官宣的 AI MW **不能全部算作全球新增数据中心电力需求**——其中一部分只是"原来挖 Bitcoin 的 1MW → 现在跑 AI 的 1MW"，对电网新增负荷几乎为零；但对 NVIDIA、液冷、电气、网络设备等 AI 产业链来说，仍是**一整套全新的设备需求**。两个口径要分开记。

三阶段：① Bitcoin miner → ② Bitcoin + GPU Cloud（当前）→ ③ AI infrastructure 为核心、挖矿作现金流与电力资产基础；**2026 可能就是转折点**（4,320 张新一代 Blackwell、~$570M TCV 已签，不再是实验性质）——但注意 HIVE 的终点和 IREN 不同：HIVE 没有说要退出挖矿。

[1]: https://www.hivedigitaltechnologies.com/news/hive-achieves-fy2026-total-revenue-of-2978-million-158-yoy-hives-buzz-hpc-positioned-for-growth/ "HIVE FY2026 业绩（$297.8M +158%、挖矿 $278.3M、HPC $19.5M、440MW、25.1 EH/s）"
[2]: https://www.hivedigitaltechnologies.com/news/hives-buzz-hpc-closes-usd-220-million-sovereign-ai-gpu-contract-with-bell-ai-fabric-for-cohere-inc/ "HIVE's BUZZ Closes $220M Sovereign AI GPU Contract with Bell for Cohere（2026-06-18）"
[3]: https://www.hivedigitaltechnologies.com/static/hivesite/filings/000106299326004522/form8k.htm "HIVE 8-K（$350M 合同：2,016 GB300、28 NVL72、CapEx $185M 含 cluster+硬件+质保、$35M deposit、Q4 2026 部署、$180M 年化口径）"
[4]: https://www.hivedigitaltechnologies.com/static/hivesite/filings/000106299326004434/form10q.htm "HIVE 10-Q FY2027 Q1（收入 $79.1M、24.0 EH/s、16.1 J/TH、电费 $45.9M、BTC 均价 $71,682、难度 134.7T、HPC 毛利 $3.128M/44.3%、mining margin 波动）"
[5]: https://www.hivedigitaltechnologies.com/news/hive-announces-transformative-acquisition-of-86-ehs-of-bitmain-s21-hydro-chips-projecting-15-ehs-by-summer-2025-driving-300-million-revenue-and-2-of-global-bitcoin-mining-network/ "HIVE S21+ Hydro 采购（15 J/TH、319 TH/s、$14/TH）"
[6]: https://www.hivedigitaltechnologies.com/news/hives-buzz-starts-building-a-digital-superhighway-for-eastern-canadas-first-sovereign-ai-factory/ "HIVE Grand Falls 光纤建设（70MW→50MW Tier III+ AI Factory）"
[7]: https://www.hivedigitaltechnologies.com/static/hivesite/filings/000106299326002973/form10k.htm "HIVE 10-K（巴拉圭 ~300MW 扩建、全球矿机部署）"
[8]: https://www.hivedigitaltechnologies.com/news/hive-digital-technologies-accelerates-into-the-ai-super-cycle-by-securing-prime-land-for-next-gen-tier-iii-ai-hpc-data-centers-and-surpassing-23-ehs/ "HIVE 新闻稿（23 EH/s、Tier III+ 土地；Grand Falls 70MW 挖矿供电）"
[9]: https://www.hivedigitaltechnologies.com/news/hive-signs-long-term-hpc-colocation-loi-with-investment-grade-swedish-client-at-boden-retrofit-to-support-up-to-10000-gb300-gpus/ "HIVE Boden colo LOI（32MW 设施、25MW usable IT、最长 10 年、~10,000 GB300、液冷改造、逐步退出 ASIC）"
[10]: https://www.hivedigitaltechnologies.com/news/hive-digital-technologies-reports-october-bitcoin-production-of-289-btc-up-8-mm-and-147-yy-in-paraguay-while-fueling-canadas-tier-iii-ai-data-center-growth/ "HIVE 2025-10 产量报告（289 BTC、24 EH/s、Paraguay 扩建完成；公司口径：Bitcoin 现金流反哺加拿大 Tier III+ AI 转型）"
[11]: https://www.hivedigitaltechnologies.com/news/hives-buzz-hpc-announces-320-mw-sovereign-ai-infrastructure-in-greater-toronto-area/ "HIVE BUZZ HPC 宣布 Greater Toronto 320MW Sovereign AI 基础设施（新增电力、100,000+ GPU）"
[12]: https://www.hivedigitaltechnologies.com/static/hivesite/filings/000106299326003293/form8k.htm "HIVE 8-K（Cohere GB200 部署于 Bell Merritt purpose-built facility，未占用 HIVE 自有矿场电力）"
[13]: https://docs.nvidia.com/mission-control/docs/systems-administration-guide/2.3.0/prs/faq.html "NVIDIA Mission Control FAQ（GB300 NVL72 designed rack power 135kW → 7.41 柜/MW）"
