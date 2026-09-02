# AI 总账 —— 需求端到底有多少钱，是不是泡沫

> 整理日期：2026-08-31 ｜ 状态：v1.3（2026-08-31 对账 #2：NVDA FY27Q2 落数、Anthropic $65B Reuters 锚点、PORTS-Pike 担保入 SEC 文件、Google-Marvell 权证与 Broadcom 举债登记）
>
> **目的**：把散落各处的证据（财报、合同公告、融资新闻、媒体报道）整理成一笔可交叉验证的账，回答三个问题：
> 1. 大公司每天在 AI 上花多少钱？（基建支出）
> 2. 终端客户为 AI 付了多少钱？（真实需求）
> 3. 两者之间的缺口靠债务、循环交易撑了多大？（泡沫程度）
>
> **与 `AI 产业链.md` 的分工**：产业链管供给侧瓶颈（电力/HBM/CoWoS 产能），总账管需求侧对账（谁在花钱、钱从哪来、谁在付钱）。两份文档互相引用，不重复登记。

---

## 0.0 口径门禁（先过门禁，再算比率）

这不是把所有 AI 新闻数字加总的表，而是追踪**资产建设、算力需求、供给收入、终端货币化与融资**是否逐步脱钩的仪表盘。五本账之间允许勾稽，不允许直接相加：

| 账本 | 记录对象 | 不可与什么直接相加 | 用途 |
|---|---|---|---|
| 资产建设账（台账 A） | 现金 CapEx、融资租赁、土建/电力/GPU 等资产投入 | 供应商收入、订单面值 | 看建设速度与资产所有权 |
| 算力需求账（§4 合同） | MW/GPU、合同期、预付款、实际利用率 | CapEx、backlog 面值 | 看客户实际需要多少算力 |
| 供给收入账（台账 B） | 芯片、服务器、电力、云服务各层的已确认收入 | 跨层供应商收入 | 看产业链兑现；NVDA→云厂→CSP 的同一条链不得累计 |
| 终端货币化账（台账 C） | 最终外部客户支付的 API、订阅、软件溢价收入 | 云厂对模型公司的中间收入 | 观察可验证的需求下限 |
| 融资与关联交易账（§5） | 股权、债务、预付款、权证、担保、take-or-pay | 当期收入或订单面值 | 判断融资缺口与需求自发性 |

**一笔交易的最小登记字段**：交易 ID、公告/签约/交付日期、最终需求方、直接付款方、资产所有者、供应商、金额类型（现金/指引/合同面值/权证公允价值/担保上限）、合同期、履约状态、来源链接与证据等级、关联交易 ID。没有这些字段的数字只能留在“线索池”，不得进入正式合计。

**计算门禁**：

1. 正式比率只用同一期间、同一币种、同一经济层级的已确认流量；实际值、推导值、公司指引和媒体转引不得混算。
2. 同一最终需求的芯片销售、云租赁和软件/API 收入只能分别展示，不能相加成“AI 收入”。
3. 未签最终协议、未履约合同、权证名义股数和融资平台目标规模，不进入正式分子；可在“上行情景/压力情景”单列。
4. CSP 未拆分 AI CapEx 时，其总 CapEx 只能作为 **AI CapEx 上限代理值**，不得称为已确认 AI CapEx。

---

## 0. 三个泡沫比率（每季更新，趋势比绝对值重要）

| 比率 | 定义 | 当前值 | 上次更新 | 数据来源 |
|---|---|---|---|---|
| **R1 当期可观察货币化覆盖度** | 同期、去除中间转售后的可核实终端 AI 收入 ÷ 已确认 AI 资产投入；它不是资本回收率 | 【不计算】分子候选继续增强但仍未过证据门禁：Anthropic 7 月末 run-rate $65B（Reuters 转引）、OpenAI 8 月 >$40B（CNBC + Motley Fool 多源），媒体合并口径 >$115B（cryptobriefing）——全部停在媒体层；分母侧仍无同期间、AI 拆分的已确认资产投入（Big-5 总 CapEx 上限代理值口径不变） | 2026-08-31 | 台账 A、C；满足门禁后再计算 |
| **R2 关联融资暴露率** | 当期已发生的供应商现金投资 + 权证/担保当期公允价值 + 已承担融资敞口 ÷ 同期、受该结构推动的已确认相关收入 | 【不计算】重要进展：8/26 NVDA 10-Q/CFO Commentary 出现**首个报表级关联担保披露**（PORTS-Pike ≤$105B，见 §5）——从 MoU/公告层进入 SEC 文件层；但担保的现金/收入确认期间仍未对齐，且 Google-Marvell 权证公允价值未披露，维持不计算 | 2026-08-31 | §5；需补现金支付、会计确认与关联收入归属 |
| **R3 外部融资缺口率** | （CapEx − OCF − 客户预付款 − 资产出售回款）÷ CapEx，并另列净举债、股权融资与融资租赁填补比例 | 【分组件证据，未合成单值】买家侧无新入库财报（库 8/19 后无新行），AMZN/GOOGL 缺口与 MSFT 覆盖结论沿用 8/20；**杠杆信号扩散到供给方**：Broadcom 拟举债 >$60B（含次级或达 $100B）为 Anthropic 等定制芯片产能融资（Bloomberg 8/21 🟡）；Nebius 7 月举债 $775M（SOFR+250bp）🟡 | 2026-08-31 | stock_data 库 + 10-Q/10-K 现金流、债务、租赁与融资科目；媒体转引单列 |

