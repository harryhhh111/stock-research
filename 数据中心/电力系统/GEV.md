# GE Vernova（GEV）研究笔记

> 2026-08-31 按 stock-research SOP 整理；2026-09-01 应要求将 Power / Electrification 两个拆解模块合并回本文件。
> 行情数据截止 2026-08-31（$898.53，市值 ~$239B，stock_data 库口径）；财务数据截止 2026 Q2（2026-07-22 披露）。

## 目录

- 1. 公司概览
- 2. 业务模块一：Power（燃气轮机）
- 3. 业务模块二：Electrification（电网设备）
- 4. 业务模块三：Wind（简述）
- 5. 营收情况
- 6. 盈利与负债
- 7. 订单与客户承诺（重点模块）
- 8. 竞争对手
- 9. 估值（Reverse DCF 速写）
- 10. 我的看法（修订版）
- 11. 跳过的模块及原因
- 12. 后续研究方向
- 13. 数据来源与核实记录

---

## 1. 公司概览

GE Vernova（NYSE: GEV）一句话理解：

> **从原通用电气 GE 拆出来的"发电设备 + 电网设备 + 风电设备"巨头。**

它不是发电厂运营商，不靠卖电赚钱。它赚的是：**卖发电设备、卖输配电设备、建设电力系统，以及对这些设备做几十年的维护服务**。2024-04-02 从 GE 独立上市，约 8.5 万员工，其设备参与生产全球约 **25% 的电力**。([GE Vernova][1])

业务地图：

```text
                GE Vernova
         ┌──────────┴──────────┐
         │                     │
     发电 Power             电网 Electrification
         │                     │
   ┌─────┼─────┐        ┌──────┼────────┐
 燃气   核电   水电     变压器  输电/变电站  软件
         │                     │
         └──────── 电 ──────────┘
                         │
                  数据中心 / 城市
   （旁边：Wind 风机，同样接入 Electrification 电网）
```

**它同时卡住了"发电"和"输电"两个环节**——这是理解这家公司的钥匙。注意：GEV 不是新能源公司，真正赚钱的核心是**天然气发电 + 电网基础设施**，风电目前亏损。

---

## 2. 业务模块一：Power（燃气轮机）

Power 分部 = **Gas Power（燃机+服务）+ 核电（含 SMR）+ 水电 + 蒸汽轮机**，Gas Power 是绝对主体。模式像航空发动机公司：

> **卖燃机 → 装机 → 之后几十年卖检修/换件/升级服务（LTSA）。**

全球 installed base 约 **7,000 台燃机**，按 MW 计全球最大——这个存量就是服务现金流的底盘，公司整体 backlog 里超 55% 是服务业务。([GE Vernova IR][5])

### 2.1 产品线：规格与参数

燃机分**重型（heavy duty）**和**航改（aeroderivative）**两类；重型按技术分代：**H 级（旗舰）> F 级（主力存量）> E 级（老机型）**。

H 级（当前接单主力）：

| 型号 | 简单循环出力 | 简单循环效率 | 联合循环效率 | 备注 |
|---|---:|---:|---:|---|
| **9HA.01**（50Hz） | 448 MW | 42.9% | >64% | |
| **9HA.02**（50Hz） | **571 MW** | 44.0% | >64%（世界纪录 63.08% 毛效率） | 爬坡 88 MW/min，热态启动 23 分钟 |
| **7HA.01 / .02 / .03**（60Hz，美日韩） | 290 / 384 / **430 MW** | — | >64% | 7HA.03 是美国市场主推机型 |

([GE Vernova 规格页][10])

要点：

- **"9 系 = 50Hz（欧亚非），7 系 = 60Hz（美日韩）"**——同代技术两个电网频率版本。
- **联合循环（CC）才是关键口径**：燃机排气余热再驱动蒸汽轮机，1×1 配置下 9HA.02 整厂约 **838 MW、效率 64.1%**；比同等煤电碳排放低约 60%。([厂商整理][11])
- 全部 HA 机型可掺烧 50% 氢气，有 100% 氢技术路线。
- F 级存量：9F 全球 450+ 台（40+ 国），7F 约 950 台 / ~175 GW——服务收入底盘。
- 航改机型（LM2500/LM6000/LMS100）启动 <10 分钟，是数据中心"过渡电源"热门选择。

