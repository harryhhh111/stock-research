# Oracle（ORCL）研究笔记

> 整理日期：2026-08-31 ｜ 最新财务更新：2026-09-10（FY2027 Q1）｜行情数据截止：2026-08-27
> 研究重点：**Oracle 的数据中心业务**（OCI 扩张、资本开支、Stargate、融资结构）
> 单位：全文统一用 $B（十亿美元）；财年口径：Oracle 财年截至 5 月 31 日，FY2026 = 2025-06-01 ~ 2026-05-31
> 数据基准：财务报表与行情以 stock_data 库为准（标注【库核实】）；10-K 原文核对标注【10-K核实】；库外数据带来源链接

## 目录

- 1. 公司概览
- 2. 业务模块
- 3. 营收情况（含收入结构）
- 4. 盈利与负债（含信用评级分析）
- 5. 竞争对手
- 6. 专题：数据中心（OCI 基建）
- 6+. 专题：两年股价复盘（独立文档：[股价复盘-2024-2026.md](/Users/vinci/Documents/stock_research/ORCL/股价复盘-2024-2026.md)）
- 7. 订单与客户承诺（RPO）
- 8. 估值与资金效率
- 9. 值得注意的点
- 10. 我的看法
- 11. 跳过的模块及原因
- 12. 后续研究方向
- 13. 数据来源与核实记录

## 1. 公司概览

Oracle 是企业级数据库与应用软件的老牌巨头，2016 年起向云转型，2024 年后因 AI 算力需求爆发，其云基础设施业务（OCI）成为增长引擎。当前（2026 年）市场已基本把 ORCL 当作"AI 基建股"定价：公司正以远超自身现金流的规模举债建设数据中心，承接 OpenAI 等 AI 客户的算力合同。

关键身份变化：CEO 为 Clay Magouyrk（原 OCI 负责人）；创始人 Larry Ellison 仍是最大股东与 CTO。FY2026（截至 2026-05-31）营收 $67.4B，市值 $437.7B（2026-08-27，【库核实】daily_quote）。

## 2. 业务模块

Oracle 是单一经营分部，FY2026 起利润表按四条收入线披露：Cloud / Software / Hardware / Services（此前口径为 Cloud Services & License Support 等四线，新口径把"云"与"软件"彻底分开——本身就是转型完成的信号）【10-K核实】：

1. **Cloud（云）**——IaaS（OCI 算力）+ SaaS（Fusion/NetSuite 等云应用订阅）。全部增长来自这里。
2. **Software（软件）**——传统数据库/中间件：大头是存量客户的年度支持费（support），小头是新增许可（license，长期缓慢萎缩）。
3. **Hardware（硬件）**——Exadata 一体机与服务器，规模小。
4. **Services（服务）**——咨询实施，规模小、毛利薄。

理解本项目要抓住的一条暗线：**Cloud 内部的 IaaS 再分两层**——
- **企业级 OCI**（数据库上云、主权云、多云互联 Multicloud）：高毛利、需求稳定；
- **AI 训练/推理算力（GPU 数据中心）**：即本研究的"数据中心业务"——重资产、低毛利（GPU 折旧+电力）、靠超长约（RPO）锁定需求。Oracle 正在从"软件公司"变成"软件现金流供养 AI 基建"的结构。

竞争对手差异：Oracle 相对 AWS/Azure/Google 的差异化是数据库存量客户 + 全栈（应用+数据库+基础设施）+ 多云互联（Oracle Database@Azure/Google/AWS）；在 AI 算力上靠敢于接超大单（OpenAI $300B）抢位，代价是资产负债表激进扩张。

## 3. 营收情况

### 3.1 年度序列（【库核实】us_financial_current_annual，单位 $B）

| 财年（截至5/31） | 营收 | YoY | 营业利润率 | 净利润 | 净利率 |
|---|---|---|---|---|---|
| FY2022 | 42.4 | +4.8% | 25.7% | 6.7 | 15.8% |
| FY2023 | 50.0 | +17.7% | 26.2% | 8.5 | 17.0% |
| FY2024 | 53.0 | +6.0% | 29.0% | 10.5 | 19.8% |
| FY2025 | 57.4 | +8.4% | 30.8% | 12.4 | 21.7% |
| FY2026 | 67.4 | +17.3% | 30.6% | 17.1 | 25.4% |

要点：