**对标基准**：1999–2001 电信光纤泡沫中，R3（vendor financing + 债务）先于 R1 恶化。观察顺序：R3 先抬头 → R2 扩大 → R1 迟迟收不回来 = 危险信号序列。
**2026-08-31 观察（暂定）**：本周三个结构性动向——(1) 关联融资从公告走进 SEC 披露（PORTS-Pike ≤$105B 担保进 NVDA CFO Commentary「Guarantees」节，会计落点首次出现）；(2) 杠杆向供给方扩散（Broadcom 拟举债 $60–100B 服务特定客户产能）；(3) 终端货币化媒体轨迹继续上行（Anthropic $65B / OpenAI >$40B，合计 >$115B）但仍无审计落点。R1/R2/R3 裁定状态不变：均未过门禁，不计算正式值。

---

## 1. 台账 A：基建买家（钱花出去的一侧）

> 口径纪律：CapEx 用公司财报口径（cash paid for PP&E 或管理层指引，需注明哪种）；"AI 相关"若公司未单独披露，用标注 🟡 的估计值。未披露 AI 拆分前，本表所有 CSP CapEx 都是总 CapEx 或上限代理，不能直接合计为 AI 投入。

| 买家 | 最新披露期 | CapEx（当期） | AI 相关口径 | 裁员/收缩背景 | 来源 |
|---|---|---|---|---|---|
| Microsoft | FY2026（止 2026-06-30） | **FY26 全年 $115.95B ✅库**；FY26Q4 单季 $35.8B ✅库（全年累计 − 前三季 $80.15B 推算；逐季 $19.4B→$29.9B→$30.9B→$35.8B 加速）。CY2026 市场跟踪 ~$190B 🟡 | 未细分；企业 AI 年运行率 >$37B 🟡（见台账 C） | **关键证据落地**：多轮裁员后 CapEx 仍在加速 ✅；FCF 同比 -23% 🟡；数据中心折旧年限 15→25 年（利润美化口径）🟡；Guardian 据内部文件称已装 AI 芯片 ~220 万颗、低于按电力容量的推算值，MSFT 否认其假设 🟡；Azure 北弗吉尼亚/得州因电网限容、报道称有 GPU 闲置仓库（呼应 Guardian）🟡 | stock_data 库（2026-08-20 取数）；financebuzz 2026-08-18；datagravity 2026-08-19；Guardian 2026-08-17（aidapted 转引）；arlobriefing 2026-08-27 |
| Google | 2026Q2 | **Q2 单季 $44.93B ✅库**（H1 $80.60B − Q1 $35.67B）；FY2025 实际 $91.45B ✅库；2026 指引两次上调至 $195–205B 🟡 | 未细分 CapEx；需求侧证据：Google Cloud Q2'26 收入 +82% YoY、cloud backlog >$514B（Q2 财报 7/22）🟡；CFO Ashkenazi 称 Q3 用第三方容量过桥 🟡 | **Q2'26 FCF -$5.86B ✅库复算**（OCF $39.07B − CapEx $44.93B），媒体称「史上首个负 FCF 季度」 | stock_data 库；financebuzz/storyboard18 2026-08-18；datagravity 2026-08-19；arlobriefing 2026-08-27 |
| Amazon | 2026Q2 | **Q2 单季 $54.21B ✅库**（Q1 $44.20B；Q3'25 $35.10B，逐季陡增）；H1'26 CapEx $98.41B > OCF $71.42B ✅库；TTM CapEx $173.0B vs OCF $161.4B ✅库；2026 指引媒体口径 $200B（7 月电话会）→ $220B（8 月 CNBC TV18）并存 🟡 | 未细分 CapEx；AWS 年化收入 $150B、AI 服务 >$15B run-rate（Q1'26 口径）🟡 | TTM FCF 转负：库口径 ≈ -$11.6B ✅（媒体值 -$7.6B 🟡，差异疑为融资租赁口径，待核）；2025 年起 AI 服务器折旧年限缩短至 5 年 🟡（与 MSFT 反向——同一资产两种折旧假设，GPU fleet 经济寿命无共识） | stock_data 库；storyboard18 2026-08-18；datagravity 2026-08-19；arlobriefing 2026-08-27 |
| Meta | 2026Q1（Q2'26 库缺行） | Q1'26 $19.00B ✅库；FY2025 $69.69B ✅库；2026 指引收窄至 $130–145B 🟡 | 未细分 | 新增债务 $24.9B、连续两季暂停回购、单季 FCF 仅 $784M 🟡；El Paso $12.5B 数据中心债券 2026-07-28 定价利差高于去年可比交易（WSJ）🟡；未开始租赁义务 $347B（截至 2026-06，含 Hyperion）🟡；Hyperion 扩至 $50B/5GW（Blue Owl 80%/Meta 20% JV，表外）🟡 | stock_data 库；financebuzz 2026-08-18；marketscale 2026-08-17；WSJ 经 36kr 转引 2026-08-18；datagravity 2026-08-19 |
| Oracle | FY2026（止 2026-05-31） | **FY26 全年 $55.66B ✅库**（Q4 单季 $16.49B 推算） | Stargate $300B 级合同承接方 | — | stock_data 库（2026-08-20 取数） |
| CoreWeave | 2026Q1 / FY2026 指引 | Q1'26 收入 $2.08B、净亏 $0.74B（EPS -$1.40）✅库；FY26 CapEx 指引 $35–39B ✅公司指引（Q2'26 实际值库未入库，待对账池） | 几乎全部 | — | stock_data 库；CRWV 研究笔记 |
| Nebius | 2026Q2 | 单季 CapEx $5.7B（超预期 $4.7B）🟡；公司称 CapEx 回本周期 1 年 10 个月、半数以上费用靠客户预付款 🟡 | 全部 | 7 月举债 $775M（SOFR+250bp，依托投资级对手方合同）🟡；客户承诺口径 $40B 🟡 | siliconangle 2026-08-12；sec-api 2026-08-26 |
| OpenAI（含 Stargate） | — | 承诺口径继续扩大（全景见 C1，累计 ~$1.1T+）；实际支出【尚无法验证】 | 全部 | 佐治亚州「Project Camellia」**进展**：2026-08-26 Georgia PSC 批准 Georgia Power 供电合同——3,200MW 新负荷、OpenAI 付全额基础设施成本、承诺 ≤1,000MW 灵活需求响应（监管程序节点，非园区 FID）🟡 | 合同公告；Georgia Power/Southern 经 compute.world 转引 2026-08-26；electricchoice tracker |
| 九大 CSP 合计 | 2026 全年 | >$886.7B（+90% YoY）🟡媒体转引；四大（AMZN/GOOGL/MSFT/META）2026 指引合计 **$725–760B** 🟡（2025 实际 ~$410B，+77%）。**口径冲突备忘**：7 月末汇编口径为五大（含 ORCL）$660–700B、75%+ 投向 AI（Futurum/Goldman/公司财报，arlobriefing 8/27）——低于四家口径是因为未计入 8 月的指引上调，以旧口径存档备查 | — | — | TrendForce（infotechlead，2026-08）；storyboard18/financebuzz 2026-08-18；arlobriefing 2026-08-27 |