实际项目形态：客户买的不是单台燃机而是整套 power block。例：越南 Nhon Trach 3&4（1.6 GW）= 2 个 800 MW block，每个含 1 台 9HA.02 + STF-D650 蒸汽轮机 + 发电机 + 余热锅炉 + Mark VIe 控制系统。([Turbomachinery][9])

### 2.2 一台燃机多少钱

**官方从不披露单机价格**，外部估算且口径混杂：

- **行业估算**：东财证券测算用 **~$300/kW** → 一台 571 MW 的 9HA.02 ≈ **$1.7 亿**量级。([东财证券][13])
- 二手平台 secondwatt 标 $200M–500M / 台、$700/kW【尚无法验证】——更像整厂 EPC 口径。
- **已确认的是涨价**：2026 H1 新签订单 $/kW 比 2025 Q4 高 **10–20 个百分点**。([Power Engineering 转述][14])

记法：**裸机 $300/kW 上下，整厂 $700–1000+/kW 量级**，两个口径都在涨。

### 2.3 产能与扩产

产能集中在南卡 **Greenville**（全球最大燃机制造基地 + 美洲维修中心）：

- HA 机型产量：**2025 年 37 台 → 2026 年 62 台 → 2027 年 74 台**，目标 70–80 台/年（2026 H2 起）。
- GW 口径：**2027 年起年出货 ~20 GW → 2028 年 24 GW → 2030 年 30 GW**。
- 投入：Greenville $160M+（+650 人）、Schenectady $41M；2025–2028 全公司 capex+R&D 合计 **$11B**。
- 供应链内化：**2025-03 完成收购 Woodward 燃机燃烧室部件业务**（金额未披露）。

([GE Vernova 新闻稿][15];[Manufacturing Mag][14];[Gas Turbine World][16])

**产能为什么紧**：高温合金叶片、燃烧室、整机测试台位都是瓶颈，三巨头交期普遍拉到 **5–7 年**。([Utility Dive 交叉分析][14])

---

## 3. 业务模块二：Electrification（电网设备）

一句话：**Power 把电造出来，Electrification 把电送过去、控起来。**

发电厂 → 升压 → 高压输电 → 变电站 → 降压 → 数据中心/工厂/城市，这条链上的设备和软件基本都在这里。四条业务线：

| 业务线 | 卖什么 | 说明 |
|---|---|---|
| **Power Transmission** | 电力变压器、开关设备（GIS/AIS）、断路器、互感器 | 变压器主力是 **Prolec GE**（2026 已收购剩余股权并表，2026E 贡献 ~$3.1B 营收） |
| **Grid Systems Integration** | HVDC 输电、FACTS/STATCOM、turnkey 变电站 | 整站 EPC：从设计到调试交付整个变电站 |
| **Power Conversion & Storage** | 电力电子变换、储能系统 | |
| **Grid Software（GridOS）** | 电网调度 EMS、监控、故障管理、电力市场管理 | 轻资产高毛利，"Orchestration" 叙事载体 |

数据中心语境下的典型交付物：**把数据中心接上电网的整套变电站**（如澳大利亚 hyperscale 项目：132/22kV AIS 变电站整站）。([GE Vernova Data Centers][17])

供应链特点：**变压器是瓶颈中的瓶颈**，且是系统性短缺（Wood Mackenzie Q2'25 调查口径，[POWER Magazine][24]）：