- FY2026 营收 +17.3%，为十余年最快增速，驱动全部来自云（[Oracle Q4 FY2026 财报新闻稿](https://www.oracle.com/news/announcement/q4fy26-earnings-release-2026-06-10/)，2026-06-10）。
- 营业利润率五年从 25.7% 抬到 30.6%——AI 重资产扩张尚未压垮利润率（折旧高峰在后头，见 §6）。
- **净利含金量需打折**：FY2026 利润表含非经营净收益 +$3.5B（FY2025 仅 +$0.06B）【10-K核实，R4 利润表】，叠加重组费用 $1.8B。Q2 FY2026 单季净利 $6.1B 异常偏高即源于此一次性项目（具体构成疑与 Ampere 股权处置相关，待查附注）。

### 3.2 收入结构（四条收入线 + 云内部拆分）

FY2026 10-K 利润表（R4）+ 收入明细附注（R89）【10-K核实】，单位 $M：

| 收入线 | FY2024 | FY2025 | FY2026 | FY2026 占比 | FY2026 YoY |
|---|---|---|---|---|---|
| **Cloud 合计** | 19,774 | 24,506 | 33,989 | **50.4%** | +38.7% |
| — 其中 IaaS（OCI 算力） | 6,840 | 10,234 | 18,101 | 26.9% | **+76.9%** |
| — 其中 SaaS（云应用） | 12,934 | 14,272 | 15,888 | 23.6% | +11.3% |
| **Software 合计** | 24,690 | 24,724 | 24,541 | 36.4% | -0.7% |
| — 其中软件支持费 | 19,609 | 19,523 | 19,804 | 29.4% | +1.4% |
| — 其中新增许可 | 5,081 | 5,201 | 4,737 | 7.0% | -8.9% |
| **Hardware** | 3,066 | 2,936 | 3,084 | 4.6% | +5.0% |
| **Services** | 5,431 | 5,233 | 5,743 | 8.5% | +9.7% |
| **合计** | 52,961 | 57,399 | 67,357 | 100% | +17.3% |

（Cloud 合计为总收入减其余三线推算，与公司披露的"FY2026 云收入 $34.0B +39%"勾稽一致 ✅）

结构判读：

- **云已占半壁江山**（50.4%），且增长全部来自 IaaS（+77%）；SaaS 只有 +11%，是成熟的应用订阅业务。
- **存量软件业务停滞**：软件线整体 -0.7%，其中新增许可 -8.9% 持续萎缩，靠支持费（存量年金，+1.4%）撑着——这条线是典型的"现金牛遗产"，高粘性但零增长。
- 换个说法：**Oracle = 一个零增长的软件年金业务（~$25B 收入、极高利润率）+ 一个爆发中的 AI 算力业务（IaaS $18.1B、+77%）+ 边缘业务（硬件+服务 $8.8B）**。估值矛盾集中在第二块。
- 分部盈利（R86，直接费用口径）：Cloud+Software 直接营业利润 $34.5B（直接利润率 59%），Hardware $2.0B，Services 微利——硬件和服务基本只贡献收入不贡献利润。

### 3.3 FY2026 单季拆分（【库核实】fact_version，YTD 差额法；单位 $B）

| FY2026 | Q1（至8/31） | Q2（至11/30） | Q3（至2/28） | Q4（至5/31） |
|---|---|---|---|---|
| 营收 | 14.9 | 16.1 | 17.2 | 19.2 |
| 净利润 | 2.9 | 6.1 | 3.7 | 4.3 |
| CapEx | 8.5 | 12.0 | 18.6 | 16.5 |

- Q4 营收 +21%，其中云收入 $9.9B（+47%）：IaaS $5.8B（+93%）、SaaS $4.1B（+10%）。云收入略低于市场预期（$9.99B），叠加融资计划公布，财报后股价跌超 10%（[Yahoo Finance](https://finance.yahoo.com/sectors/technology/article/oracle-q4-earnings-beat-on-revenue-but-miss-on-cloud-sales-221337908.html)，2026-06-11）。
- 单季 CapEx 从 Q1 的 $8.5B 爬到 Q3 的 $18.6B，数据中心建设斜率极陡。

### 3.4 员工与人效

- FY2025 员工约 16.2 万人；FY2026 据媒体复算 10-K 为约 14.1 万人，人均创收约 $478K（+35%）（[Axis Intelligence](https://axis-intelligence.com/oracle-statistics/)，2026-07-27，二手转述）。
- 旁证【10-K核实】：FY2026 重组费用 $1.84B（FY2025 仅 $0.37B），与大规模裁员/重组一致。

### 3.5 FY2027 指引与 Q1 开局（2026-09-10 更新）

| 项目 | 管理层 FY2027 指引 / Q1 实际 | 信息属性 |
|---|---|---|
| 全年营收 | **至少 $90B** | 管理层电话会指引 |
| 全年 non-GAAP EPS | **$8.10** | 管理层电话会指引，较此前 $8.05 上调 |
| Q2 营收增速 | +30% 至 +34% | 公司新闻稿指引 |
| Q2 云收入增速 | +65% 至 +71% | 公司新闻稿指引 |
| Q1 营收 / 云收入 | $19.3B（+30%）/ $11.6B（+62%） | 公司实际披露 |
| Q1 IaaS / SaaS | $7.4B（+121%）/ $4.2B（+10%） | 公司实际披露 |

- 年度营收与 EPS 是管理层的非 GAAP 预测，不等于已签约收入或现金流；$90B 相比 FY2026 的 $67.4B 意味着至少约 34% 的增长。
- CapEx 指引另见 §4.1.1 与 §6.1：全年总 CapEx $90–95B、净现金 CapEx 不超过 $70B。因此，本轮增长指引的核心问题不是需求是否增长，而是收入确认、预付款和外部融资能否跟上建设支出。

来源：[Oracle FY2027 Q1 财报新闻稿](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Q1-Results-Driven-by-Triple-Digit-Growth-in-Cloud-Infrastructure-Revenues/default.aspx)（2026-09-10，S）；年度营收/EPS 为管理层电话会表述，见 [Q1 电话会文字稿](https://stockanalysis.com/stocks/orcl/transcripts/689425-q1-2027/)（2026-09-10，二手转录）。

## 4. 盈利与负债

### 4.1 现金流（【库核实】us_financial_current_annual / fact_version，$B）

| 财年 | 经营现金流 | CapEx | 自由现金流 | SBC | 分红 | 回购 |
|---|---|---|---|---|---|---|
| FY2022 | 9.5 | 4.5 | 5.0 | 2.6 | 3.5 | 16.2 |
| FY2023 | 17.2 | 8.7 | 8.5 | 3.5 | 3.7 | 1.3 |
| FY2024 | 18.7 | 6.9 | 11.8 | 4.0 | 4.4 | 1.2 |
| FY2025 | 20.8 | 21.2 | -0.4 | 4.7 | 4.7 | 0.6 |
| FY2026 | 32.0 | 55.7 | **-23.7** | 4.8 | 5.8 | 0.1 |

- **这是全篇最重要的一张表**：FY2025 起 FCF 转负，FY2026 负 $23.7B。CapEx/营收比从 FY2022 的 11% 升到 FY2026 的 82.6%。
- 资本分配彻底掉头：FY2022 还回购 $16.2B，FY2026 回购只剩 $0.1B；分红仍在涨（$5.8B，股息率约 1.3%），且 FY2026 已出现优先股股息（$0.1B，强制可转债）。FY2026 的 CapEx + 普通股分红合计 $61.5B，显著超过 $32.0B 经营现金流；不能按单笔现金追溯“哪笔债直接发了股息”，但从整体资金来源看，外部融资是覆盖建设与分配的必要部分。
- SBC $4.8B/年（占营收 7.1%），摊薄股数 FY2022→FY2026 从 27.86 亿股增至 29.14 亿股（四年 +4.6%，温和）；但 FY2026 已启动 $5B 股权融资，FY2027 还有 $20B ATM 增发计划，稀释将加速（见 §6.6）。

### 4.1.1 FY2027 Q1：客户预付款缓冲 CapEx，但不改变 FCF 为负

| FY2027 Q1（截至 2026-08-31） | $B | 口径 |
|---|---:|---|
| 经营现金流 | +23.10 | GAAP 现金流量表 |
| 总 CapEx | -28.50 | 现金购置 PP&E |
| 自由现金流 | **-5.40** | 经营现金流 - 总 CapEx |
| 客户预付款（含重大融资成分） | +11.36 | 已包含在经营现金流，不能再额外相加 |
| “净现金 CapEx” | 17.97 | 公司调整口径：计入客户预付款及与 CapEx 有关的短期融资现金流 |

- Q1 的 **GAAP 自由现金流仍为 -$5.40B**。公司披露的“净现金 CapEx”是解释建设资金由谁承担的辅助口径，而不是自由现金流的替代品；由于经营现金流本身已经含有客户预付款，不能用 $23.10B - $17.97B 再称为 FCF，否则会重复计算预付款。
- 管理层在 Q1 电话会上维持 FY2027 **总 CapEx $90–95B、净现金 CapEx 不超过 $70B** 的预期。Q1 总 CapEx 已达 $28.50B，约为全年总额区间的 30%；季度建设和付款节奏会高度不均匀，不能机械年化。
- 这说明“客户出一部分钱”确实降低 Oracle 自有现金压力，却没有消除项目的资本密集性；应同时看总 CapEx、GAAP FCF、预付款及融资，而非只看任一单一指标。

来源：[Oracle FY2027 Q1 财报新闻稿](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Q1-Results-Driven-by-Triple-Digit-Growth-in-Cloud-Infrastructure-Revenues/default.aspx)（2026-09-10，S）；[Q1 财报 PDF](https://investor.oracle.com/files/content_files/1q27-pressrelease-September_FINAL.pdf)（2026-09-10，S）；全年 CapEx 指引为管理层电话会表述，见 [Q1 电话会文字稿](https://stockanalysis.com/stocks/orcl/transcripts/689425-q1-2027/)（2026-09-10，二手转录）。

### 4.1.2 FCF 为负仍分红：资本配置选择，不是现金充足证明

- FY2026 的经营现金流 $32.0B 减总 CapEx $55.7B，已形成 -$23.7B FCF；再加 $5.8B 普通股分红，建设和分红合计比经营现金流多消耗约 $29.5B（尚未计入还债等其他资金用途）。
- 同期公司取得约 $42.7B 净发债资金、$5.0B 强制可转优先股融资，并有约 $4.9B 投资处置收入及 $3.3B 与 CapEx 有关的短期融资现金流【10-K核实】。这些不是“债券直接拿来付股息”的逐笔归因，而是 FY2026 总体流动性来源。
- **【我的推演】** Oracle 仍保留并提高普通股分红，反映的是管理层在维持成熟软件公司股东回报记录与押注云基建长期回报之间的选择；分红并非合同性必付。若 FCF 持续深度为负、同时债务和股权融资扩大，分红会放大资本配置的审视压力，而非证明现金流无虞。

来源：[Oracle FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm)（2026-06-22，S）。

### 4.2 资产负债表（【库核实】+ SEC companyfacts，$B）

| 财年 | 总资产 | 股东权益 | 净PP&E | 现金 | 长期债券 | 一年内到期债券 | 经营租赁负债 |
|---|---|---|---|---|---|---|---|
| FY2022 | 109.3 | -6.2 | 9.7 | 21.4 | 72.1 | 3.8 | 3.7 |
| FY2023 | 134.4 | 1.1 | 17.1 | 9.8 | 86.4 | 4.1 | 4.9 |
| FY2024 | 141.0 | 8.7 | 21.5 | 10.5 | 76.3 | 10.6 | 7.5 |
| FY2025 | 168.4 | 20.5 | 43.5 | 10.8 | 85.3 | 7.3 | 13.5 |
| FY2026 | 261.8 | 42.5 | **100.0** | 31.3 | **122.3** | 7.2 | **30.2** |

- 有息债券合计 FY2026 末约 **$129.5B**（SEC XBRL：LongTermNotesPayable + NotesPayableCurrent）；加经营租赁负债 $30.2B（数据中心租约，FY2022 才 $3.7B，四年 8 倍），广义负债约 $160B，现金 $31.3B，净债务约 $128B。
- 净 PP&E 一年翻倍以上（$43.5B → $100.0B），直接对应数据中心投建。
- 利息费用 FY2026 $4.6B（FY2022 $2.8B），随发债继续上行。
- **表外承诺才是真正的规模【10-K核实，R64/R69 承诺附注】**：已签约但尚未起租的经营租赁承诺高达 **$260B**（租期 15-19 年，起租后才进资产负债表）——对比表内经营租赁负债仅 $30.2B，数据中心的真实承诺规模是表内数字的 9 倍；另有融资租赁负债 $7.7B（FY2025 仅 $2.9B，FY2026 新增融资租赁资产 $4.9B）、为出租方借款提供的担保 $3.3B（2026-09 到期）、无条件采购义务 $13.3B（期后又新增 $19B）。广义"表内债务+租赁+表外承诺"合计超 **$430B**，这才是穆迪说"支出承诺是重大信用关切"的完整图景。

### 4.3 为什么评级只有 Baa2/BBB（离垃圾级两档）

这是三层原因叠加，不是AI周期才开始的：

**第一层：历史包袱——举债回购把评级买下来的（2021 年就被降级）**
穆迪 2021-03 把 Oracle 从 A3 降到 Baa2，理由原文："elevated financial leverage, aggressive use of debt to finance large shareholder returns, and lack of any long-term financial policy goals"（杠杆高、激进举债回购分红、且没有任何长期财务政策目标——对大债务公司很罕见，制造了管理层风险偏好不确定性）。当时背景：税改后 Oracle 从净现金 $10B+ 变成净负债 $33B，2021-03 又发债 $15B 用于回购（回购授权加 $20B、分红加 33%），债务/EBITDA 约 4.3×（[穆迪评级公告](https://finance.yahoo.com/news/oracle-corporation-moodys-downgrades-oracles-120807586.html)，2021-03-22，S）。**其他科技巨头是 A/AA 级，是因为它们净现金或低杠杆；Oracle 是唯一一家十几年来把资本回报放在资产负债表前面的 mega-cap**——FY2022 股东权益甚至是负的（-$6.2B）。

**第二层：AI 扩张让本就高的杠杆雪上加霜**
- 穆迪（2025-12，Baa2 负面展望）：RPO 暴涨令人印象深刻，但"支持增长所需的交易对手风险与支出承诺是重大信用关切，是负面展望的主要驱动"（[Moody's Credit Outlook](https://www.moodys.com/web/en/us/insights/credit-risk/outlooks/mco-15-december-2025.html)，2025-12-15，S）。
- **标普已于 2026-07-09 降级 BBB → BBB-（展望稳定），距垃圾级仅一档**（[S&P 公告](https://www.spglobal.com/ratings/en/regulatory/article/-/view/sourceId/101695609)，2026-07-09，S）。降级理由：FY2027 capex 预测上修至 $90-95B、FY2027 自由经营现金流缺口预计 -$42B（此前预测 -$24B）、调整后杠杆 FY2027 将达 mid-4×、**OpenAI 约占 RPO 一半**、且与三大云不同，Oracle 没有自有 AI 负载可以在客户流失时消化产能（[mlq.ai](https://mlq.ai/news/sp-downgrades-oracle-to-bbb-one-notch-above-junk-citing-openai-concentration-risk/)，2026-07-12，B）。标普/Nikkei 还估算 Oracle 有 ~$273B 数据中心租赁与电力采购承诺（FY2027-29 起陆续进表）且大多不可撤销——与 10-K 披露的 $260B 未起租租赁承诺互相印证 ✅。惠誉 BBB。
- 穆迪 2026 年进一步表示：**没有其他大型 AI 基建商是以这种杠杆水平和负现金流进入本轮投资周期的**；杠杆近期可能接近 **5× EBITDA**（[Economic Times](https://m.economictimes.com/markets/us-stocks/wall-street-guide/global-market-oracles-ai-spending-spree-pushes-credit-rating-to-brink-of-junk-status/articleshow/132892290.cms)，2026-08-05，A）。
- 租赁的隐性代价：穆迪警告大量租赁数据中心虽降低前期资本需求，但**租赁资产不能出售或抵押**，削弱了财务灵活性（ET，2026-08-05）。
- 信用基本面数据点（[Bondsupermart](https://www.bondsupermart.com/bsm/article-detail/oracle-downgraded-to-bbb-yields-as-high-as-7-8-is-it-an-opportunity-or-a-warning-sign-RSS380)，2026-07-29，NA 级但数据翔实）：净债务 ~$98B、净负债率 228%、利息保障倍数 6.5×、现金 $30B+——短期偿债无虞，风险在长期承诺；OpenAI 合同年付款义务约 $60B，而 OpenAI 年化收入仅 ~$24B、尚未盈利，2026-03 完成 $122B 融资（亚马逊/英伟达/软银参投）。

**第三层：市场已经在定价"堕落天使"（fallen angel）风险**
- 若从 BBB 跌入垃圾级（BB），大量养老金/保险等授权受限机构将被强制抛售其约 $129.5B 债券——垃圾级利差比 IG 高约 300-400bp，对 FY2027 计划新增 $40B 债务意味着每年多 $0.8-1.2B 利息（Market Supply Chain，2026-06-25，NA，机制分析可靠）。
- 市场证据：Oracle 债券收益率已到 **7-8%** 区间，而 Alphabet/Amazon 只有 2.5-3.5%；2025-12 股价暴跌期间 CDS 利差一度突破 125bp（正常 IG 为 50-100bp）；巴克莱将其债券下调至低配；股价从 2026-06-03 高点 $244.58 到 2026-07-29 低点 $117.74，**区间最大跌幅 -52%**（【库核实】daily_quote；债券/CDS 数据为 ET 与 Market Supply Chain 媒体转述，2026-08）。
- 摩根士丹利信用分析师：堕落天使式降级不是迫在眉睫，但属中期风险，取决于 AI 投资的执行与变现（ET 引述，2026-08-05）。

## 5. 竞争对手

同口径对比（【库核实】，各公司财年口径不同：ORCL/MSFT 为 5/31 与 6/30 财年，AMZN/GOOGL 为日历年）：

| 公司 | 最新财年营收 | 营收增速 | 营业利润率 | 财年CapEx | 财年FCF | TTM CapEx | 市值（8/27） | PE TTM |
|---|---|---|---|---|---|---|---|---|
| ORCL（FY2026） | $67.4B | +17.3% | 30.6% | $55.7B | **-$23.7B** | $55.7B | $438B | 26.1 |
| MSFT（FY2026） | $331.8B | +17.8% | 46.8% | $115.9B | +$67.0B | $115.9B | $3,750B | 28.1 |
| AMZN（CY2025） | $716.9B | +12.4% | 11.2% | $131.8B | +$7.7B | $197.2B | $2,764B | 20.6 |
| GOOGL（CY2025） | $402.8B | +15.1% | 32.0% | $91.4B | +$73.3B | $132.4B | $4,166B | 17.1 |

- 四家都在重资本开支，但**只有 Oracle 的 FCF 深度为负**：MSFT/GOOGL 的 CapEx 仍被经营现金流覆盖（FCF 为正），AMZN TTM FCF 也已转负（-$17.4B）但其 CapEx/CFO 约 95%，而 Oracle FY2026 CapEx/CFO 达 174%——Oracle 是唯一必须持续大规模外部融资的一家，这直接解释了 §4.3 的评级差距。
- 行业背景：2026 年五大厂（MSFT/GOOGL/AMZN/Meta/ORCL）合计 CapEx 指引约 $660-690B，全部声称"供给受限而非需求受限"（[Futurum](https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/)，2026-02-12，B 级）。
- Oracle 相对三大的位置：IaaS 体量仍小一个数量级（FY2026 IaaS $18.1B vs Azure/AWS 单季 $30-40B 级），靠 AI 训练大单实现最快增速；另有一类新对手是 CoreWeave 等 neocloud（GPU 专营云，本工作区已有 [CRWV 项目](/Users/vinci/Documents/stock_research/CRWV)），它们在 Stargate 体系中既是合作方也是替代方。

### 5.1 与 neocloud 的估值分层（2026-09-01，回答"同样的逻辑为什么不同价"）

| | ORCL | CoreWeave | Nebius |
|---|---|---|---|
| 市值 / 现价 | $429.5B / $149.12【库，8-31】 | ~$42B / $81.39（Yahoo 9-1） | ~$53.5B / $196.62（Yahoo 9-1） |
| TTM 营收 / 增速 | $67.4B / +17% | ~$7.6B / Q2 +112%【库：FY25 $5.13B、26H1 $4.65B】 | ~$1B / Q1 +684% |
| 净利润 | +$17.1B | -$1.2B（FY25，【库】） | +$102M（FY25，已盈利） |
| P/S（TTM） | 6.4× | ~5.5× | ~45× |
| 资产负债表 | BBB-、$130B 债、$260B 表外租赁、FCF -$24B | $21B+ 债务、FCF 深负、adj OI 利润率 19%→1% | 净现金 + 客户预付 capex |
| Backlog / EV÷Backlog | RPO $638B / 0.83× | $99.4B / ~0.80× | ~$44B / 1.1-1.6× |
| 股价位置 | YTD -22% | 距 2025-06 峰值 -43% | YTD +135% |

判读（【我的推演】）：市场并非无差别给 AI 算力高估值，而是按四个维度分层——
1. **纯度**：NBIS/CRWV 是 100% AI 敞口；ORCL 一半是零增长软件年金，合并增速被稀释；
2. **谁为 capex 买单**：客户预付（NBIS）> 举债+backlog 对冲（CRWV）> 举债+评级悬崖（ORCL），NBIS 的 45× P/S 买的是"不用自己烧钱"的确定性；
3. **EV/Backlog 口径三家趋同（0.8-1.6×）**——市场对"订单资产证券化"的隐含定价一致，分歧在兑现路径上谁会死在半路；
4. **边际买家**：ORCL 受 BBB- 授权约束（机构被迫卖），neocloud 买家本来是高风险偏好资金，无机械卖出压力。

CRWV/NBIS 数据来源：库 fact_version（FY25 年报与 26 年季报）；[Motley Fool 对比](https://www.fool.com/coverage/charts/2026/04/09/nebius-vs-coreweave-accelerating-growth-vs-massive-scale-in-revenue/)（2026-04-09，A）；[daloopa 财务对比](https://daloopa.com/blog/analyst-pov/nebius-vs-coreweave-neoclouds-financial-analysis-daloopa-mcp-sourced)（2026-06-03，NA）；[sec-api Nebius 分析](https://sec-api.io/insights/nebius-financial-analysis)（2026-08-26，NA）；Yahoo Finance 报价页（2026-09-01，S）。

## 6. 专题：数据中心（OCI 基建）

### 6.1 扩张规模：从数字看

- CapEx：FY2024 $6.9B → FY2025 $21.2B → FY2026 $55.7B（+163%）。FY2027 管理层指引为 **总 CapEx $90–95B、净现金 CapEx 不超过 $70B**；两者不能混用，后者计入客户预付款及与 CapEx 有关的短期融资现金流。Q1 FY2027 已发生总 CapEx $28.5B、净现金 CapEx $18.0B（见 §4.1.1）。
- 净 PP&E：FY2022 $9.7B → FY2026 $100.0B（四年 10 倍）。
- 容量兑现：CEO Magouyrk 曾预计 FY2027 Q1 将有接近 1 GW 容量上线；Q1 实际披露为交付 **850 MW** 新数据中心容量及 30 万块以上 GPU。容量交付不等于当季已完全变现，需与后续 IaaS 收入、利用率和 FCF 一起观察（[Oracle FY2027 Q1 财报](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Q1-Results-Driven-by-Triple-Digit-Growth-in-Cloud-Infrastructure-Revenues/default.aspx)，2026-09-10，S）。

### 6.2 物理产能台账：GW 与 GPU（截至 2026-08-31）

**电力容量（GW）分层**——注意区分"投运 / 签约 / 规划"三个口径，媒体常混用：

| 层级 | 容量 | 内容 | 来源 |
|---|---|---|---|
| 已投运（AI） | ~1.2 GW | Abilene 旗舰园区 2026 年初开始投运，8 栋楼中前 2 栋已满负荷运营，全部预计 2026 年中完工 | TechGig 2026-03-09；IntuitionLabs 2025-11-30 |
| 上线节奏 | 近 1 GW / 季 | CEO：FY2027 Q1（2026 年 6-8 月，即当前季度）将有接近 1 GW 容量上线 | 财报电话会转述，etfpedia 2026-06-11 |
| 已签约 | 4.5 GW | Oracle 确认已完成美国 4.5 GW 电力容量租赁签约（Stargate 相关） | TechGig 2026-03-09 |
| 电力采购 | 2.8 GW | Bloom Energy 燃料电池协议扩至 2.8 GW（2026-04-17），现场发电绕开电网排队；Ellison 明言瓶颈是电力不是硬件 | Finexus/媒体 2026-04-17（B 级） |
| Stargate 规划 | 近 7 GW / $400B+ | OpenAI 官宣（2025-09-23）：五个新站点 + Abilene + CoreWeave 项目合计；目标 2025 年底锁定全部 $500B / 10 GW | [OpenAI 官网](https://openai.com/index/five-new-stargate-sites/)（S） |
| 传统云底座 | 100+ 区域 | 全球 101+ OCI 云区域（2025-03）；第三方数据库统计美国 17 个设施合计约 4.3 GW（口径含在建/规划，谨慎使用） | Blackridge 2026-03-05（B）；DataCenterMap（NA） |

- 站点清单（在建/规划）：Abilene TX（1.2 GW，投运中）、Shackelford County TX、Milam County TX（SB Energy，1.2 GW，2026 年初步投运）、Doña Ana County NM（~0.5 GW）、Port Washington/Racine WI（~0.4 GW，Vantage）、Saline Township/Mount Pleasant MI（~0.4 GW）、Salem Township PA（~0.4 GW）、Lordstown OH（软银）。
- 用工口径：Oracle 官方称 1 GW 站点运营期约需 1,000+ 名长期员工（[Oracle 社区公告](https://www.oracle.com/news/announcement/blog/oracle-ai-infrastructure-in-2026-and-our-commitment-to-local-communities-2026-01-26/)，2026-01-26）。

**GPU 数量分层**：

| 口径 | 数量 | 内容 | 来源 |
|---|---|---|---|
| 单集群上限（传统） | 131,072 | OCI Supercluster 最大规模（B200/GB200 NVL72），2025-06 GA | [Oracle 官网](https://www.oracle.com/cloud/compute/gpu/)（A） |
| 单集群上限（新） | 800,000 | OCI Zettascale10：跨多数据中心、2km 半径内、16 zettaFLOPS、multi-GW，2025-10-14 AI World 官宣，首发即 Abilene，2026 日历年下半年起交付 | [Oracle 新闻稿](https://www.oracle.com/news/announcement/ai-world-oracle-unveils-next-generation-oci-zettascale10-cluster-for-ai-2025-10-14/)（A） |
| Abilene 实际部署 | 64,000 GB200 | 2026 年底前部署 64,000 块 GB200（首批 16,000 块 2025 年夏末安装） | Bloomberg 经 [DCD](https://www.datacenterdynamics.com/en/news/openai-and-oracle-to-deploy-64000-gb200-gpus-at-stargate-abilene-data-center-by-2026-report/) 转述（B 级，原文为 2025 年报道口径，时间点待核） |
| 采购承诺 | ~400,000 GB200 / ~$40B | Oracle 采购约 40 万块 GB200，以 15 年租约向 OpenAI 供算力；"全部给 Abilene 还是分摊整个 Stargate"各来源口径不一 | Bloomberg 原始报道，经 [GPUSmith](https://gpusmith.com/articles/en/nvidia-gpu-lead-times-h100-h200-gb200)（NA）/IntuitionLabs（C）转述 |

**采购承诺的一手核对【10-K核实，R64/R69 承诺附注】**：FY2026 末（2026-05-31）Oracle 的**无条件采购义务合计仅 $13.3B**（付款计划：FY2027 $1.84B / FY2028 $1.03B / FY2029 $1.05B / FY2030 $0.95B / FY2031 $0.90B / 其后 $7.53B）；财报日后（2026-06 期后事项）又新增 **$19B、五年期**无条件采购承诺。两者合计 $32.3B——与 Bloomberg 的"$40B"在量级上接近但**对不上**，说明 40 万块/$40B 的说法要么含有条件/意向部分，要么把客户预付采购部分算了进去。结论：Bloomberg GPU 数字 ⚠️ 无法与一手文件勾稽，引用时用 $13.3B+$19B 的 10-K 口径为准。
| 全舰队规模 | "hundreds of thousands"~1M+ | Oracle 自述数十万块（2024-09）；第三方评估称 1M+（含 H100/H200/A100/AMD MI300X 存量） | [ServeTheHome](https://www.servethehome.com/2025-zettaflops-scale-compute-as-oracle-looks-to-operate-hundreds-of-thousands-of-nvidia-gpus/)（B）；layer2c 评估（NA，待核） |

**GW↔GPU 换算（【我的推演】，供估算用）**：按 Abilene 口径 40 万块 GB200 / 1.2 GW ≈ 每 GW 约 33 万块 Blackwell 级 GPU（即每 GPU 分摊约 3 kW 含网络/存储/制冷 overhead）。由此粗算：Stargate 规划 7 GW ≈ 230 万块 GPU 量级；FY2026 CapEx $55.7B ÷ 每 GPU 全系统成本约 $50-60K ≈ 当年部署能力约 100 万块 GPU 量级——与"舰队 1M+"说法在数量级上自洽。

**判读**：Oracle 当前"手里有电"的确定性排序是 投运 1.2 GW < 已签约 4.5 GW < 电力采购 2.8 GW（部分重叠）< 规划 7 GW。真正的瓶颈变量是电力接入与建设速度，不是 GPU 供应（Ellison 原话佐证）；GPU 侧的约束是 Blackwell 交付排期与 2026-2027 换代（GB300/Vera Rubin）。

### 6.3 电力从哪来（2026-09-02 专题）

**一句话答案：以天然气为主、"电网 + 自带电源（behind-the-meter）"两条腿走路；核电和可再生是叙事层，燃气才是施工层。** 10-K 主文档（orcl-20260531.htm，已存档）只有风险章节的通用表述（"扩张依赖可靠且可预测的电力来源"），未点名任何电力项目，以下全部来自公告与媒体，按站点分层：

**第一层：电网直供（公用事业公司专线）**

| 站点 | 供电安排 | 来源 |
|---|---|---|
| Abilene TX（1.2 GW，投运中） | 主用 ERCOT 电网（含附近风电），现场 350 MW 燃气电厂仅作备份（Oracle 自述）；Altman 2025 年承认"我们在烧天然气跑这个数据中心" | [AP 经 Newsday](https://www.newsday.com/business/ai-stargate-microsoft-openai-crusoe-oracle-r10037)（2026-03-27，B） |
| Port Washington WI "Lighthouse"（902 MW，2028 投运） | We Energies（WEC Energy）专用大负荷费率，Vantage 承担 100% 电力基建投资；We Energies 已在建 150 MW 光伏 + 110 MW 风电 + 75 MW 储能，约一半容量定向供给园区；WEC 口径合计新增近 2 GW 零排放容量（70% 园区 / 30% 居民）；**剩余缺口仍靠化石电力 + 年度绿证匹配** | [DigitalBridge 新闻稿](https://ir.digitalbridge.com/news-releases/news-release-details/openai-oracle-and-vantage-data-centers-announce-stargate-data)（2025-10-22）；[DCD](https://www.datacenterdynamics.com/en/news/we-energies-begins-work-on-three-renewable-projects-slated-to-help-power-vantages-data-center-in-port-washington-wisconsin/)（2026-08-06，B） |

**第二层：现场自发电（绕开电网并网排队，ERCOT 排队 5-7 年）**

| 项目 | 规模 | 细节 | 来源 |
|---|---|---|---|
| Bloom Energy 燃料电池总协议 | 最高 2.8 GW（已签约 1.2 GW，部署中） | 2026-04-13 官宣；固体氧化物燃料电池（SOFC），**烧天然气而非氢**，无燃烧、低水耗；此前一单 55 天交付（计划 90 天）；Oracle 另持 Bloom 认股权证（$113.28 × 353 万股 ≈ $400M），利益深度绑定 | [Reuters 经 socastsrm](https://d2233.cms.socastsrm.com/2026/04/13/bloom-energy-to-supply-up-to-2-8-gw-of-fuel-cells-under-expanded-oracle-deal/)（2026-04-13）；[Converge Digest](https://convergedigest.com/bloom-energy-oracle-scale-fuel-cell-deal-to-2-8-gw/)（2026-04-14，A） |
| VoltaGrid 模块化燃气发电 | 2.3 GW（德州多站点） | 2025-10-15 官宣；INNIO Jenbacher 往复式燃气发动机（单节点 20 MW）+ ABB 控制系统；气源为 Energy Transfer 管道网络 | [POWER Magazine](https://www.powermag.com/oracle-taps-voltagrid-for-2-3-gw-modular-gas-fleet-to-power-ai-data-centers-across-texas/)（2025-10-15，A） |
| Shackelford County TX "Frontier"（Vantage，1.4 GW） | 700 MW 已获批，**完全离网** | TCEQ 批准 210 台 Jenbacher 机组（197 主用 + 13 备用），美国最大燃气微电网之一 | [Business Insider 经 constructionowners](https://www.constructionowners.com/news/oracle-and-openai-to-power-new-texas-data-center-off-the-grid)（2025-10-24）；[Natural Gas Intelligence](https://naturalgasintel.com/news/no-turbine-data-centers-find-faster-path-with-natural-gas-reciprocating-engines/)（2026-05-29） |
| Project Jupiter（新墨西哥 Doña Ana/Santa Teresa，$165B，STACK+BorderPlex 开发） | 微电网规划 2.45 GW Bloom 燃料电池 | 原方案为燃气轮机 + 柴油机（县文件 700-900 MW，空气许可申请到 2.8 GW），2026-04 在社区反对下改为燃料电池；**但燃料电池仍烧天然气**——17.77 英里输气管道被州政府拒绝穿越州土地、空气许可未批，Oracle 向监管承认"没有可靠的天然气来源，电厂无法运行"；SemiAnalysis 把首次供电从 2027 推到 2029（访谈暗示可能滑到 2030s）；2026-08 新墨西哥最高法院两次不利裁决 | [DCD](https://www.datacenterdynamics.com/en/news/oracle-revealed-as-tenant-of-project-jupiter-data-center-campus-in-new-mexico/)（2026-08-19，B）；[AI Weekly](https://aiweekly.co/alerts/oracle-jupiter-swaps-gas-turbines-for-costlier-bloom-fuel-cells)（2026-07-19，B）；[KOB](https://www.kob.com/new-mexico/nm-supreme-court-delivers-two-blows-to-oracle-data-center-in-southern-new-mexico/)（2026-08-25）；[Energy News Beat](https://energynewsbeat.co/ai/oracles-165-billion-data-center-plan-gets-a-gas-pipeline-delay/)（2026-08-15，NA） |
| Abilene 现场燃气电厂 | 350 MW（备份定位） | GE Vernova / Solar Turbines 涡轮机；隔壁微软 900 MW 扩建则配 900 MW 自备燃气电厂（100% 离网口径） | [National Law Review](https://natlawreview.com/article/turbines-fence-line-how-gas-power-fueling-ai-data-center-race)（2026-02-27，A）；Newsday（同上） |

**气源层**：Energy Transfer 与 Oracle 签多份长约，向三个数据中心（两个在德州）合计供约 **900 MMcf/d**（约 90 万 Mcf/天）天然气，第一条支线已向 Abilene 供气，另两条 2026 年中接通（[Energy News Beat](https://energynewsbeat.co/ai/oracles-165-billion-data-center-plan-gets-a-gas-pipeline-delay/)，2026-08-15，NA 级但与 Energy Transfer 财报口径一致）。

**第三层：远期叙事**——Stargate 规划文件提到中期考虑核电 SMR；BorderPlex 计划为新墨西哥项目 2028 年采购 500 MW 可再生、2032 年 1 GW（[DCD](https://www.datacenterdynamics.com/en/news/oracle-revealed-as-tenant-of-project-jupiter-data-center-campus-in-new-mexico/)，2026-08-19）。Oracle 目前没有已披露的核电采购合同（对照：亚马逊买 Talen 核电、微软签 Constellation/三里岛）。

**判读**：
- **电的真实瓶颈是"时间"不是"资源"**：电网并网排队 5-7 年，而 Oracle 承诺 2027 年起向 OpenAI 供 4.5 GW——所以燃气现场发电（涡轮/发动机/燃料电池三条技术线都上）是抢时间的唯一解。"燃料电池"不等于清洁，只是换了种方式烧天然气（无燃烧、低水耗、低 NOx，但碳排放仍在，Jupiter 口径年排放约 1,000 万吨 CO₂e）。
- **自建电源不是免责金牌**：Jupiter 卡住的不是发电设备而是**输气管道和空气许可**——把电网审批换成了管道审批，SemiAnalysis 已把供电时点推后两年。这是 §6.7 风险清单里"电力与建设进度"的具体化，也解释了 Oracle 为什么要同时押注 Bloom（燃料电池）、VoltaGrid（往复式发动机）、GE Vernova（涡轮机）三条技术路线对冲审批风险。
- **电力链受益方**（研究延伸）：Energy Transfer（气源长约）、Bloom Energy（Oracle 持股绑定）、VoltaGrid/Jenbacher/GE Vernova（发电设备）。行业背景：Cleanview 统计全美数据中心自建电源设备 75% 是燃气（2026-02，[Unbreakable Ventures 转述](https://www.unbreakableventures.com/p/the-pin-how-the-strait-of-hormuz)，NA 级，仅作行业背景）。供应链各环节的承诺容量、交付里程碑与审批闸门已单列跟踪：[电力供应链跟踪表.md](/Users/vinci/Documents/stock_research/ORCL/电力供应链跟踪表.md)（2026-09-02）。

**附：三种现场发电技术的原理与取舍**（2026-09-02 补，技术常识整理，非 Oracle 披露口径）

- **燃气轮机**（Abilene 350 MW 备份电厂）：航改喷气发动机原理——压气机压缩空气 → 喷天然气燃烧 → 高温燃气推涡轮旋转发电。单机几十 MW，功率密度最高、最成熟；但设备交付是全行业最紧约束（GE Vernova 订单排到 2028+），单循环效率仅 35-40%。
- **往复式燃气发动机**（VoltaGrid/Jenbacher，2.3 GW 总协议 + Shackelford 210 台/700 MW）：放大版内燃机，活塞往复带动发电机。单机仅 3-4 MW，但恰好命中 AI 痛点：模块化拼装（坏一台不影响全局）、启停快、负载跟随好（AI 训练负荷秒级波动，VoltaGrid 宣称零电池即可平抑）、单机容量小可走"小型源空气许可"加快审批。效率 ~45%，维护量大。
- **固体氧化物燃料电池（SOFC）**（Bloom，2.8 GW 总协议）：**无燃烧**——天然气重整出氢，在 ~800°C 陶瓷电解质中与氧发生电化学反应直接产直流电（新平台 800V DC，契合下一代 AI 机房直流架构）。电效率 50-60%、NOx 极低（Jupiter 口径减排 92%）、几乎不用水（沙漠站点的生死指标）、Bloom 创过 55 天交付纪录。缺点：单位造价高、产能有限、电堆寿命衰减需更换，且**仍烧天然气**——Jupiter 的 17.77 英里输气管道批不下来，2.45 GW 就是无法点火的陶瓷片。
- **为什么三条全押**：不是选型犹豫，而是审批风险对冲——三种技术走不同许可路径（大气源许可 / 小源许可 / 部分州对燃料电池有清洁技术优待），哪条先批哪条先供电。

### 6.4 Stargate 与旗舰项目（库外来源）

- **Stargate 项目**（2025-01-21 官宣）：OpenAI + 软银 + Oracle，宣称四年 $500B、10 GW 美国 AI 基建（[IntuitionLabs 综述](https://intuitionlabs.ai/articles/oracle-openai-300b-deal-analysis)，2025-11-30；[Futurum](https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/)，2026-02-12）。
- **Abilene, TX 旗舰站**：1.2 GW 园区，2026 年初已投运（Crusoe 开发，Oracle 运营 OCI 算力），部署数十万块 Nvidia GB200（GPU 采购约 $40B）。
- **扩张**：2025-07 OpenAI 与 Oracle 追加 4.5 GW，在建容量超 5 GW；至 2026 年初 Stargate 规划近 **7 GW、投资超 $400B**，站点扩至密歇根、威斯康星、怀俄明、宾夕法尼亚、新墨西哥及德州多地（Milam County 由软银旗下 SB Energy 开发 1.2 GW）。
- 值得注意的插曲：微软在 Abilene 隔壁向 Crusoe 租了 900 MW（OpenAI 放弃的扩容选项）——OpenAI 与微软渐行渐远，Oracle 成为 OpenAI 基建主力承接方（IntuitionLabs，C 级来源，细节待更权威来源复核）。

### 6.5 需求侧：OpenAI 集中度

- **OpenAI–Oracle $300B / 5 年合同**（2025-09）：自 2027 年起每年供应约 4.5 GW 算力，是 RPO 暴涨的最大单一来源（[Yahoo Finance](https://finance.yahoo.com/sectors/technology/article/oracle-q4-earnings-beat-on-revenue-but-miss-on-cloud-sales-221337908.html)，2026-06-11）。
- OpenAI 自身状态（决定合同履约能力）：2025 年底 ARR 约 $20B，2026 年初约 $25B；已完成 $122B 融资（估值 $852B）、重组为 PBC；2026-06 已秘密提交 IPO 文件，可能 Q4 2026 上市（IntuitionLabs 2025-11-30；Yahoo 2026-06-11）。
- 风险含义：Oracle 数据中心的故事本质上是**单一客户信用 + 单一技术周期（大模型训练）的双重集中赌注**。穆迪在负面展望中点名的"交易对手风险"（counterparty risk）即指此。Oracle 管理层口径是"AI 客户多元化在推进"，但 RPO 增量大部分仍来自"超大规模 AI 合同"（财报原话）。

### 6.6 资金侧：怎么付这笔钱

- FY2026：发债 $43B + 股权融资 $5B（[Oracle Q4 FY2026 财报](https://www.oracle.com/news/announcement/q4fy26-earnings-release-2026-06-10/)，2026-06-10）。
- CY2026 融资计划（2026-02-01 官宣，少见的前置披露）：一次性投资级债券发行（高盛牵头，实际 $20-25B 于 2026-02 完成）+ **$20B ATM 增发** + 强制可转债（花旗牵头）；公司承诺 2026 日历年不再增发债券（[Oracle IR](https://investor.oracle.com/investor-news/news-details/2026/Oracle-announces-Equity-and-Debt-Financing-Plan-for-Calendar-Year-2026/default.aspx)，2026-02-01；[TwentyFour AM](https://blog.twentyfouram.com/insights/oracle-clears-the-supply-cloud-with-record-demand)，2026-02-03）。
- FY2027 资金安排：Q4 FY2026 时公司预计 FY2027 融资约 $40B（债+股组合，含 $20B ATM）；到 FY2027 Q1，**$20B ATM 已完成**。这不是“尚有 $20B 必定继续举债”的承诺；其余资金缺口取决于 CapEx、经营现金流、客户预付款与后续融资决策。
- 项目级融资（表外化倾向）：2025-11 报道 $38B 银行贷款（摩根大通牵头，Vantage 的威斯康星/德州数据中心）+ $18B 新墨西哥项目债（STACK 开发）——数据中心越来越多以项目融资/租赁结构而非 Oracle 表内 capex 推进（[Octus](https://octus.com/resources/articles/banks-prep-series-of-multibillion-dollar-debt-offerings-for-oracle/)，2025-11-11）。经营租赁负债 $30.2B（FY2026）的暴涨正是这一结构的会计体现；代价见 §4.3（租赁资产不能抵押/出售）。
- 客户预付缓冲：FY2026 Q4 时 RPO 中已有 **$75B** 属"客户预付 GPU 采购款或自带 GPU"的 AI 合同；FY2027 Q1 单季客户预付款（含重大融资成分）为 $11.36B。它们实质上将部分建设资金前置由客户承担，降低 Oracle 自有现金需求，但不降低总资产建设规模（见 §4.1.1）。
- 宏观面：2026 年 AI 相关发债近 $570B（摩根士丹利预测），Oracle 是被信用市场点名"显著再杠杆化"的发行人（[Credence Wire](https://credencewire.com/article/morgan-stanley-ai-debt-issuance-surge-2026)，2026-06-24；[UBS 观点转述](https://www.fi-desk.com/usd-issuance-to-hit-record-highs-in-2026-ubs-predicts/)，2026-01-29）。

### 6.7 小结：数据中心模式的经济学

Oracle 的数据中心业务=**用 BBB- 信用 + 客户长约 + 预付款/项目融资，把 GPU 算力批发给 AI 客户**。$75B 客户预付/自带 GPU、Q1 $11.36B 客户预付款、项目级贷款、经营租赁等结构说明公司在控制自有现金敞口；但 FY2026 FCF -$23.7B、FY2027 指引总 CapEx $90–95B，仍说明敞口巨大。成败取决于：(1) RPO→收入的转化节奏（折旧高峰 vs 收入确认高峰谁先到）；(2) OpenAI 等客户的履约能力；(3) 电力与建设进度（全行业瓶颈）。

## 7. 订单与客户承诺（RPO）

（研究方式.md 第 10 问，对 Oracle 升格为重点章节）

- RPO 轨迹（库外，公司披露）：FY2025 Q4（2025-05）约 $138B → Q1 FY2026 $455B（2025-09，OpenAI 大单落定，单季 +$317B）→ Q2 FY2026 $523B（[穆迪引用](https://www.moodys.com/web/en/us/insights/credit-risk/outlooks/mco-15-december-2025.html)，2025-12-15，S）→ Q3 FY2026 $553B → Q4 FY2026 $638B → **Q1 FY2027 $664B**（环比 +$26B，同比 +$209B）（[Oracle FY2027 Q1 财报](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Q1-Results-Driven-by-Triple-Digit-Growth-in-Cloud-Infrastructure-Revenues/default.aspx)，2026-09-10，S）。
- 转化节奏：公司此前指引 RPO 中仅约 **12% 在未来 12 个月转为收入**（媒体转述财报口径，ifyouspent 2026-07-27）——因此 RPO 大部分仍是多年期收入承诺；以 Q1 FY2027 的 $664B 粗算，不能将其直接等同于当期收入或现金流。
- 对比参照（媒体整理，粗略口径）：RPO/IaaS 年化收入 Oracle 约 110×，微软约 5.7×，AWS 约 4.4×——Oracle 的"承诺/交付"杠杆比同行高一个数量级（[Beancount 整理](https://beancount.io/blog/2026/08/26/oracle-fy2026-q4-earnings-analysis)，2026-08-27，NA 级来源，该文其他数字有明显错误，仅取此对比框架，数值待核）。
- 结构性折价因素：$75B 是预付/自带 GPU 部分（资本风险降，但这部分 RPO 对应的利润率也更接近"托管"而非"云服务"）。

## 8. 估值与资金效率

（按纪律：Reverse DCF 先行，假设显式标记）

- 现状（2026-08-27，【库核实】）：股价 $151.94，市值 $437.7B，PE TTM 26.1；FY2027 指引 non-GAAP EPS $8.05 → 前瞻 PE 约 18.9。EV ≈ 市值 + 净债务 $128B ≈ **$566B**。
- **反推市场预期**：EV $566B 对 FY2027 指引营收 $90B ≈ EV/S 6.3×。若假设【假设】稳态营业利润率回到 32-35%（折旧爬坡后）、【假设】10 年后营收达到 $200B 级（隐含 RPO 大部分转化为收入，FY2027-2036 CAGR 约 9%+）、【假设】WACC 9%，则当前价格大体合理——即**市场已经把 $638B RPO 的成功转化计入价格**，留给"执行失败"的安全边际很薄。
- 估值的另一个参照系是信用市场（见 §4.3）：债券 7-8% 的收益率说明债市给 Oracle 的风险定价比股市苛刻得多——股债两个市场对同一家公司给出了分裂定价。
- 资金效率警讯：FY2026 ROE 因权益基数小（$42.5B）虚高至 40%，无参考意义；更有意义的指标是 ROIC 趋势——CapEx 狂奔期 ROIC 必然被稀释，等 FY2027-28 折旧与收入确认后再看。
- ±30% 规则：未自建完整 DCF 模型（FCF 为负、资本结构剧变中，模型输出噪音大于信号），本节仅做反推预期分析，不给出公允价值结论。

## 9. 值得注意的点

- **治理/股东**：Larry Ellison 仍为最大股东与 CTO，Ellison 家族利益与 OpenAI/Stargate 深度绑定；CEO Clay Magouyrk 出身 OCI，说明公司已把战略重心完全押在云基建上。治理上另一个信用相关点是：公司历史上没有公开财务政策目标（穆迪 2021 年降级理由之一），资本纪律全靠管理层自我约束。
- **TikTok 入股（Deal Radar 命中）**：2026-01-22 TikTok 美国合资公司成立，Oracle/Silver Lake/MGX 各持 15%，字节保留 19.9%；交易估值约 $14B。Oracle 同时承接 TikTok 美国数据托管与算法重训练（在 Oracle 云上）（[ABC News](https://abcnews.com/US/tiktok-signs-deal-create-new-us-joint-venture/story?id=128540504)，2025-12-19；[Harvard HKS](https://www.hks.harvard.edu/centers/carr-ryan/our-work/carr-ryan-commentary/under-us-ownership-tiktok-poses-even-greater-threat)，2026-01-27）。金额对 Oracle 不大，但带来持续的政策/隐私争议敞口。
- **评级风险**：见 §4.3——穆迪 Baa2 负面展望；**标普已于 2026-07-09 降至 BBB-（距垃圾级一档）**；债市已在定价堕落天使风险（30 年债收益率 7.8%，5 年 CDS 破 198bp 创纪录）。
- **裁员与人效**：FY2026 重组费用 $1.84B【10-K核实】，员工据传降至约 14.1 万（二手转述待核）——一边大裁员一边大建数据中心，是典型的"软件公司变公用事业"转型。
- 未发现激进股东介入、针对 Oracle 本身的反垄断审查或进行中的大型并购（Deal Radar，2026-08-31 检索）。

## 10. 我的看法

（整篇【我的推演】，待事实纠正）

1. Oracle 已经不再是"数据库公司上云"的故事，而是"**用软件现金流和 BBB 信用给 AI 基建加杠杆**"的故事。分析它应该用重资产基建股（甚至公用事业）的框架，而不是 SaaS 框架——PE 26 对这个结构不便宜，因为利润表还没反映 $100B PP&E 的折旧高峰。
2. 核心问题只有一个：**$638B RPO 的转化速度 vs $100B+ 资产的折旧速度**。如果 OpenAI 2027 年如期起量（4.5 GW/年），Oracle 营收可以在 FY2028 冲击 $120B+，当前估值说得通；如果 AI 训练需求 2027 年见顶回落，Oracle 是五大厂中资产负债表最脆弱的一家（唯一 FCF 深负 + 评级两档离垃圾）。
3. $75B 客户预付/自带 GPU 是聪明的缓冲，但也说明客户（OpenAI）同样资金紧张——双方是互相担保的关系，一损俱损。
4. 信用市场是更诚实的温度计：股市还在给 26 倍 PE，债市已经按准垃圾级收 7-8% 利息。历史上债市对资本结构恶化的判断通常比股市早。跟踪 Oracle 的正确姿势是盯债券利差/CDS，而不是盯财报 beat/miss。
5. 我不具备判断"AI 算力需求 2027-2028 是否持续"的信息优势，所以对 ORCL 不下买卖结论；但会把它放进"AI 资本开支链条风险敞口最大者"的观察名单，跟踪三个先行指标：季度 RPO 环比增量、FY2027 实际融资节奏 vs $40B 计划、OCI IaaS 增速是否守住 50%+。

## 11. 跳过的模块及原因

- **护城河与竞争壁垒**：数据库存量粘性是真实护城河（软件支持费 $19.8B/年、零增长但极稳定，见 §3.2），但本项目的投资问题在数据中心，存量业务护城河已被充分讨论过，暂不深挖。
- **完整 DCF 估值**：FCF 为负且资本结构剧变中，模型噪音大于信号（见 §8）。
- **客户结构（独立章节）**：并入 §6.3/§7——Oracle 客户集中问题当前≈OpenAI 单客户问题，无需重复。

## 12. 后续研究方向

- 确认 FY2026 非经营净收益 +$3.5B 的具体构成（10-K 附注，疑为 Ampere 股权处置收益）→ 据此把 FY2026"经营性净利"还原出来
- FY2026 10-K 原文核对：员工数 14.1 万、RPO 12 个月转化比例
- 数据中心项目融资的表外化程度：Vantage/STACK/Crusoe 各项目中 Oracle 的担保与最低租赁承诺
- Q1 FY2027 已核对：RPO $664B、IaaS $7.4B（+121%）、$20B ATM 完成、850 MW 新容量交付；下一步跟踪 Q2 的 RPO 转化、总/净 CapEx、客户预付款与 FCF 是否继续背离
- 建立 Oracle 债券利差/CDS 跟踪（债市定价是先行指标，见《我的看法》第 4 条）
- 与 [CRWV](/Users/vinci/Documents/stock_research/CRWV) / [数据中心](/Users/vinci/Documents/stock_research/数据中心) 项目交叉：neocloud 与 hyperscaler 的单位经济学对比
- 电力侧：Oracle 各站点的电力来源安排（核电/燃气/PPA）——行业瓶颈变量

## 13. 数据来源与核实记录

### 来源清单

**一手/库数据**

- stock_data 库（ssh my-t-vinci）：`us_financial_current_annual` / `us_financial_current_ttm` / `us_financial_fact_version` / `daily_quote`，2026-08-31 取数【库核实】
- SEC XBRL companyfacts（CIK 0001341439）：债务与租赁负债年度值，2026-08-31 下载，本地存档 [orcl_companyfacts.json](/Users/vinci/Documents/stock_research/ORCL/factcheck/data/orcl_companyfacts.json)
- Oracle FY2026 10-K（accession 0001193125-26-277521，2026-06-22 提交）：利润表（R4）、分部信息（R86）、收入明细附注（R89），2026-08-31 从 EDGAR 提取【10-K核实】，R 文件存档于 `factcheck/data/`
- [Oracle Q4/FY2026 财报新闻稿](https://www.oracle.com/news/announcement/q4fy26-earnings-release-2026-06-10/)（2026-06-10）：RPO、云收入拆分、融资额、$75B 预付款
- [Oracle FY2027 Q1 财报新闻稿](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Q1-Results-Driven-by-Triple-Digit-Growth-in-Cloud-Infrastructure-Revenues/default.aspx)（2026-09-10）：营收/云收入/RPO、850 MW 容量、$20B ATM 完成、GAAP 经营现金流与 FCF
- [Oracle FY2027 Q1 财报 PDF](https://investor.oracle.com/files/content_files/1q27-pressrelease-September_FINAL.pdf)（2026-09-10）：总 CapEx、客户预付款与“净现金 CapEx”定义及数值
- [Oracle CY2026 融资计划公告](https://investor.oracle.com/investor-news/news-details/2026/Oracle-announces-Equity-and-Debt-Financing-Plan-for-Calendar-Year-2026/default.aspx)（2026-02-01）
- [穆迪 2021 年降级公告](https://finance.yahoo.com/news/oracle-corporation-moodys-downgrades-oracles-120807586.html)（2021-03-22，S）；[穆迪信用展望周报](https://www.moodys.com/web/en/us/insights/credit-risk/outlooks/mco-15-december-2025.html)（2025-12-15，S）

**媒体/研究（按引用处标注的日期与级别）**

- Yahoo Finance（2026-06-11，S）；Economic Times（2026-08-05，A）；Futurum（2026-02-12，B）；Octus（2025-11-11）；TwentyFour AM（2026-02-03）；ABC News（2025-12-19，B）；Harvard HKS（2026-01-27，S）
- C/NA 级（使用时已注明或标记待核）：IntuitionLabs（2025-11-30，C）；etfpedia（2026-06-11）；ifyouspent（2026-07-27，NA）；Axis Intelligence（2026-07-27，NA）；Credence Wire（2026-06-24，NA）；Deepstory Research（2026-08-06，NA）；Beancount（2026-08-27，NA，仅取对比框架）；Market Supply Chain（2026-06-25，NA）

### 核实记录

- 2026-08-31：建项目文件夹与骨架。
- 2026-08-31：刷新数据库 schema——旧表 `us_income_statement` 等已删除，美股数据迁往 `us_financial_current_*` + `us_financial_fact_version`；通用三报表（income_statement 等）现为 A 股/港股口径（无 ORCL 数据）。SOP 的 database.md 已于当日同步重写。
- 2026-08-31：完成首轮取数（5 财年年度 + FY2026 季度拆分 + 债务/租赁 + 同行对比）与首轮外部检索（Deal Radar + 数据中心专题），成稿 v1。已核对：FY2026 营收/净利/CapEx/FCF 库值与公司财报新闻稿一致（$67.4B / $17.1B / $55.7B / -$23.7B ✅）。
- 2026-08-31（v2，回应"收入结构缺失 + 评级为何低"两个问题）：
  - 从 FY2026 10-K 利润表（R4）与收入附注（R89）补齐四条收入线 + 云内部 IaaS/SaaS 拆分（§3.2），云合计与公司披露 $34.0B 勾稽一致 ✅；
  - 新发现：FY2026 非经营净收益 +$3.5B、重组费用 $1.84B、优先股股息 $0.1B【10-K核实】，Q2 净利异常的一次性收益来源基本锁定（§3.1）；
  - 新增 §4.3 信用评级分析：2021 年举债回购降级史 + 当前穆迪/标普/惠誉口径 + 堕落天使风险的市场证据；股价 6-7 月最大回撤 -52% 用库数据复算 ✅（244.58→117.74）。
- 2026-08-31（v3，物理产能专题）：新增 §6.2"物理产能台账：GW 与 GPU"——分层整理电力容量（投运 1.2 GW / 已签约 4.5 GW / 燃料电池采购 2.8 GW / Stargate 规划近 7 GW）与 GPU 数量（单集群上限 131K→800K、Abilene 实际部署 64K GB200、采购承诺约 400K GB200/$40B、舰队数十万至 1M+），并给出 GW↔GPU 换算框架；小节重编号（原 6.2-6.5 → 6.3-6.6）。
- 2026-08-31（v4，10-K 承诺附注深挖）：从 R64/R69 提取并核实——**未起租经营租赁承诺 $260B**（15-19 年租期，表内仅 $30.2B）、融资租赁负债 $7.7B、出租方借款担保 $3.3B（2026-09 到期）、无条件采购义务 $13.3B + 期后新增 $19B。结论：Bloomberg"40 万块 GB200/$40B"无法与一手文件勾稽（⚠️），采购口径以 10-K 的 $13.3B+$19B 为准；§4.2 新增表外承诺段。
- 2026-09-01（v5，两年股价复盘）：新建独立专题文档 [股价复盘-2024-2026.md](/Users/vinci/Documents/stock_research/ORCL/股价复盘-2024-2026.md)（六幕时间线，全部转折点收盘价库核实）；**重要更新：标普 2026-07-09 已降级 BBB→BBB-（展望稳定）**，§4.3/§9 评级相关内容已修正——此前 v1-v4 的"标普 BBB 负面展望"口径已过时；补充 OpenAI 约占 RPO 一半、FY2027 capex $90-95B（S&P 口径）、OpenAI 年付款义务 ~$60B vs 其年化收入 ~$24B 等关键事实。
- 2026-09-01（v6，neocloud 估值对比）：§5 新增 5.1"与 neocloud 的估值分层"——ORCL/CRWV/NBIS 三家同口径对比（市值、增速、P/S、EV/Backlog、资产负债表），回答"逻辑相近为何定价不同"。CRWV/NBIS 财务取库 fact_version（FY25 年报 + 26H1 季报），报价用 Yahoo（2026-09-01）；注意 daily_quote/us_financial_current_* 未覆盖 CRWV/NBIS（行情与精选表缺口，fact_version 有数）。
- 2026-09-02（v7，电力来源专题）：新增 §6.3"电力从哪来"（小节重编号 6.3-6.6 → 6.4-6.7）。核心结论：以天然气为主，"电网专线 + 现场自发电"两条腿；Bloom 燃料电池总协议 2.8 GW（烧气不烧氢）、VoltaGrid 燃气 2.3 GW、Energy Transfer 供气长约 900 MMcf/d、Jupiter 因输气管道与空气许可被 SemiAnalysis 推迟至 2029。已下载 10-K 主文档 [orcl_10k_main.htm](/Users/vinci/Documents/stock_research/ORCL/factcheck/data/orcl_10k_main.htm) 全文检索——10-K 不点名任何电力项目，仅风险章节通用表述。Oracle 无已披露核电合同。同日补充 §6.3 附录"三种现场发电技术的原理与取舍"（燃气轮机/往复式发动机/SOFC 燃料电池的原理、效率、审批路径差异）——属技术常识整理，非 Oracle 披露口径。
- 2026-09-02（v8，电力供应链跟踪表）：新建独立文档 [电力供应链跟踪表.md](/Users/vinci/Documents/stock_research/ORCL/电力供应链跟踪表.md)——按环节（气源/燃料电池/燃气发电/电网/开发商）整理供应商承诺容量、交付里程碑、审批闸门与 7 条可核查监控点（含"被打脸信号"和应对动作）。新发现：Milam 站点由 SB Energy 负责"综合能源交付"（OpenAI+软银各投 $500M，拟 IPO），首栋楼目标 2026-10；GE Vernova 重型涡轮售罄至 2028、新订单交期 ~3 年（行业层约束）；Bloom 产能 2026 年底翻倍至 2 GW/年、总 backlog ~$20B。站点容量口径更新：Shackelford 2.0 GW / Jupiter 2.2 GW / Port Washington 1.3 GW / Saline Township 1.4 GW（Epoch AI 卫星分析口径，与 §6.2 旧口径差异已标注待核）。
- 2026-09-02（v9，目录整理）：按 AGENTS.md 第 2 条约定，将 14 个 10-K 原始文件（R*.htm、FilingSummary.xml、orcl_10k_main.htm、orcl_companyfacts.json）从项目根层收进 `factcheck/data/`；删除 330 字节空壳 FY2026_10K_Financial_Report.xlsx；ORCL.md 内两处文件链接与"R 文件存档位置"表述已同步更新。根层现仅存三份研究文档：ORCL.md、股价复盘-2024-2026.md、电力供应链跟踪表.md。
- 2026-09-15（v10，FY2027 Q1 与资本配置更新）：补充 FY2027 Q1 的经营现金流 $23.10B、总 CapEx $28.50B、GAAP FCF -$5.40B、客户预付款 $11.36B 与公司“净现金 CapEx”$17.97B；明确后者不能替代 FCF，避免在经营现金流中重复计算预付款。更新 FY2027 指引为总 CapEx $90–95B、净现金 CapEx 不超过 $70B（管理层电话会二手转录），并记录 FY2027 营收“至少 $90B”、non-GAAP EPS $8.10 的管理层指引；补充 FY2026 FCF 为负仍分红的总体资金来源分析，以及 Q1 RPO $664B、850 MW 新容量和 $20B ATM 完成情况。