**这一层要盯的问题**：裁员的公司（MSFT/META/AMZN 都裁过）省下的钱是不是转手变成了 AI 采购？——这是"支出质量"问题，需逐年序列对照人力成本 vs CapEx。
**2026-08-20 进展**：CapEx 侧已确认「裁员后仍在加速」（MSFT 逐季 ✅）。新增同维度问题：**现金流转负后靠发债和表外 SPV 继续加速**——Meta 未开始租赁 $347B、九大科技公司 AI 表外承诺合计 ~$3T（未开始租赁 $1.2T + 采购承诺及其他 $1.9T，约为过去一年 CapEx $600B 的 5 倍；WSJ 分析 9 家公司申报文件，经 36kr 转引 🟡 2026-08-18）。Morgan Stanley 估 hyperscaler 2026–2028 AI 基建支出 $3.3–3.5T 🟡。
**2026-08-31 补充**：NVDA 电话会需求侧口径（🟡转引）——ACIE（neocloud/工业/企业）客户群 2026 年底装机 ~8GW（2025 底 ~3GW）；AWS 至 FY29Q2 再部署 200 万颗 GPU。第三方需求叙事（Gartner：2026 全球 AI 支出 $2.59T、+47% 🟡）继续上行，但均非终端付费证据。

---

## 2. 台账 B：供给方（钱收进来的一侧）

| 供应商 | 最新期 | 营收 | AI/DC 相关口径 | backlog / 合同负债 | 来源 |
|---|---|---|---|---|---|
| NVIDIA | **FY27Q2（止 2026-07-26，8/26 发布）** | **FY27Q2 单季 $96.22B（+106% YoY / +18% QoQ）、DC $89.0B（+117%）、GAAP 毛利率 75.0%、净利 $59.69B、EPS $2.46（GAAP）/ $2.22（non-GAAP）、FCF $21.34B** ✅财报（新闻稿 + CFO Commentary + 10-Q 多源转引一致；stock_data 库截至 8/31 未入库，入库后复核）；FY27Q3 指引 $108B ±2%（**假设中国 DC 算力收入为零**；Q2 中国 Hopper DC 出货 <1% DC 收入）；Q4 毛利率市场预期 71–72%（管理层称存储成本续涨）🟡 | **首次拆分客户结构**：Hyperscale $48.7B（+102%）vs ACIE（AI 云/工业/企业）$40.3B（+138%）；Vera Rubin 8 月初量产出货、Q3 预计占 DC ~20%；单 GW 收入口径 Hopper $18B → Blackwell $25B → Rubin $40B | **供应与产能承诺（NVDA 对上游的采购承诺，非客户 backlog）：$119B（4 月）→ $279B（7 月）** ✅财报转引；客户 backlog/合同负债仍未取 | NVDA 新闻稿/CFO Commentary/10-Q 经 odaily、sec-api、cloud.theai.com、compute.world 转引（2026-08-26~28，多源一致） |
| AMD | Q2'26（止 2026-06-27） | $11.54B（+50%）✅；净利 $2.30B ✅ | DC 分部 $6.72B（+107%）✅；Helios 早期部署方确认：Azure / Meta / OpenAI / Oracle 🟡；AMD 宣称 tokens-per-dollar 较 Vera Rubin NVL72 优 30% 🟡 | OpenAI 6GW + Meta 6GW + Anthropic 2GW 长约，三家前沿实验室累计 ~14GW（见登记簿） | stock_data 库 + AMD 笔记；moorinsights 2026-08-18；ceevis 2026-08-23；arlobriefing 2026-08-27 |
| Intel | FY2025 | $52.9B ✅（营业亏损 $2.2B） | 对照组：错过 AI 的供给方长什么样 | — | stock_data 库 |
| Micron | FQ3'26（止 2026-05-28） | **FQ3 单季 $41.46B、净利 $28.24B ✅库**（FQ2 $23.86B/NI $13.79B；FQ1 $13.64B——三个季度收入 3 倍化） | HBM 超级周期的最直接实证（NVDA 称存储成本「续涨」与此互证 🟡） | — | stock_data 库（2026-08-20 取数） |
| Broadcom | FY26Q2（止 2026-05-03） | $22.19B ✅库（FY26Q1 $19.31B） | OpenAI 10GW 定制加速器承诺（2026H2 起部署至 2032；Tunguz 按 $35B/GW 行业基准估 ~$350B 🟡**测算口径非官方**） | 【待取】；**8/21 拟举债 >$60B（含次级层或达 $100B）为 Anthropic 等定制芯片产能融资**（Bloomberg，谈判中未签约，见 §5）🟡 | stock_data 库；tomtunguz 2026-08-18；Bloomberg 经 code4u 转引 2026-08-21 |
| Marvell（新增） | FY27 展望 | 公司上调 FY27 收入展望至 ~$11.5B ✅公司指引（媒体转引）；FY27Q2 指引 $2.7B ±5% 🟡 | Google 定制芯片生态扩大合作（推理加速器/存储/网络/内存接口），Google 获权证 ≤$12.2B 绑订单（见 §5）🟡 | — | Yahoo Finance 2026-08-24；Bloomberg/CNBC 经 andrew.ooo/code4u 转引 2026-08-19 |
| TSMC | — | 【待取】 | CoWoS 产能（AI 产业链.md） | — | — |
| Vertiv | 2026Q2 | **$3.27B、净利 $0.50B ✅库**（Q1'26 $2.65B） | 电力/散热基建 | — | stock_data 库（2026-08-20 取数） |
| CoreWeave | 2026Q1 | Q1'26 $2.08B ✅库；FY2025 $51.31 亿 ✅ | 全部 | $104.2B（2026Q2 末），Q3 初再 +$25B | stock_data 库；CRWV 笔记 |
| Nebius | 2026Q2 | $582.3M（+454% YoY，超预期 ~$10M）🟡 | 全部；每季 Microsoft 合同交付「按期」（sec-api 转引 🟡） | 新签 4 笔数据中心合同、单笔均值 >$1B 🟡；Meta+MSFT 存量合同上限 $46.4B 🟡；客户承诺口径 $40B 🟡 | siliconangle 2026-08-12；sec-api 2026-08-26 |