- **交期**：电力变压器平均 **128 周**（~2.5 年），GSU（发电升压变）**144 周**，部分订单 4 年；开关设备 44 周
- **需求爆炸**：GSU 需求较 2019 年 **+274%**，变电站变压器 +116%
- **涨价**：电力变压器单价较 2019 年 **+77%**，GSU +45%，配电变压器 +78–95%
- **上游卡脖子**：取向硅钢（GOES）美国仅 Cleveland-Cliffs 一家供，新产线 24–36 个月才能落地；**美国 80% 大型变压器靠进口**
- **缓解时点**：即使北美已宣布 ~$1.8B 扩产，WoodMac 预计短缺至少持续到 **2027–2028**；Hitachi Energy / Siemens Energy / GEV 三家全部 allocation 配售到 2028

GEV 对策：Prolec GE 北卡 $140M 新厂。([Transformer Technology][18])

### 3.1 为什么爆发

- **2026 H1 数据中心相关订单 >$5B，已是 2025 全年的 2 倍以上**。
- 设备 backlog：**$40.6B，同比 +69%**（含 Prolec $5B）；Q2'26 book-to-bill ≈ **1.7**。
- 涨价同样存在：Q2'26 EBITDA margin 有机 +700bps，管理层归因"量 + 生产率 + 有利价格"。
- 增量不只有数据中心：欧美电网老化改造（美国大量变压器服役超 30 年）、新能源并网（HVDC/FACTS）、印度等新兴市场扩产。([Q2'26 新闻稿][3];[GE Vernova India][19])

### 3.2 竞对分层（电网侧）

| 厂商 | 强项 | 与 GEV 的关系 |
|---|---|---|
| **Hitachi Energy** | 全球最大电网设备商，变压器/HVDC 全面 | 高压主战场最正面对手 |
| **Siemens Energy**（Grid Technologies） | HVDC、欧洲 turnkey 项目；SF6-free 差异化 | 高压/HVDC 正面对手 |
| **Eaton** | 中低压开关柜、UPS、母线——数据中心"表后"配电 | 电压等级错层，部分互补 |
| **Schneider Electric** | 中低压配电、楼宇电气 | 错层竞争 |
| **Vertiv** | 机房内电源/散热 | 不直接竞争（电网侧 vs 机房侧） |

([HDIN Research][20];[Eaton][21])

**GEV 的卡位**：北美变压器（Prolec 规模化）+ 高压输电 + GridOS 软件。与 Siemens Energy"复杂 turnkey"路线不同，GEV 走"标准化工作马产品 + Lean 降本"——这是它 margin 追赶更快的原因之一。

---

## 4. 业务模块三：Wind（简述）

不单独深挖（理由见第 11 节）。要点：陆上+海上风机，全球约 **59,000 台 / 120+ GW** 存量（美国陆上 ~35,000 台 / 80+ GW）。([GE Vernova Wind][7])

2024 年海上风机叶片制造缺陷计提 $700M，至今拖累；2026 指引营收下滑低双位数、EBITDA 亏损 ~$400M。亮点是陆上服务改善 + 海上 Dogger Bank B 推进。管理层策略是止血而非扩张。存量风机 = 潜在服务底盘，但短期内它是三块业务里最差的。([4Q'24 财报][8];[Q2'26 新闻稿][3])

---

## 5. 营收情况

分部营收 / EBITDA margin 三年序列 + 最新季度（SEC 财报口径；2026-01-01 起分部内业务单元重划，2025 有重述版，跨年比较留意口径）：

| | FY2023 | FY2024 | FY2025 | Q2'26 |
|---|---|---|---|---|
| **Power 营收** | $17.4B | $18.1B (+4%) | $19.8B | $5.5B (+14%) |
| Power margin | 9.9% | 12.5% | 14.7% | **18.8%** |
| **Electrification 营收** | $6.4B | $7.6B (+18%) | $9.6B (+28%) | $3.6B (**+68%**，有机 +29%) |
| Elec. margin | 3.7% | 9.0% | 14.9% | **18.4%**（有机 +700bps） |
| **Wind 营收** | $9.8B | $9.7B (-1%) | $9.1B | $2.0B (-10%) |
| Wind margin | -10.5% | -6.1% | -6.6% | -13.6% |
| **公司营收** | $33.2B | $34.9B (+5%) | $38.1B (+9%) | $11.1B (+22%) |

([4Q'24 财报][8];[Q2'26 新闻稿][3])

读法：**Power 是利润压舱石（margin 三年 +890bps），Electrification 是增长引擎（margin 三年翻 4 倍），Wind 是出血点**。公司营收加速（+5% → +9% → 单季 +22%）由前两者驱动。Electrification GAAP +68% 里约一半来自 Prolec 并表，有机 +29% 才是内生增速，引用时要区分。

**2026 全年指引（Q2'26 上调后）**：营收 $45.5–46.5B；调整后 EBITDA margin 12–14%；FCF $11.5–12.5B（大幅上调自 $6.5–7.5B）。分部：Power 有机 +18–20% / margin 17–19%；Electrification 营收 $14.5–15B（含 Prolec ~$3.1B）/ margin 18–20%；Wind EBITDA -$400M。([Q2'26 新闻稿][3])