**勾稽用途**：本表按层分别观察，不做跨层收入加总。买方资产投入可与其直接采购的硬件/土建金额勾稽；GPU/服务器收入、云租赁收入、最终 API/软件收入对应同一经济链的不同层，必须通过交易 ID 去重后才可讨论覆盖关系。
**2026-08-31 注**：NVDA 首次客户结构拆分给了勾稽新锚点——DC 收入 $89B 中 hyperscale $48.7B vs neocloud/企业 $40.3B，neocloud 占比 ~45%，其中相当部分收入由供应商关联融资支撑（§5）；NVDA 自身对上游承诺 $279B 意味着其在为「需求持续」下注，该承诺若遇需求回撤即变为库存/减值风险。另：NVDA 传闻近 $12.9B 洽购 Hugging Face（donvitocodes 2026-08-29，NA 单源）——入线索池，不登记。

---

## 3. 台账 C：终端付费（真实需求锚）

> 这一层是整个对账的地基，也是数据最稀缺的一层。原则上只收"有人真金白银付费"的证据。

| 付费方 | 指标 | 数值 | 口径/日期 | 来源 | 核实状态 |
|---|---|---|---|---|---|
| OpenAI | 年化收入（run-rate） | 轨迹：$3.7B（2024 末）→ ~$20B（2025 末）→ $25B（2026 初）→ **>$40B（2026-08，CNBC + Motley Fool 多源一致）**；对照：2025 审计 booked 收入 $13.1B、经营亏损 $20.9B（泄露审计财报，双源 ⚠️）；企业收入占比 >40%（CNBC 称 8 月企业已超消费）；公司 2029 目标：收入 $100B 且转正盈利 | 2024 末 ~ 2026-08 | Reuters、CNBC（经 quashbugs/getpanto 转引）；Motley Fool/Yahoo 2026-08-27；valueaddvc 2026-08-05 | 🟡 媒体转引（多源）；**仍不进 R1 分子** |
| OpenAI | IPO / 融资 | 机密 S-1 已于 2026-06-08 递交 🟡；最近一轮估值 $852B（2026-03-31）🟡；传 IPO 目标估值 ≥$1T（约 25x  trailing ARR）、募资 ≥$60B；CFO Friar 内部称「2027 年成为上市公司」 | 2026-03 ~ 2026-08 | Motley Fool/Yahoo 2026-08-27；alphasignals 2026-08-17 | 🟡 |
| Anthropic | ARR 轨迹 | 官方/高管序列：$9B（2025-12）→ $14B（2026-02）→ $19B（03）→ $30B（04）→ $44B（05 初）→ $47B（05 中，Series H 披露，CFO Rao）→ **$65B（07 末，Reuters）**；第三方追踪器估 $69–74B（NextBigFuture），差异提示上市前口径收紧；**Q2'26 收入 >$11.5B（超对 Series H 投资人的 $10.9B 预测）、首次经营利润 $559M（Bloomberg）**；Claude Code：$0.5B（2025-09）→ $8B（05）→ ~$15B（08，追踪器）；承销行按 2028 收入 $190–200B 建模（Reuters） | 2025-12 ~ 2026-07 | Reuters/Bloomberg/CNBC 经 futuresearch（2026-08-20 重跑）转引；36kr；chiefgroup | 🟡 媒体转引（Reuters/Bloomberg 层级）；**仍不进 R1 分子** |
| Anthropic | 估值 / 融资 / 上市 | Series G 2026-02：$30B @ $380B post；Series H 2026-05：$65B @ $965B post（Capital Group 共同领投，Fidelity/T. Rowe 参与——共同基金锚定上市预期）；机密 S-1 2026-06-01 递交；传 2026-10 Nasdaq 窗口（GS/JPM/MS 主承销）、目标估值 $2T（≈31x 7 月 ARR）；pre-IPO 信贷额度 >$10B；Polymarket 定价 10 月底前上市 ~74%；**风险提示**：云转售毛额记账若被审计改净额，ARR 一次性砍 20–40%（Sacra 经 futuresearch） | 2026-02 ~ 2026-08 | futuresearch 2026-08-20；Zacks 2026-08-26；36kr；alphasignals | 🟡（$965B 双源；$2T 为传闻；会计风险待 S-1 公开） |
| MSFT 企业 AI | 年运行率 | >$37B，+123% YoY（含 Azure AI + Copilot 家族的合并口径，**非纯 Azure AI 拆分**） | FY26Q2 口径 | axis-intelligence 2026-07-31；arlobriefing 2026-08-27（同口径复述） | 🟡 |
| MSFT Copilot | 付费席 | M365 Copilot 20M 付费席（FY26Q3 电话会，Nadella，2026-04-29），渗透率 ~4.4%（分母 450M+ 商业席）；GitHub Copilot 4.7M 付费（FY26Q2，+75% YoY） | 2026-04 / 2026-01 | TechCrunch 转引财报会；axis-intelligence | 🟡 |
| 消费端 | ChatGPT | WAU ~10 亿（2026-07，OpenAI 发言人经 The Verge）；消费付费订阅 >5,000 万（2026-02-27 OpenAI 官方口径）；企业席 7M | 2026-02 / 2026-07 | quashbugs 汇编（含一手出处标注） | 🟡 |

**原则**：OpenAI/Anthropic 的 ARR 未经核实前，一律不进 R1 的分子。宁可 R1 空着，不用编数填。
**2026-08-31 注**：Anthropic 的 $65B 已有 Reuters 归属、Q2 利润有 Bloomberg 归属，证据等级从「汇编媒体」上升到「权威媒体转引公司披露」，但按本账纪律仍未达「公开审计报表/S-1」门槛；Anthropic 10 月 IPO 窗口（Polymarket ~74%）是分子转正最近的事件节点。Sequoia（David Cahn，8/10）框架可作分母直觉参照：$1.5T 基建支出需要 $3T 收入匹配，而当时 OpenAI+Anthropic 合计 ~$80B ARR（8 月末媒体口径已升至 >$105B）🟡。

---

## 4. 勾稽检查表（双边出现原则）

**原则**：每一笔大额交易，必须在买方和卖方两边的报表/公告里都能找到落点；同一笔交易不得在买家 CapEx 和卖家 backlog 里被当成两笔独立需求重复计数。

| # | 检查项 | 买方落点 | 卖方落点 | 状态 |
|---|---|---|---|---|
| C1 | OpenAI 承诺全景与支付能力 | **未去重公开面值池（tomtunguz 2026-08-18 整理）**：Oracle/Stargate $300B（2027–31，$60B/年）+ Azure 增量 $250B（2025–30）+ AWS $38B（2025–31）+ NVDA 算力承诺（电话会口径 **≈12GW**，原 10GW LOI + PORTS-Pike 4.25GW 园区 20 年租约）+ AMD 6GW（~$90B 硬件收入潜力）+ Broadcom 10GW（Tunguz 估 ~$350B 🟡测算）+ CRWV $22.4B（至 2029）→ **~$1.1T+**。其中可能有同一最终需求的上下游、备选供应商、硬件与云服务重叠；不是 OpenAI 净承诺。年化收入 >$40B 🟡仅作偿付能力背景，**不得计算承诺/收入比** | 各家供应商报表分散落点（ORCL FY26 CapEx $55.7B ✅库；NVDA PORTS-Pike 担保 ≤$105B ✅财报 8/26；Camellia 3.2GW 获 GA PSC 批准 8/26 🟡） | ⬜ 先分配交易 ID、交付期与重复关系；去重并确认最终协议后，才可计算净承诺/收入 |
| C2 | AMD Q2'26 DC +107% 中，多少来自 OpenAI/Meta 长约（带权证的"循环收入"），多少来自无关联第三方 | AMD 10-Q 客户集中度 | OpenAI/Meta 侧 CapEx | ⬜ 进展：8/18 Advancing AI 活动再确认结构分化——OpenAI/Meta 拿权证、Anthropic 拿 AMD 现金入股（moorinsights/ceevis 🟡）；第三方/关联收入拆分仍待 10-Q |
| C3 | MSFT 占 CRWV 收入 67%（FY2025）——MSFT 一边自己建一边租，租的部分是否重复计入"AI 需求" | MSFT CapEx vs 租赁（FY26 CapEx $116B ✅库已落） | CRWV 收入集中度 | ✅ 事实已确认，含义待分析 |
| C4 | 九大 CSP CapEx $886.7B（四大 $725–760B）vs 供给侧 AI 收入合计 | 台账 A 合计（Q2'26 单季 Big-5 ≈ $185B，其中 $151B ✅库） | 台账 B：NVDA FY27Q2 DC $89B（年化 ~$356B）✅财报转引 + 其余 | ⬜ 差额分析待做；NVDA hyperscale/ACIE 拆分（$48.7B/$40.3B）给了买家结构新锚点 |
| C5 | 裁员节省的人力成本 vs 同期 CapEx 增量（MSFT/META/AMZN 逐家） | 10-K 人力成本科目 | — | ⬜ 本轮无增量 |
| C6 | NVDA $500B 融资平台（2026-08-10 MoU）与**已披露担保**的关系 | 未来借款人（neocloud/企业）报表——尚未发生 | **8/26 10-Q/CFO Commentary 已披露实际担保：PORTS-Pike（SB Energy 4.25GW 园区，独家租与 OpenAI 20 年）担保上限 ≤$105B** ✅财报；$500B 平台最终协议截至 8/31 无签署新闻 | 🟡 部分落点：担保已入 SEC 文件（或有事项口径待 10-Q 全文细读）；平台 MoU 仍悬空——二者是否同一框架待核 |
| C7（新增） | Anthropic 承诺全景：AWS $100B/10 年（ceevis 单源 🟡）+ Azure $30B（chiefgroup 🟡）+ AMD 2GW + Google TPU 存量 vs Anthropic 自身收入（$65B ARR 🟡）与融资 | Anthropic 承诺池（待系统整理，未去重） | AWS/MSFT/AMD/Google 各自报表落点 | ⬜ 新开口项，先补交易清单与来源等级 |
| C8（新增） | Google-Marvell 权证（≤$12.2B，vesting 绑订单；潜在收入上限 $120B 至 FY33 为面值非承诺）双边落点 | GOOGL CapEx / 自研芯片采购 | MRVL 报表：权证公允价值、收入确认节奏（MRVL 称 FY27 收入展望已上调至 ~$11.5B 🟡） | ⬜ 待 MRVL 下季 10-Q 权证披露 |