---

## 6. 盈利与负债

公司整体（stock_data 库口径，财年=日历年，USD）：

| FY | 营收 | 净利润 ⚠️ | CFO | FCF |
|---|---:|---:|---:|---:|
| 2022 | $29.7B | -$2.7B | -$0.1B | -$0.6B |
| 2023 | $33.2B | -$0.4B | $1.2B | $0.4B |
| 2024 | $34.9B | $1.6B | $2.6B | $1.7B |
| 2025 | $38.1B | $4.9B | $5.0B | $3.7B |
| TTM 至 26-06 | $41.4B | $9.5B | $14.1B | $12.4B |

分季度单季数据（库 `us_financial_fact_version`，YTD 已换算）：

| 季度 | 营收 | 毛利率 | 经营利润 | 净利润 |
|---|---:|---:|---:|---:|
| Q2'25 | $9.11B | 20.3% | $0.38B | $0.51B |
| Q3'25 | $9.97B | 19.0% | $0.37B | $0.45B |
| Q4'25 | $10.96B | 21.2% | $0.60B | $3.66B ⚠️ |
| Q1'26 | $9.34B | 19.1% | $0.18B | **$4.75B** ⚠️ |
| Q2'26 | **$11.10B（+22%）** | **21.3%** | $0.65B | $0.67B |

- ⚠️ **净利失真**（硬规则 7）：Q4'25/Q1'26 净利远超经营利润，主因**递延税资产估值备抵释放**（Q1'26 净利 $4.75B vs 经营利润 $0.18B）。看盈利能力用**经营利润 / 调整后 EBITDA**（Q2'26：$1.25B / margin 11.3%，有机 +340bps）。
- **现金流极强**：2026 H1 CFO $10.7B、FCF ~$10B（超 2025 全年 2.5 倍）——含大额订单定金（down payments）的营运资本红利，不可简单年化。
- **资产负债表干净**：现金 $13.1B（年内 +$4.3B），上半年已回购+分红 $3.9B（超 2025 全年）；另有资产处置回款 $1.5B。负债主要是经营性负债（合同负债随 backlog 膨胀），有息债务负担轻。
- **口径提醒**：分部 margin ≠ 全公司 margin。FY2025 三分部 EBITDA 合计 $3.74B ≈ 营收 9.8%（未扣总部费用、含 Wind 拖累）；全公司口径 Q2'26 才达 11.3%（同比 +340bps，仍是明显改善）。利润季节性下半年重于上半年（Q1'26 经营 margin ~2% → Q2'26 ~5.9%），单季与全年不能直接比。

---

## 7. 订单与客户承诺（重点模块）

2B + 长交付周期公司，订单是最硬的先行指标：