---

## 5. 关联融资与潜在循环交易登记簿（供应商融资 / 股权换订单）

> 互联网泡沫的 vendor financing 在现代的样子：芯片厂/云厂给客户注资或送权证，客户拿钱回头买货——收入可能真实，但需求的"自发性"存疑。**全部登记不等于全部计入 R2**：仅当现金支付、担保或权证公允价值及其对应收入均已在同一期间确认，才符合 §0.0 的正式计算门禁。

| 日期 | 出资方 | 接收方 | 结构 | 规模 | 来源 |
|---|---|---|---|---|---|
| 2025-09 | NVIDIA | OpenAI | 股权投资换系统采购 | 拟投最高 $1,000 亿，绑定 10GW 采购 | 公告（AMD 笔记） |
| 2025-10-06 | AMD | OpenAI | 6GW 长约 + 权证最高 160M 股（行权价 $0.01，绑里程碑+股价） | 权证按签约时股价价值数十亿美元 | AMD 公告（AMD 笔记） |
| 2026-01 | NVIDIA | CoreWeave | $20 亿股权（$87.20/股）+ 此前 $63 亿 take-or-pay 产能兜底至 2032 | 合计 $83 亿量级 | CRWV 笔记 |
| 2026-02-24 | AMD | Meta | 6GW 长约 + 权证最高 160M 股 | 同上结构 | AMD 公告（AMD 笔记） |
| 2026-04 | Jane Street | CoreWeave | $10 亿股权（$109/股）+ $60 亿云合同 | $70 亿量级 | CRWV 笔记 |
| 2026-07-22 | AMD | Anthropic | **反向结构**：AMD 出资最高 $5B 入股（无权证，绑部署里程碑），换 2GW MI450 采购（首个 1GW 2027H1）；AMD 三家前沿实验室累计承诺 ~14GW | $5B | AMD 笔记；ceevis 2026-08-23 🟡 |
| — | OpenAI | CoreWeave | $3.5 亿股权投资 + 合同累计 $22.4B | $22.4B+ | CRWV 笔记 |
| 2026-08-10 | NVIDIA + Apollo / BlackRock / Blackstone / Brookfield / Goldman Sachs / KKR | NVDA 客户（未来借款人） | **vendor financing 机构化**：六家机构募集第三方资本建独立算力融资平台，以 GPU/数据中心为抵押放贷，债券经 SPV 打包由 GS 承销；NVDA 提供单项目 ≤25% 残余价值支持。MoU 阶段、未签最终协议，$500B 是目标非承诺（截至 8/31 无签署新闻） | 目标 >$500B；NVDA 或有敞口上限 ≈$125B（25%） | 公司公告多源核实：proactiveinvestors(B)/futunn(A)/tipranks(B)/remio(B)，2026-08-11~13；8/10 CNBC 联合采访 |
| 2026-08 | NVIDIA | Nebius | $2B 股权投资（支持 Vera Rubin 部署）；链条下游：Nebius 持 Meta ≤$27B 合同（2026-03-16 官宣，$12B 专属容量 + ≤$15B 追加）+ MSFT 合同，Meta+MSFT 合计上限 $46.4B | $2B 股权（下游合同 $46.4B） | DataCenterDynamics 2026-08-05 🟡；Nebius 官方公告（eqs-news）2026-03-16 |
| —（时点待核） | Microsoft / NVIDIA | Anthropic | MSFT 入股约 5–10% + Anthropic 承诺 $30B Azure 采购；NVDA 投资 >$10B（ceevis 亦提及「现有 Microsoft 与 Nvidia 股权承诺」，方向获第二来源支持） | $30B 采购承诺 + 股权 | chiefgroup 2026-04-10 🟡；ceevis 2026-08-23 🟡；待原始公告核实 |
| **2026-08-19（新）** | Google | Marvell | **买家拿权证模式扩散**：Google 获权证可购 ≤$12.2B MRVL 股票，vesting 绑未来芯片订单；扩大定制芯片合作（推理加速器/存储/网络/内存接口）；潜在收入上限 $120B 至 FY2033（面值非承诺） | 权证 ≤$12.2B；订单上限 $120B（面值） | Bloomberg/CNBC 经 andrew.ooo（2026-08-24）/code4u 转引 🟡 |
| **2026-08-21（新）** | Broadcom（举债方）；Blackstone、Apollo 等（贷款方） | Broadcom 自身定制芯片产能（服务 Anthropic、OpenAI 等） | **供应商举债扩产**：谈判募资 >$60B（含次级层或达 $100B），延展 6 月三方算力融资合作；非股权换订单，但债务偿还依赖特定客户采购承诺 | $60–100B 债务（谈判中，未签约） | Bloomberg 经 code4u 转引 2026-08-21 🟡 |
| **2026-08-26（新）** | NVIDIA | SB Energy / OpenAI（PORTS-Pike 园区） | **首个报表级关联担保**：NVDA 为 SB Energy 俄亥俄 4.25GW 园区（独家租与 OpenAI、20 年）提供担保 ≤$105B；CFO Commentary 称每代部署 ≈150 万颗 GPU ≈ $150–200B NVDA 收入 | 担保上限 $105B（已进 10-Q/CFO Commentary「Guarantees」节） | NVDA Q2 FY27 CFO Commentary ✅财报（cloud.theai.com 转引，2026-08-26） |
| —（结构待核） | Anthropic | MatX | 报道称 Anthropic 愿付 $7B（远高于 MatX 最近私募估值），MatX 保持独立；结构（股权投资/收购要约/采购绑约）不明——**买家注资供应商**方向，若属实为实验室向上游延伸的首例大额 | $7B（报道值） | cryptobriefing 2026-08-27 🟡单源 |

**观察（假设，待会计落点验证）**：AMD 的“权证换订单”与“现金入股换订单”是值得追踪的结构变化，但不能单凭结构本身认定需求恶化；须看实际行权、交付、收入确认和客户是否有替代融资来源。
**2026-08-31 追加观察（待核）**：本周三个结构信号——(1) **关联融资进入 SEC 披露层**：PORTS-Pike ≤$105B 担保写入 NVDA CFO Commentary，是登记簿中首个有报表落点的条目，R2 门禁所缺的「会计确认」开始补齐；(2) **买家拿权证模式从 AMD 扩散到 Google-Marvel(l)**——8 月前还只有 AMD 一家送权证，现在 Google 也拿供应商权证，说明该结构已成行业标准谈判工具；(3) **杠杆向供给方蔓延**：Broadcom 为特定客户产能举债 $60–100B，供应商自身也开始加杠杆。另入线索池不登记：Meta 向 Anthropic 出租自有算力的谈判（≤$10B/2 年，NYT/CNBC/Reuters 7/17，未确认）；NVDA 传近 $12.9B 洽购 Hugging Face（8/29 单源传闻）；Anthropic $1.5B 企业 JV（8/9 语焉不详）。
Jane Street 同时出现在 CRWV（股权+云合同）和 Etched（领投 $700M @ $21B 估值 + 首个机架客户，WSJ 经 stocktwits 转引 🟡 2026-08-19）——交易型资金在算力链多层同时做「投资人+客户」，单笔不登记，模式记入观察。

---

## 6. 对账节奏

- **每日对账**（定时任务「AI 总账 · 每日对账」，每天 09:17 Asia/Shanghai）：扫过去 24–48 小时新闻/财报/合同 → 更新台账三层 + 登记簿 → 数据足够时重算 R1/R2/R3 → 更新第 8 节核实记录（无增量也如实记录）。
- **财报季全量对账**（一年四次，每日任务在财报季内自动加密）：Q4 财报 1 月中–2 月 / Q1 4 月中–5 月 / Q2 7 月中–8 月 / Q3 10 月中–11 月。财报季内逐家落数，替换指引口径为实际口径。
- **事件触发**：单笔 >$10B 的合同/融资公告，当天登记，不等待定任务。

---

## 7. 待对账池（按优先级）

1. **OpenAI / Anthropic ARR** —— 台账 C 地基，R1 分子的前提。进展（2026-08-31）：Anthropic $65B（7 月末，Reuters 转引）/ OpenAI >$40B（8 月多源）；转正观察窗口 = Anthropic 传 10 月 Nasdaq IPO（Polymarket ~74%）、OpenAI 机密 S-1（6/8 递交）公开。附加风险项：Anthropic 毛额/净额记账重述风险（-20~40% 口径）。
2. ~~MSFT / GOOG / AMZN / META 2026Q2 实际 CapEx~~ —— **2026-08-20 已取 ✅**（MSFT FY26Q4 $35.8B 推算、GOOGL Q2 $44.93B、AMZN Q2 $54.21B）。剩余：META Q2'26（库缺行，本轮仍无）、各家融资租赁/表外口径与现金 CapEx 的差异。
3. NVIDIA backlog / 合同负债 —— 部分进展（2026-08-31）：对上游供应与产能承诺 $119B→$279B ✅财报转引；**客户侧** backlog/合同负债仍待取（10-Q 全文）。
4. MSFT Azure AI 单独收入口径 —— 部分进展：企业 AI 合并口径 >$37B 年运行率 🟡；纯 Azure AI 仍未拆分。
5. CRWV 2026Q2 实际 CapEx vs 指引 $35–39B 的进度 —— 库暂只有 Q1'26 收入（$2.08B ✅）；等 Q2 财报入库（本轮库 8/19 后无新行）。
6. OpenAI 累计融资额与现金消耗速率 —— 部分进展：2025 经营亏损 $20.9B（泄露审计财报，双源 ⚠️）。
7. NVDA $500B 融资平台：最终协议签署、首单发行（截至 8/31 无签署新闻）；PORTS-Pike $105B 担保的 10-Q 或有事项全文细读（是否与平台同一框架）。
8. META Q2'26 CapEx / FCF 入库核验（媒体：单季 FCF $784M、新增债 $24.9B 🟡）；AMZN TTM FCF 库口径（-$11.6B）与媒体口径（-$7.6B）的差异定性。
9. **（新）NVDA FY27Q2 入库核验**：库截至 8/31 未收 8/26 的 10-Q；当前 $96.22B/$89.0B/EPS $2.46 等均为财报多源转引，入库后逐项复核。
10. **（新）Google-Marvell 权证公允价值与 vesting 进度**（MRVL 下季 10-Q）；Broadcom $60–100B 举债是否签约；Anthropic-MatX $7B 结构定性。

---

## 8. 来源与核实记录