- **Backlog $176B**（Q2'26，环比 +$13B）；其中服务占 55%+，设备 backlog 定价随新签水涨船高（$/kW 环比 +10–20pp）。
- **Q2'26 订单 $24.2B，有机 +88%**：Power $16.7B（+134%）/ Electrification $6.3B（+66%，book-to-bill 1.7）/ Wind $1.2B（-40%）。
- **燃机 116 GW** = 53 GW 合同 backlog + 63 GW slot reservation；年底目标 ≥125 GW。Q2 单季新签 20 GW（18 GW 预留位 + 2 GW 订单），并把 10 GW 存量预留位转为正式订单——**预留位→订单的转化正在发生**。对应年产能 ~20 GW → 5 年产能售罄，新客户排期 2030 后。
- **客户结构变化**：燃机订单 ~20%（~20 GW）直接来自数据中心；Electrification 数据中心订单 H1'26 >$5B（2025 全年 2 倍+）。Hyperscaler 直采正在改变客户结构——公用事业开始用框架联盟（Xcel × GEV × NextEra，6 GW）对冲科技巨头抢产能。
- **含金量提示**：slot reservation 靠不可退定金锁定，转化率是 backlog 质量的关键观察点。

([Q2'26 新闻稿][3];[Manufacturing Mag][14])

### 供需结论：不是紧平衡，是明确短缺（2026-09-01 补）

两条产品线都满足"短缺"的全部特征——交期、价格、backlog、扩产行为、买方行为五个维度同时印证：

| 维度 | 燃气轮机 | 大型变压器 |
|---|---|---|
| 交期 | 三巨头 5–7 年 | 128–144 周，部分 4 年 |
| 价格 | 新签 $/kW 环比 +10–20pp | 单价较 2019 +77% |
| Backlog | GEV 116 GW ≈ 5 年产能售罄 | GEV 设备 backlog +69%，book-to-bill 1.7 |
| 供给刚性 | 测试台位、高温合金叶片、燃烧室 | GOES（美国仅一家供）、绕线工位、80% 靠进口 |
| 买方行为 | 不可退定金抢 slot、 hyperscaler 加价 | 全部厂商 allocation 配售到 2028 |

**产能刚性决定短缺至少再持续 2–3 年**（变压器 WoodMac 口径缓解最早 2027–28；燃机三巨头 2028 年前产能全部售罄）。GEV 是少数两头都占的公司。

---

## 8. 竞争对手

公司层面版图（电网侧分层详见第 3.2 节）：

| 战场 | 对手 | GEV 位置 |
|---|---|---|
| 重型燃机 | Siemens Energy、Mitsubishi Power | installed base 最大（7,000 台），产能 20→30 GW |
| 电网设备（高压） | Hitachi Energy、Siemens Energy Grid Tech | 北美变压器规模领先（Prolec）+ GridOS 软件 |
| 中低压/表后配电 | Eaton、Schneider | 错层，非正面竞争 |
| 机房内电源/散热 | Vertiv | 不竞争（电网侧 vs 机房侧） |
| 风机 | Vestas、Siemens Gamesa、金风等 | 收缩止血中 |

**重型燃机三巨头**（全球最集中的设备市场之一）：

| 厂商 | 旗舰机型 | 近期动向 |
|---|---|---|
| **GE Vernova** | 9HA / 7HA | 产能 20→30 GW；Greenville 扩产 |
| **Siemens Energy** | SGT5/6-8000H、SGT-9000HL | backlog 排到 ~2030；年产量 48 → 70–80 台；美国制造投 $1B |
| **Mitsubishi Power** | M501J/M701JAC | 2026/27 交付位售罄；**2030 财年前产能翻倍**；FY2025 接单 35 台（+40%） |

第二梯队：Ansaldo（意）、BHEL（印）、东方电气/上海电气（中）、Doosan（韩）、Solar Turbines（小型机）、Baker Hughes（航改）。市占率口径：Global Energy Monitor（2022，在建电站口径）三家合计 ~2/3，亚洲在建 GEV 38%；东财证券（2026 转述）三家合计 ~85%——口径不同方向一致：**格局在向头部集中**。H/J 级效率（>64% CC）三巨头之外几乎无人能及，后进者只能吃本国保护性订单。([GEM][22];[东财证券][13])

共同点：**全行业产能售罄到 2028 年后，卖方市场，集体涨价**。GEV 相对独特的是"发电 + 输电"双卡位。

---

## 9. 估值（Reverse DCF 速写）

> 输入除股价/市值外均为**假设**，粗略量级判断，非精确模型。股价 $898.53 / 市值 ~$239B（库，2026-08-31）。

**先看价格隐含什么**（Reverse DCF 先行）：

- 2026E 调整后 EBITDA ~$6B（指引中值 $46B × 13%）→ 市值/2026E EBITDA ≈ **40x**
- 假设 WACC 9%、永续增长 3%：$239B 市值隐含稳态 FCF ≈ $239B × 6% ≈ **$14B/年**
- 对照：2026 FCF 指引 $11.5–12.5B 含定金红利不可持续；正常化 FCF（假设 EBITDA - capex - 现金税）约 $4–6B
- 乐观情形推演（假设）：2030 年营收 $70B（燃机 30 GW + Elec 翻倍 + 服务复利）× margin 18% ≈ EBITDA $12.6B → FCF ~$8–9B，**仍不及 $14B**

**结论**：当前价格隐含"2030 年后仍高增长 + margin 到 20%+"的近乎完美剧本。粗略稳态锚（$9B FCF ÷ 6% ≈ $150B）与市值偏离超 30% → **触发 caution：业务是真的好，但价格已预支多年执行**。换句话说，**买 GEV 当前价格 ≈ 买"电力设备卖方市场持续到 2030 年以后"这个判断本身**；backlog 锁定了 5 年收入下限（下行保护），但估值倍数要求增长叙事在 2030 后仍不破。本结论对假设极敏感（WACC/永续增长差 1pp 结果差很多），待正式模型。

---

## 10. 我的看法（修订版）【我的推演】

1. **GEV 是 AI 电力链上"发电 + 并网"双瓶颈的交汇点**，上市公司里几乎没有平替。研究重心放在 Power 产能爬坡和 Electrification 的 margin 兑现上，Wind 只盯止血进度。
2. **Power 的本质是"卖铲子 + 收租"**：116 GW 订单对应 5 年设备收入可见性，而每新装 1 GW 就给 7,000 台存量服务盘多加一块——存量服务才是 margin 地板的真正来源。
3. **产能是比订单更硬的约束**：37→74 台/年的爬坡曲线决定 2026–2028 营收上限；订单再多也只能排队，这是涨价能落地的原因。
4. **Electrification 是弹性最大的业务**：小基数 + margin 三年翻 4 倍 + backlog +69%；若数据中心并网持续，2028 年营收可能翻倍到 $20B+。和 Power 是同一枚硬币的两面（既要电源又要并网），这结构相对纯电网商/纯设备商独特。
5. **本轮景气的主角是"价格"不只是"量"**：产能锁死 5 年 + $/kW +10–20pp + 各分部 margin 齐涨——卖方市场的利润弹性才刚开始反映到报表。
6. **净利、FCF、分部 margin 都有口径陷阱**（税收项、定金红利、分部≠全公司、Prolec 并表 vs 有机），建模必须用经营利润/调整后 EBITDA + 正常化 FCF + 有机增速。
7. **最大长期风险是 2030 年的 30 GW 产能撞上下行周期**：若 AI 电力需求不及预期，天价 backlog（含可退性差但可转让的 slot）蒸发速度决定这是成长股还是周期股顶点。估值一节显示市场已按成长股定价。
8. 修订记录：初版（2026-08-31）暂无外部评审；待 persona 压力测试（Burry 视角：下行保护与 backlog 可取消性；Damodaran 视角：叙事→运营假设自洽性）。

## 11. 跳过的模块及原因

- **Wind 独立成篇**：跳过。收缩中的亏损业务，管理层策略是止血，第 4 节信息已足够；若陆上服务转盈或海上出清再补。
- **护城河独立篇**：跳过，壁垒分析已融入业务模块（H 级技术代际 + installed base 服务盘 / 高压认证 + 变压器产能）。
- **客户结构独立篇**：跳过，客户集中风险尚低（80% 公用事业/IPP），数据中心占比升破 30% 后再升格。
- **核电/SMR 深挖**：仅列背景（Darlington BWRX-300 已开工、美日政府 MoU 最高 $100B），SMR 商业化在 2030 后，暂不构成估值主线。

## 12. 后续研究方向

1. 正式估值模型（分部加总：Power 服务年金 + 设备放量，Elec backlog 转化，Wind 止血路径）——坐实或推翻第 9 节的 caution
2. slot reservation 定金条款、取消条款、二级市场转售迹象——backlog 含金量
3. Power 服务经济性：LTSA 单价、续约率、单台燃机全生命周期服务收入
4. 2030 年 30 GW 产能 vs 届时需求的供需框架（对接数据中心电力需求测算）
5. Hitachi Energy / Siemens Energy 分部 margin 横向对比
6. Prolec GE 并表的完整财务影响（收购价、margin 稀释/增厚）
7. GridOS 软件收入体量与 ARR 口径（管理层未单独披露）
8. Q3'26（2026-10 下旬）跟踪：指引兑现、slot→订单转化率、数据中心订单

## 13. 数据来源与核实记录

**来源**

1. [GE Vernova About](https://www.gevernova.com/company/about)（公司概况、25% 电力）
2. [GE Vernova 2025 Annual Report](https://www.gevernova.com/sites/default/files/gevernova_2025_annual_report.pdf)（FY2025 分部数据）
3. [GE Vernova Q2 2026 财报新闻稿（SEC 存档，2026-07-22）](https://www.sec.gov/Archives/edgar/data/1996810/000199681026000147/gevpressrelease2q26.htm)（Q2'26 分部明细、backlog $176B、指引、116 GW）
4. [Q2 2026 财报电话会纪要（Yahoo Finance）](https://finance.yahoo.com/quote/Y5C.DU/earnings/Y5C.DU-Q2-2026-earnings_call-652843.html/)（margin 归因、Q3 指引、Robotech、处置回款）
5. [GE Vernova Investor Relations](https://www.gevernova.com/investors)（installed base、服务占比）
6. [GE Vernova Electrification](https://www.gevernova.com/electrification/)
7. [GE Vernova Wind](https://www.gevernova.com/wind-power/about)（59,000 台风机）
8. [GE Vernova 4Q 2024 财报（SEC 存档）](https://www.sec.gov/Archives/edgar/data/1996810/000199681025000004/gev4q2024earningsrelease.htm)（FY2023/24 分部序列、Wind 叶片计提）
9. [Turbomachinery International, 2026-08-14](https://www.turbomachinerymag.com/view/ge-vernova-starts-first-ha-class-power-plant-in-vietnam-with-9ha-02-turbines)（Nhon Trach power block 配置、AGP 升级）
10. [GE Vernova 9HA 规格页](https://www.gevernova.com/gas-power/products/gas-turbines/9ha)（448/571 MW、效率、爬坡）
11. [厂商燃机规格整理 PDF](https://temperi-logistics.com/wp-content/uploads/2024/08/manufacturers-of-gas-turbine-units-in-the-eu-and-asia-part-1.pdf)（1×1 CC 838 MW / 64.1%）
12. [GE Vernova H-Class 页面](https://www.gevernova.com/gas-power/products/gas-turbines/h-class-gas-turbines)（7HA 三档、9F/7F 存量）
13. [东方财富证券研报转述（Futu, 2026-04-01）](https://news.futunn.com/en/post/70951436/east-money-securities-the-ai-wave-is-driving-a-surge)（$300/kW 估算、三巨头 85%、售后市场 $44.5B）
14. [Manufacturing Mag, 2026-06-06](https://www.manufacturingmag.com/article/ge-vernova-gas-turbine-backlog-2030-data-centers-outbid-utilities)（100 GW 合同、+10–20pp 涨价、80/20 客户结构、37→62→74 台、交期 5–7 年、Xcel 联盟）
15. [GE Vernova 新闻稿, 2025-03-06](https://www.gevernova.com/news/press-releases/ge-vernova-h-class-gas-turbine-fleet-accumulates-three-million-operating-hours)（70–80 台/年、20 GW/年、Greenville $160M）
16. [Gas Turbine World, 2026-05-28](https://gasturbineworld.com/ge-vernova-announces-a-very-good-year-led-by-booming-gas-turbine-sales-and-grid-modernization/)（沙特 $14B、backlog $150B、$11B capex+R&D、SMR MoU）
17. [GE Vernova Data Centers 行业页](https://www.gevernova.com/electrification/industries/data-centers)（变电站交付案例）
18. [Transformer Technology, 2025-10-31](https://transformer-technology.com/u-s-transformer-market-to-hit-1-49b-by-2030-amid-grid-modernization-transformer-technology-news/)（变压器交期 4 年、Prolec 北卡厂）
19. [GE Vernova 印度扩产新闻](https://general.energy/en/news/ge-vernova-to-invest-16-million-to-expand-grid-technology-manufacturing-in-india/)（HVDC/FACTS 产线）
20. [HDIN Research, 2026-02](https://www.hdinresearch.com/news/804)（GEV vs Siemens Energy 战略对比）
21. [Eaton × Siemens Energy 数据中心合作, 2025-06](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2025/eaton-and-siemens-energy-join-forces-to-provide-power-and-technology.html)
22. [Global Energy Monitor, 2022-10-14](https://globalenergymonitor.org/research/leading-three-manufacturers-providing-two-thirds-turbines-gas-fired-power-plants-under)（在建口径市占率）
23. [GE Vernova / Woodward 收购新闻稿](https://www.gevernova.com/news/press-releases/ge-vernova-completes-acquisition-gas-turbine-combustion-parts-business-woodward-inc)（2025-03-03 完成）
24. [POWER Magazine, 2026-01-02](https://www.powermag.com/transformers-in-2026-shortage-scramble-or-self-inflicted-crisis/)（WoodMac Q2'25 调查：变压器交期 128/144 周、涨价 77%、GOES 瓶颈、短缺持续至 2027–28）

**核实记录**

- 2026-08-29：初版笔记（ChatGPT 整理口径）。
- 2026-08-31：按 SOP 重组并补全：公司级财务取 stock_data 库（库口径为准，`us_financial_current_annual/ttm`、`us_financial_fact_version` 季度换算）；分部三年序列与 Q2'26 明细取 SEC 存档财报（S 级）；股价/市值取库（2026-08-27）。查明净利畸高为递延税备抵释放；分部 2026 年起有重划口径差异，已注明。单机价格为外部估算（非官方披露），secondwatt 口径标【尚无法验证】。估值为 Reverse DCF 速写，假设显式标记，偏离 >30% 触发 caution。
- 2026-08-31：Deal Radar 排查（截止 2026-08-31）——已完成/进行中：Woodward 燃烧部件收购（2025-03）、Prolec GE 剩余股权收购并表（2026）、Robotech Automation 收购（2026-07，机器人/自动化）、Darlington SMR（建设中）、美日 SMR MoU（最高 $100B 框架）、2026 年内资产处置回款 $1.5B；未检索到监管审查、激进股东介入或大股东变更。
- 2026-09-01：应用户要求将 `GEV-Power拆解.md`、`GEV-Electrification拆解.md` 合并回本文件，按「业务归业务章、数据归营收章」去重重排，来源清单合并去重。
- 2026-09-01：补变压器短缺证据（WoodMac Q2'25 调查，来源 24）；订单章新增「供需结论」小节（燃机+变压器五维短缺对照）；股价/市值更新至 2026-08-31（$898.53 / ~$239B），估值章同步改口径并补"买 GEV ≈ 买卖方市场持续到 2030+"的翻译。