| 日期 | 动作 | 内容 |
|---|---|---|
| 2026-08-20 | 建台账 | 骨架 v1；库核实数字（NVDA/AMD/INTC/CRWV）来自本会话 2026-08-18 stock_data 取数；TrendForce/CSP 数字为媒体转引待原始出处；OpenAI/Anthropic ARR 标【尚无法验证】 |
| 2026-08-20 | 每日对账 #1 | **库核实（stock_data，本日取数）**：NVDA FY27Q1 $81.62B/NI $58.32B/EPS $2.39；MSFT FY26 CapEx $115.95B（Q4 单季 $35.8B 推算）、FY26 OCF $182.94B；GOOGL Q2'26 CapEx $44.93B、Q2 FCF -$5.86B（复算坐实「负 FCF 季」媒体说法）；AMZN Q2'26 CapEx $54.21B、H1 CapEx $98.41B > OCF $71.42B、TTM FCF ≈ -$11.6B；META Q1'26 $19.00B（Q2 库缺行）；ORCL FY26 CapEx $55.66B；MU FQ3'26 $41.46B/NI $28.24B；AVGO FY26Q2 $22.19B；VRT Q2'26 $3.27B；CRWV Q1'26 收入 $2.08B/净亏 $0.74B。**媒体登记**：四大 CSP 2026 指引 $725–760B（AMZN $220B↑ / GOOGL $195–205B↑ / MSFT ~$190B / META $130–145B 收窄）；NVDA+六家华尔街机构 $500B 算力融资平台 MoU（8/10，Burry「绝望信号」，NVDA CDS 翻倍）；WSJ：九大科技公司 AI 表外承诺 ~$3T（未开始租赁 $1.2T + 采购承诺 $1.9T；Meta 未开始租赁 $347B）；OpenAI 年化 $25B（Reuters 2 月）→$40B+（CNBC 8 月，冲突未解）、机密 S-1 已递；Anthropic ARR 轨迹至 5 月 $47B（36kr 单源 ⚠️）、Q2'26 收入 $11.5B + 首季经营盈利、Series H $65B @ $965B（双源）；OpenAI Project Camellia $20–30B/3.2GW；Meta-Nebius ≤$27B（3/16 官宣）+ NVDA-Nebius $2B 入股；MSFT/NVDA-Anthropic 入股 + $30B Azure（chiefgroup 单源待核）；Guardian 调查 MSFT 已装 AI 芯片 ~220 万颗（MSFT 否认其推算假设）。**初步口径（已被 v1.2 替代）**：当时将 $185B 视为 R1 分母、将累计融资存量/单季收入计算为 R2、将现金流缺口描述为 R3 抬头；这些均保留为修订前工作痕迹，不再作为当前结论。 |
| 2026-08-20 | 方法论修订 v1.2 | 新增 §0.0 口径门禁与五本账；Big-5 $185B 降级为混合期间的总 CapEx 上限代理值；R1 改为“当期可观察货币化覆盖度”，R2/R3 改为满足同期间与会计确认条件后才可计算；撤回未去重承诺/收入、累计融资存量/单季收入等正式比率表述。 |
| 2026-08-31 | 每日对账 #2 | **库查询**：stock_data 库 2026-08-19 后无新入库行（NVDA FY27Q2 的 10-Q 尚未入库），META Q2'26 仍缺。**财报登记（NVDA FY27Q2，8/26 发布，新闻稿+CFO Commentary+10-Q 多源转引一致，待入库复核）**：收入 $96.22B（+106%）、DC $89.0B（+117%）、GAAP GM 75.0%、NI $59.69B、EPS $2.46/$2.22、FCF $21.34B；Q3 指引 $108B±2%（中国 DC 算力归零假设）；首次客户拆分 Hyperscale $48.7B vs ACIE $40.3B；对上游供应/产能承诺 $119B→$279B；Rubin 8 月初量产、Q3 占 DC ~20%、单 GW $40B。**新 >$10B 登记（§5）**：NVDA PORTS-Pike 担保 ≤$105B（10-Q/CFO Commentary，首个报表级落点）；Google-Marvell 权证 ≤$12.2B 绑订单（8/19，Bloomberg/CNBC 转引）；Broadcom 拟举债 $60–100B 服务 Anthropic 等定制芯片产能（8/21，Bloomberg 转引）。**终端付费更新**：Anthropic ARR $65B（7 月末，Reuters）、Q2'26 收入 >$11.5B + 首季经营利润 $559M（Bloomberg）、S-1 6/1 递交、传 10 月 Nasdaq 窗口（GS/JPM/MS）、承销按 2028 收入 $190–200B（Reuters）、毛额/净额重述风险提示；OpenAI >$40B（8 月，CNBC+Motley Fool 多源）、估值 $852B（3/31 轮）、CFO 称 2027 上市。**买家侧**：OpenAI Camellia 3.2GW 供电合同获 GA PSC 批准（8/26）；Google Cloud Q2 +82%、backlog >$514B；AWS 年化 $150B、AI >$15B run-rate；MSFT Azure 两区域电力限容报道。**比率**：R1/R2/R3 均未过 v1.2 门禁，维持【不计算】——但 R2 所需的会计落点开始出现（PORTS-Pike），R3 杠杆信号扩散至供给方（Broadcom）。**线索池（不登记）**：NVDA 传 ~$12.9B 洽购 Hugging Face（8/29 单源）；Meta→Anthropic 出租算力谈判（7/17，未确认）；Anthropic-MatX $7B（结构待核，已按单源 🟡 登记于 §5 末行）；Anthropic $1.5B 企业 JV（8/9 不详）。 |

**数据源优先级**：stock_data 库（ssh my-t-vinci）> 公司 10-Q/10-K > 官方公告 > 权威媒体 > 一般媒体。媒体转引必须标注，能换原始出处就换。
