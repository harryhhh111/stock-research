# Western Digital（WDC）研究笔记

> 2026-10-05 补充：已新增[东芝研究](东芝.md)。东芝官方于 2026-10-02 确认菲律宾新增近线 HDD 产线首次出货；原文的供给纪律判断需结合第三家厂商扩产重新审视。原文财务、行情与估值仍保留原截止日。

> 整理/核对日期：2026-08-27
> 行情数据截止：2026-08-26（stock_data 库）；财务数据截止：FY2026（财年截至 2026-07-03，53 周）
> 口径说明：2025-02-21 Sandisk（SNDK）分拆后，WDC = 纯 HDD 公司。FY2023–FY2026 为公司重述的 HDD continuing operations 口径；FY2022 用分拆时披露的 unaudited pro forma HDD-only 数据。金额单位统一为 $B（十亿美元）。
> 库口径差异：stock_data 库 `us_financial_current_annual` 的 FY2021/FY2022 是分拆前 HDD+Flash 合并口径（$16.9B / $18.8B），与本笔记 FY2022 pro forma HDD-only（$9.04B）不可直接比较；库 FY2023–FY2025 收入/毛利率/营业利润率与本笔记一致【库核实】；库的 net_income 含已终止业务（FY2023 库 -$1.68B vs 持续经营 -$0.90B；FY2025 库 $1.89B vs 持续经营 $1.64B），正文以持续经营口径为准并标注。

## 目录

1. 公司概览
2. 业务模块（Cloud / Client / Consumer 与技术路线）
3. 行业供需框架（强周期核心章）
4. 周期位置判断
5. 营收情况
6. 盈利与负债
7. 客户结构与集中度
8. 订单与客户承诺
9. 竞争对手与同行对比（Seagate / Toshiba）
10. 资本分配与 Deal Radar
11. 估值与资金效率
12. 我的看法（【我的推演】）
13. 跳过的模块及原因
14. 后续研究方向
15. 数据来源与核实记录

---

## 1. 公司概览

一句话：

> **Western Digital 现在是一家以大容量 HDD 机械硬盘为核心、主要给云计算和 AI 数据中心提供海量存储的公司。**

- 成立于 1970 年，总部美国加州 San Jose，NASDAQ: WDC。
- **2025-02-21 完成 Sandisk 分拆**：原 NAND Flash / SSD 业务成为独立上市公司 Sandisk（SNDK）。分拆后 WDC = HDD，SNDK = NAND/SSD，两家公司必须分开分析。([WDC 官网](https://investor.wdc.com/news-releases/news-release-details/western-digital-completes-planned-company-separation))
- FY2026 营收 **$12.92B**，其中 Cloud 占 **89%**——不要再把 WDC 当成"给消费者卖 WD 蓝盘、移动硬盘的公司"，那已经不是核心业务。

**它是数据中心上游公司**，需求链条：

> Microsoft / Google / Amazon / Meta 等 hyperscaler 建 AI/Cloud 数据中心 → 数据量增加 → 需要 PB/EB 级存储 → Seagate / WDC 提供大容量 HDD。

---

## 2. 业务模块

（本章只解释业务是什么、卖给谁、怎么赚钱；经营数据见第 5 章营收。）

### 2.1 Cloud（核心，FY2026 占 89%）

- 客户：hyperscaler 超大规模云厂商、云服务商、neocloud、大型企业数据中心；公司披露客户类型含 hyperscale CSP、neoclouds、OEM、经销商。([FY2026 10-K](https://financialfilings.com/filings/western-digital-corp/annual-report/2026/56179556/))
- 产品：**Ultrastar 企业级大容量 HDD**（26TB / 28TB / 32TB / 36TB / 40TB…）。
- 核心指标不是"卖了多少块盘"，而是 **卖出了多少 Exabyte（EB）**。逻辑和 NAND 的 bit shipment + ASP 完全一样：**Drive 数量 × TB/drive × $/TB**。

**为什么 AI 数据中心还需要机械硬盘**——存储分层：

```
GPU → HBM → 高速 NVMe SSD → HDD 大容量存储 → 归档/冷数据
```

SSD 解决"快"，HDD 解决"便宜地存非常多"。HDD 承载：原始训练数据、图片/视频数据集、数据湖、模型 checkpoint 长期保存、日志、推理生成内容、备份、大规模对象存储。数据量越大，$/TB 越重要。公司把 AI 数据增长视为 HDD 长期需求核心驱动，预测 HDD exabyte shipment 2024–2028 CAGR 约 **23%**（公司预测，不是事实）。([Investor Day 2025](https://investor.wdc.com/news-releases/news-release-details/western-digital-unveiled-go-forward-strategy-investor-day-2025))

### 2.2 Client（约 6%）/ Consumer（约 5%）

PC/客户端 HDD、品牌移动硬盘等。两块合计约 11%，且占比持续下降，已不是投资逻辑的一部分。

### 2.3 制造体系：重资产垂直整合

不是 NVIDIA 式"自己设计 → 代工"。WDC 的 HDD assembly 和 testing 是 **vertically integrated、in-house**（[FY2026 10-K](https://financialfilings.com/filings/western-digital-corp/annual-report/2026/56179556/)），核心竞争力 = 磁头 + 磁盘介质 + 精密机械 + 固件 + 组装 + 测试 + 大规模量产。制造基地：泰国（Bang Pa-In、Prachinburi）、马来西亚（Penang、Johor Bahru、Kuching）、菲律宾（Laguna）、中国深圳、美国（San Jose、Fremont）。**本质上是重资产精密制造公司。**

### 2.4 技术路线：ePMR / UltraSMR → HAMR

- 当前主力：**ePMR**（能量辅助垂直磁记录）+ **UltraSMR**（提高单盘面密度）。
- 未来：**HAMR**（热辅助磁记录）。Seagate 在 HAMR 上更激进，WDC 过去更多靠 ePMR/UltraSMR 延续容量提升；WDC 已让两家大型 hyperscaler 测试 HAMR，并已开始在两家 hyperscaler 做 40TB UltraSMR qualification、出货 40TB ePMR 产品。([Investor Day 2025](https://investor.wdc.com/news-releases/news-release-details/western-digital-unveiled-go-forward-strategy-investor-day-2025))([Innovation Day](https://investor.wdc.com/static-files/f010ae83-c695-4c08-b1cf-cb4091940da5))
- 公司给的平均 Nearline 容量路线：**23TB → 32TB → 40TB → 44TB → 100TB+**，并明确写 Higher TB/drive → Lower TCO → Better Profitability。
- 关键研究问题：**Seagate 的 HAMR 是否领先 WDC？WDC 能否靠 ePMR/UltraSMR 继续推容量而不付出过高成本？** 这直接决定两家的成本/TB。

---

## 3. 行业供需框架（强周期核心章）

**判定：HDD 适用强周期变体**——产品高度商品化、供给由三寡头产能与 TB/drive 路线图决定、经营杠杆极大。核心问题是周期位置。

### 3.1 需求测算框架（可复算）

```
WDC 营收 ≈ HDD EB 出货量 × Revenue/EB
其中 EB 出货 ≈ Drive 数量 × 平均 TB/drive
```

FY2026 验证：EB sold **+25%** × ASP/EB **+8%** ≈ 1.25×1.08 ≈ **+35%**，对应营收 +36%，增长结构非常干净。([FY2026 10-K](https://www.sec.gov/Archives/edgar/data/106040/000162828026057139/wdc-20260703.htm))

上游需求驱动：AI/Cloud 数据量 → 数据中心需要多少 EB 存储 → 其中多少用 HDD → 全球 Nearline HDD 需求 → WDC/STX/Toshiba 份额。

### 3.2 供给：三寡头

全球能大规模生产 HDD 的只有 **Seagate、Western Digital、Toshiba** 三家（WDC 10-K 列出的直接竞争对手即 Seagate 与 Toshiba Electronic Devices & Storage）。([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/106040/000010604025000038/wdc-20250627.htm)) hyperscale 高容量段主要是 WDC vs Seagate，Toshiba 规模较小。

供给端一个重要特点：**EB 产能不只靠建厂**。同样一块盘从 20TB 变 30TB，EB capacity 就 +50%。所以 HDD 供给 = 产线产能 × TB/drive 路线图。FY2026 WDC CapEx 仅 $418M（收入的 3.2%），公司长期模型 CapEx 为收入的 4%–6%——远低于 NAND 行业的资本强度。([FY2026 10-K](https://www.sec.gov/Archives/edgar/data/106040/000162828026057139/wdc-20260703.htm))

### 3.3 经营杠杆（这个行业最重要的财务特征）

FY2023 谷底揭示了机制：数据中心客户前期备货后去库存，EB -26%，而制造固定成本照旧，出现 **unabsorbed manufacturing overhead**——FY2023 约 $200M、FY2024 约 $155M，FY2025 基本消失（FY2025 毛利率 +10.7pct 中约 2.5pct 仅来自未吸收制造费用不再发生）。([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/106040/000010604025000038/wdc-20250627.htm))

> 下行：EB ↓ → 产能利用率 ↓ → 单位成本 ↑ → 毛利率暴跌
> 上行：EB ↑ → utilization ↑ → 单位成本 ↓ → 毛利率猛涨

FY2026 毛利率 +10.1pct 的解释：shipment volume 上升 + 新一代产品成本结构更好 + mix 转向更大容量 + pricing 改善。([FY2026 10-K](https://www.sec.gov/Archives/edgar/data/106040/000162828026057139/wdc-20260703.htm))

---

## 4. 周期位置判断

### 4.1 五阶段复盘（FY2022→FY2026 是一个完整的"衰退—触底—复苏—景气"）

| 阶段 | FY | 发生了什么 |
|---|---|---|
| 上一轮高位 | FY22 | 557 EB，收入 $9.0B（pro forma HDD-only） |
| **崩盘** | **FY23** | EB -26%，营收 -31%，GM 跌到 22.2%，营业亏损 |
| **底部** | FY24 | EB +7.5% 小幅恢复，利润仍为负 |
| **量复苏** | **FY25** | EB +57%，Cloud +65%，GM → 38.8% |
| **量价齐升** | **FY26** | EB +25%，ASP/EB +8%，GM → **48.9%** |
| 当前 run-rate | Q4FY26 | 231 EB/季（Nearline 209 EB，占 90.5%），GM **54%+** |

([SEC 分拆 pro forma 8-K](https://www.sec.gov/Archives/edgar/data/106040/000010604025000012/wdc8-khardxspin.htm))([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/106040/000010604025000038/wdc-20250627.htm))([FY2026 10-K](https://www.sec.gov/Archives/edgar/data/106040/000162828026057139/wdc-20260703.htm))([Q4'26 Earnings Deck](https://investor.wdc.com/static-files/e1f02f77-4432-42c3-8bd4-024371f40e54))

注意：FY2026 为 53 周（FY2024/25 为 52 周），同比有一点额外周数帮助。

### 4.2 两种互斥解释（全文最关键的分歧）

**解释 A：结构性变化。** AI 数据量增长 → hyperscaler HDD EB 长期 +20%+ → 寡头控制供给、不再恶性扩产 → ASP 稳定 → 毛利率永久抬升到 ~50%。若为真：今天的 WDC 已不是过去那个周期股。

**解释 B：超级上行周期顶部。** hyperscaler 补库存 + AI 资本开支狂潮 + 供给紧 → ASP 涨、utilization 拉满、GM 暂时 50%+；未来云厂商库存恢复 + 供给增加 → ASP 转跌、GM 回 ~30%。若为真：**拿 FY2026/Q4 利润算 PE 会非常危险。**

管理层显然押注 A：2026 Innovation Day 给的 3–5 年目标模型为 Revenue CAGR >20%、Nearline EB CAGR mid-20s、GM >50%、OM >40%、FCF Margin >30%（**公司目标，不能直接当预测**）。([Innovation Day](https://investor.wdc.com/static-files/f010ae83-c695-4c08-b1cf-cb4091940da5))

支持 A 的新证据：长约能见度显著提高（见第 8 章）。支持 B 警惕的证据：客户集中度快速上升（第 7 章）、2026 年 7–8 月股价从高点回撤约 26%（市场已在重新定价）。

### 4.3 当前判断

FY2025 的利润恢复还可以解释成周期反弹；但 FY2026 出现了定价改善 + 产品 mix 改善 + 结构性 Cloud/AI 需求，且 Q4 + FY2027 Q1 指引显示利润率仍在扩张（Q1FY27 指引：营收 $4.1B±$0.1B、Non-GAAP GM 55%–56%、EPS $4.00±$0.15）。([Q4'26 Earnings Deck](https://investor.wdc.com/static-files/e1f02f77-4432-42c3-8bd4-024371f40e54)) **周期仍在上升段，尚无非拐头信号；但估值已把解释 A 定价得相当满（见第 11 章）。**

---

## 5. 营收情况

### 5.1 五年总表（HDD 口径）

| 财年 | 营收 ($B) | YoY | HDD 出货 | YoY | 毛利率 | 营业利润率 |
|---|---:|---:|---:|---:|---:|---:|
| FY2022* | 9.04 | — | 557 EB | — | 28.0% | +4.5% |
| FY2023 | 6.26 | -30.8% | 412 EB | -26.0% | 22.2% | -8.8% |
| FY2024 | 6.32 | +1.0% | 443 EB | +7.5% | 28.1% | -6.4% |
| FY2025 | 9.52 | +50.7% | 696 EB | +57.1% | 38.8% | +24.5% |
| FY2026 | 12.92 | +35.7% | ≈872 EB | ≈+25% | 48.9% | +34.5% |

\* FY2022 为分拆 pro forma HDD-only（库中 FY2022 为 $18.79B 合并口径，勿混用）。FY2023–25 收入/毛利率/营业利润率【库核实】（库 `us_financial_current_annual`：6.255/22.2%/-8.8%；6.317/28.1%/-6.4%；9.520/38.8%/24.5%）。FY2026 库中尚无年报行，用 10-K/财报披露；EB 全年 +25% 为公司披露，≈872 为四个季度整数相加，有四舍五入误差。([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/106040/000010604025000038/wdc-20250627.htm))([FY2026 10-K](https://www.sec.gov/Archives/edgar/data/106040/000162828026057139/wdc-20260703.htm))

毛利率轨迹 **22.2% → 28.1% → 38.8% → 48.9%（Q4 单季 54.1%）** 是本轮盈利爆发的核心。

### 5.2 分部营收五年变化（比总营收更重要）

| 财年 | Cloud ($B) | 占比 | Client ($B) | 占比 | Consumer ($B) | 占比 |
|---|---:|---:|---:|---:|---:|---:|
| FY2022* | 6.75 | 74.7% | 1.04 | 11.5% | 1.25 | 13.8% |
| FY2023 | 4.75 | 76.0% | 0.69 | 11.0% | 0.81 | 13.0% |
| FY2024 | 5.05 | 80.0% | 0.58 | 9.1% | 0.69 | 10.9% |
| FY2025 | 8.34 | 87.6% | 0.56 | 5.8% | 0.62 | 6.5% |
| FY2026 | 11.49 | **88.9%** | 0.73 | 5.6% | 0.70 | 5.4% |

\* FY2022 三分部为重构值：当年 WDC 总端市场收入减去 Sandisk carve-out 披露的 Flash 收入（Cloud 8.017−1.264=6.753；Client 7.076−6.038=1.038；Consumer 3.700−2.452=1.248），三项正好等于 pro forma $9.039B。([FY2022 10-K](https://www.sec.gov/Archives/edgar/data/106040/000010604022000055/wdc-20220701.htm))

Cloud 占比 75% → 89%：Client HDD 和移动硬盘对投资逻辑已不重要，真正的问题是 **hyperscaler 要买多少 EB Nearline HDD**。

### 5.3 EB 与"ASP"拆解

用 年收入 ÷ EB 算 **Revenue/TB proxy**（非公司官方 ASP，仅为观察"每 TB 实现多少收入"的近似）：

| 财年 | HDD EB | 营收 ($B) | 隐含 Revenue/TB |
|---|---:|---:|---:|
| FY2022 | 557 | 9.04 | $16.23/TB |
| FY2023 | 412 | 6.26 | $15.18/TB |
| FY2024 | 443 | 6.32 | $14.26/TB |
| FY2025 | 696 | 9.52 | $13.68/TB |
| FY2026 | ≈872 | 12.92 | ≈$14.82/TB |

**一个容易误解的点**：FY2025 公司披露 ASP **per unit +29%**（Cloud 单位出货 +36%、ASP/unit +20%），但 Revenue/TB 反而约 -4%。不矛盾——客户转向更高容量盘：单盘从 18TB/$270 变成 28TB/$350，每块盘 ASP 大涨，但 $/TB 下降。所以盯 WDC 要同时看 **Drive 数量 × TB/drive × $/TB**，不能只看"卖了多少块盘"。([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/106040/000010604025000038/wdc-20250627.htm))

FY2026 是关键转折：$/TB 五年来首次回升（$13.68 → ≈$14.82），公司官方口径 ASP/EB +8%。

### 5.4 FY2026 逐季加速

| FY2026 | Revenue ($B) | HDD EB | Nearline EB | Non-GAAP GM | FCF ($M) |
|---|---:|---:|---:|---:|---:|
| Q1 | 2.818 | 204 | 183 | 43.9% | 599 |
| Q2 | 3.017 | 215 | 192 | 46.1% | 653 |
| Q3 | 3.337 | 222 | 199 | 50.5% | 978 |
| Q4 | **3.747** | **231** | **209** | **54.4%** | **1,281** |

Q4FY25→Q4FY26：季度 EB 190 → 231，GM 41.3% → 54.4%；Q4 Nearline 209/231 ≈ **90.5%**，出货容量约九成已是数据中心级 HDD。([Q4'26 Earnings Deck](https://investor.wdc.com/static-files/e1f02f77-4432-42c3-8bd4-024371f40e54))

---

## 6. 盈利与负债

### 6.1 GAAP 利润序列（含失真警示）

| 指标 ($B) | FY2023 | FY2024 | FY2025 | FY2026 |
|---|---:|---:|---:|---:|
| Revenue | 6.26 | 6.32 | 9.52 | 12.92 |
| Gross profit | 1.39 | 1.77 | 3.69 | 6.31 |
| Operating income | -0.55 | -0.40 | 2.33 | 4.45 |
| Operating margin | -8.8% | -6.4% | 24.5% | 34.5% |
| 持续经营净利润 | -0.90 | -0.77 | 1.64 | **9.42*** |

⚠️ **FY2026 的 $9.42B 净利润不能拿来算 PE**（硬规则 7：NI 远超 OP，必查非经营项）：FY2026 含 **$6.50B Sandisk retained-interest gain**（分拆后保留的 SNDK 股票市价变动及处置收益），GAAP 净利润严重失真。([FY2026 10-K](https://www.sec.gov/Archives/edgar/data/106040/000162828026057139/wdc-20260703.htm)) 同理，库 daily_quote 的 PE TTM 19.3（2026-08-26）用的就是这个失真净利润，**不代表真实估值水平**。

### 6.2 核心盈利看 Non-GAAP

| 指标 | FY2025 | FY2026 | YoY |
|---|---:|---:|---:|
| Revenue ($B) | 9.520 | 12.919 | +36% |
| Non-GAAP gross margin | 39.4% | 49.1% | +9.7pct |
| Non-GAAP operating income ($B) | 2.326 | 4.817 | +107% |
| Non-GAAP operating margin | 24.4% | 37.3% | +12.9pct |
| Non-GAAP EPS | $5.02 | $10.22 | +104% |
| CFO ($B) | 1.691 | 3.929 | +132% |
| FCF ($B) | 1.432 | 3.511 | +145% |

([Q4'26 Earnings Deck](https://investor.wdc.com/static-files/e1f02f77-4432-42c3-8bd4-024371f40e54)) 经营杠杆：营收 +36% → 营业利润 +107% → FCF +145%。

**FCF 口径警示**：历史现金流量表未把 discontinued Sandisk 现金流完全 segregate（FY2025 FCF 含 SNDK 至 2025-02-21 分拆日）。**FY2026 的 $3.511B 是最干净的纯 HDD 参考值**；FY2025 看趋势；FY2022–24 的 FCF 对今天的 WDC 估值意义不大。库 TTM（截至 2026-04-03）：revenue $11.78B、FCF $2.905B【库核实】。

### 6.3 资产负债表（库口径）

| 财年 ($B) | 总资产 | 总负债 | 净资产 | 负债率 | 流动比率 |
|---|---:|---:|---:|---:|---:|
| FY2024 | 24.19 | 13.14 | 10.82 | 54.3% | 1.32 |
| FY2025 | 14.00 | 8.46 | 5.31 | 60.4% | 1.08 |

分拆后总资产从 $24.2B 缩到 $14.0B（Flash 资产出表），负债率 60.4%、流动比率 1.08，单看报表偏紧——但 2026 年 2 月 debt-for-equity exchange 用 SNDK 股票退役了约 **$31 亿债务**（见第 10 章），实际杠杆已显著低于 FY2025 报表。FY2025 ROE（库口径）35.6%。

### 6.4 CapEx 与资金效率

FY2026：CFO $3.929B、CapEx $418M（收入 3.2%）、FCF $3.511B。公司长期模型 CapEx 为收入 4%–6%。**HDD 扩 EB 不一定靠扩厂，TB/drive 提升本身就是产能**——资本强度远低于 NAND/代工，这是 HDD 双寡头商业模式被低估的一点。

---

## 7. 客户结构与集中度（可选模块：启用——客户集中是投资关键）

| 财年 | Top 10 客户占营收 |
|---|---:|
| FY2023 | 56% |
| FY2024 | 55% |
| FY2025 | 68% |
| FY2026 | **73%** |

FY2026 前三大客户分别 **16% + 15% + 13% = 44%**（FY2025 为 17%+12%+10%=39%）。公司不披露大客户名字。([FY2025/FY2026 10-K](https://www.sec.gov/Archives/edgar/data/106040/000162828026057139/wdc-20260703.htm))

- 好处：hyperscaler 采购量巨大，且开始签更长期 supply commitment（第 8 章）。
- 坏处：对少数客户的采购节奏、qualification、话语权高度敏感——一个 15% 营收的客户去库存，冲击会非常大。集中度快速上升是 Cloud 占 89% 的另一面。

---

## 8. 订单与客户承诺（可选模块：启用——长约是判断"解释 A vs B"的关键先行指标）

Q2 FY2026 财报电话会（2026-01-30）管理层披露：

- **前七大客户已有覆盖到 2026 日历年年底的 firm purchase orders**；
- 前五大客户中三家有正式商业长约：**两家到 CY2027 年底，一家到 CY2028 年底**；
- UltraSMR-enabled JBOD 平台发布，把 UltraSMR 推向更广客户群。

([Motley Fool Q2'26 电话会实录](https://www.fool.com/earnings/call-transcripts/2026/01/30/western-digital-wdc-q2-2026-earnings-transcript/))

这是"解释 A（结构性）"最有力的实据：需求能见度从季度订单变成了 1–3 年长约。反方注意点：LTA 在 HDD 史上也出现过（2021–22 年），下行期客户仍会 renegotiate 或消化库存——**长约改善的是能见度，不是免疫周期**。

---

## 9. 竞争对手与同行对比

### 9.1 格局

三寡头：Seagate、WDC、Toshiba。高容量 Nearline 主战场是 **WDC vs Seagate**。技术路线分叉：Seagate 押注 HAMR 更激进（已量产推进），WDC 以 ePMR/UltraSMR 延续 + HAMR 跟进（两家 hyperscaler 测试中）。**HAMR 竞赛结果决定未来两家成本/TB 曲线。**

### 9.2 WDC vs STX 五年对比【库核实，库口径】

| 公司 FY | 营收 ($B) | 毛利率 | 营业利润率 | 净利润 ($B) | FCF ($B) |
|---|---:|---:|---:|---:|---:|
| STX FY2022 | 11.66 | 29.7% | 16.8% | 1.65 | 1.28 |
| WDC FY2022* | 18.79 | 31.3% | 12.7% | 1.55 | 0.76 |
| STX FY2023 | 7.38 | 18.3% | -4.6% | -0.53 | 0.63 |
| WDC FY2023 | 6.26 | 22.2% | -8.8% | -1.68** | -1.23 |
| STX FY2024 | 6.55 | 23.4% | 6.9% | 0.34 | 0.66 |
| WDC FY2024 | 6.32 | 28.1% | -6.4% | -0.80** | -0.78 |
| STX FY2025 | 9.10 | 35.2% | 20.8% | 1.47 | 0.82 |
| WDC FY2025 | 9.52 | 38.8% | 24.5% | 1.89** | 1.28 |
| STX FY2026 | 12.20 | 45.6% | 33.6% | 3.18 | 3.11 |
| WDC FY2026*** | 12.92 | 48.9% | 34.5% | 9.42** | 3.51 |

\* WDC FY2022 库口径为分拆前 HDD+Flash 合并值。\*\* WDC 库净利润含已终止业务/一次性损益，与持续经营口径有差异（FY2026 含 $6.5B SNDK 收益）。\*\*\* WDC FY2026 为 10-K 外部披露（库尚无年报行）。FY 截止日两家均为 6 月底/7 月初，基本可比。

读法：

- 两家周期形态完全同步（FY23 同崩、FY25–26 同爆），**这是行业 beta，不是某家的 alpha**。
- FY2026 WDC 营收、毛利率、FCF 均略高于 STX；但市场对 STX 定价更贵（市值 $191.8B vs WDC $169.1B，2026-08-26 库口径；STX PE TTM 60.9）。
- 把 WDC + STX 一起研究清楚，基本就覆盖了全球大容量 HDD 的大头。希捷详见 [希捷.md](希捷.md)。

---

## 10. 资本分配与 Deal Radar

（2026-08-27 检索；区分官宣/完成/传闻。）

### 10.1 已完成/官宣

- **Sandisk 保留股权退出基本完成**（分拆时 WDC 保留 19.9% SNDK）：
  - 2025-06：出售约 74% 保留股（约 2,130 万股），约 $880M 用于税高效退役债务（Sherwood 报道）。
  - 2026-02-18：debt-for-equity exchange，5,821,135 股 SNDK 以 $545/股换 WDC 债务，规模约 **$31.7 亿**（退役债务约 $30.9 亿）。([SNDK 424B7](https://investor.sandisk.com/static-files/2319dcd3-1ea8-4624-a024-e08be4e266fc))
  - 2026-05-06：equity-for-equity exchange，653,203 股 SNDK 换回 1,865,801 股 WDC；此后仅剩 **1,038,681 股 SNDK** 待处置。([WDC 官网](https://www.westerndigital.com/company/newsroom/press-releases/2026/2026-05-06-wd-announces-equity-for-equity-exchange))
  - 含义：SNDK 高位变现 → 退役 WDC 债务/回购 WDC 股票，是本轮周期里非常漂亮的资本操作；FY2026 利润表里的 $6.5B 一次性收益也来源于此。
- **2026-02-03：董事会新增授权 $4.0B 回购**。([WDC 官网](https://investor.wdc.com/news-releases/news-release-details/western-digital-authorizes-additional-40-billion-share))
- 2026-01：战略投资量子硬件公司 Qolab（材料科学/精密制造能力外延，金额小，属期权性质）。([Q2'26 电话会](https://www.fool.com/earnings/call-transcripts/2026/01/30/western-digital-wdc-q2-2026-earnings-transcript/))

### 10.2 传闻级（不可当事实）

- **2026-07-21：市场报道 WDC 与 Kioxia 重启合并谈判**（Simply Wall St 经 Yahoo 转发），内容称"合并双方 NAND 闪存资产"——但 WDC 的 NAND 已分拆给 SNDK，该报道口径与分拆后事实不符，疑似旧叙事翻炒或误述，**标记【尚无法验证】，仅作情绪面参考**。值得后续跟踪是否有正式 8-K。

### 10.3 未发现

- 未检索到激进股东介入、重大监管审查/诉讼、大股东变更的可核实条目。

---

## 11. 估值与资金效率

### 11.1 市场定价（库口径，2026-08-26）

- 收盘价 **$468.88**，市值 **$169.1B**，PE TTM 19.3（⚠️ 分母含 $6.5B SNDK 一次性收益，失真）、PB 1.41。
- 近期波动极大：2026-07-21 报道时股价 $548，且此前 30 天已 -26.5%；到 8-26 进一步回落至 $469。**市场正在重新定价"周期顶部 vs 结构性"的分歧。**

### 11.2 Reverse DCF 先行：当前价格隐含了什么？

不用库的失真 PE。用 FY2026 干净口径：

- 市值 / FY2026 Non-GAAP EPS $10.22 ≈ **45.9x**
- 市值 / FY2026 FCF $3.51B ≈ **48.2x**（FCF yield ≈ 2.1%）
- 前瞻：Q1FY27 指引 EPS $4.00，粗略年化 $16 → 约 **29x** forward（假设：Q1 利润率维持、无季节大幅下滑）

反推（**全部为假设**：贴现率 10%、永续增长 3%、以 FY2026 FCF $3.5B 为基数、5 年显性期）：

| 假设 FCF 5 年 CAGR | 隐含估值 |
|---|---:|
| 20%（≈管理层目标下限） | ≈$100B |
| 25% | ≈$124B |
| 30% | ≈$149B |
| **≈33%** | **≈$169B（当前市值）** |

**结论：当前市值隐含 FY2026 的高基数上 FCF 再以 ~33% CAGR 连涨 5 年**——这已经超出管理层自己 >20% 的营收 CAGR 目标，即市场不仅定价了解释 A（结构性），还定价了相当长的持续时间和利润率继续扩张。

### 11.3 ±30% 偏离规则

按解释 A 乐观情形（FCF CAGR 20–25%）自估 $100–124B，对市价 $169B 偏离 **-27% ~ -41%**，触及 ⚠️ **caution**。分歧来源：市场可能用更低贴现率（降息预期）、更长显性增长期（AI 数据 10 年叙事）、或把"寡头不扩产"当成确定性。我的估算对周期反转（解释 B）只给了有限保护——若 GM 回落到 30%，FCF 可能腰斩以上，估值支撑会远低于 $100B。

### 11.4 资金效率小结

- FCF margin FY2026 = 27.2%，Q4 单季 34%；
- CapEx 仅 3.2% 收入，长期 4–6%；
- ROE FY2025（库）35.6%，分拆退役债务后杠杆持续下降；
- 回购 $4B 授权 + SNDK 股权变现，资本分配目前对股东友好。

---

## 12. 我的看法（【我的推演】，整篇主观，待事实纠正）

1. **公司边界判断**：WDC 的研究框架 = 希捷框架，唯一主线是"Nearline EB 量价 × 寡头供给纪律"。Client/Consumer 合计 11% 且萎缩，可以忽略。——事实笔记支持（第 5 章）。
2. **周期判断**：我倾向于"**A 与 B 之间、偏 A**"。支持 A 的证据：三寡头谁都没有扩产动机（CapEx 3–6% 收入 vs NAND 的 30%+）、长约签到 CY2027/28、AI 数据量的物理增长、$/TB 首次回升而非继续通缩。但 FY2023 的 -31% 才过去三年，这个行业没有"这次不一样"的豁免权——**长约给的是能见度，不是免疫**。
3. **估值判断**：$169B 市值已经把解释 A 定价到超出管理层自身目标（Reverse DCF 隐含 ~33% FCF CAGR），赔率不好。7–8 月 26%+ 的回撤说明市场也在意识到这点。**这不是"公司好不好"的问题，是"价格里还剩多少"的问题。** 合理策略是等周期信号或估值给安全边际，而不是在 GM 54%、情绪最热时追。
4. **跟踪信号**（周期反转的先行指标，按敏感度排序）：
   - hyperscaler 资本开支指引与库存天数（一个 15%+ 客户去库存 = 重大警报）；
   - 季度 EB 出货环比、ASP/EB 方向（连续两季 $/TB 转跌 = 周期拐点）；
   - LTA 续约/重谈动向；
   - Seagate HAMR 量产进度 vs WDC 40TB ePMR/UltraSMR 的 $/TB 竞争力；
   - 库口径 TTM FCF 环比。
5. **被事实纠正记录**：初稿认为"FY2026 每个季度都在加速，利润率无拐头迹象"——补充 Deal Radar 后发现 2026 年 7–8 月股价已回撤 26%+，市场对景气持续性的定价已先于基本面松动，估值判断相应从"合理偏贵"下调为"caution"。

---

## 13. 跳过的模块及原因

- **护城河与竞争壁垒（独立章）**：跳过独立成篇——寡头格局、垂直整合制造、TB/drive 路线图已分别并入第 3 章（供需）与第 9 章（竞争），再单写会重复。
- **数据库财务深扒（独立章）**：跳过——库核对已分散嵌入正文【库核实】标注；FY2026 库尚无年报行，待库更新后再做一次完整对账。
- **分红与资本分配（独立章）**：并入第 10 章 Deal Radar。WDC 当前分红金额与派息政策【尚无法验证】，列入后续研究。

---

## 14. 后续研究方向

1. **WDC vs STX 技术对标专项**：HAMR 量产时间表、40TB+ ePMR/UltraSMR 的 $/TB 成本曲线、两家 qualification 进度。
2. **Nearline HDD 行业总需求测算**：hyperscaler 资本开支 → EB 需求的自上而下模型（23% CAGR 公司预测的可复算验证）。
3. **库 FY2026 年报行更新后**：补一次完整库对账（含股数稀释、SBC——当前库表无 weighted shares / SBC 字段）。
4. **员工数与人均创收**：库无此字段，从 FY2026 10-K 补（分拆后口径）。
5. **Kioxia 合并传闻跟踪**：是否有正式 8-K/官宣；若无则删除该条目。
6. **分红政策**：WDC 分拆后股息政策核实。
7. **季度跟踪清单**：EB、ASP/EB、Cloud 收入、Nearline 占比、GM、客户集中度、LTA 动向——每季度财报后更新本笔记。

---

## 15. 数据来源与核实记录

### 来源清单

**公司披露 / SEC**
- [WDC 完成分拆公告（2025-02-21）](https://investor.wdc.com/news-releases/news-release-details/western-digital-completes-planned-company-separation)
- [分拆 pro forma 8-K（FY2022 HDD-only）](https://www.sec.gov/Archives/edgar/data/106040/000010604025000012/wdc8-khardxspin.htm)
- [FY2022 10-K](https://www.sec.gov/Archives/edgar/data/106040/000010604022000055/wdc-20220701.htm)（FY2022 分部重构依据）
- [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/106040/000010604025000038/wdc-20250627.htm)
- [FY2026 10-K（截至 2026-07-03）](https://www.sec.gov/Archives/edgar/data/106040/000162828026057139/wdc-20260703.htm)（[FinancialFilings 镜像](https://financialfilings.com/filings/western-digital-corp/annual-report/2026/56179556/)、[PublicNow 镜像](https://ebs.publicnow.com/view/6DA2409148F5DD210BED17BF114A5DFB1FADCEDE)）
- [Q4 FY2026 财报与 Earnings Deck](https://investor.wdc.com/node/28586)（[Deck PDF](https://investor.wdc.com/static-files/e1f02f77-4432-42c3-8bd4-024371f40e54)）
- [Investor Day 2025](https://investor.wdc.com/news-releases/news-release-details/western-digital-unveiled-go-forward-strategy-investor-day-2025)、[Innovation Day 2026 Deck](https://investor.wdc.com/static-files/f010ae83-c695-4c08-b1cf-cb4091940da5)
- [Q2 FY2026 电话会实录（Motley Fool，2026-01-30）](https://www.fool.com/earnings/call-transcripts/2026/01/30/western-digital-wdc-q2-2026-earnings-transcript/)（PO/LTA 披露）
- [$4.0B 回购授权（2026-02-03）](https://investor.wdc.com/news-releases/news-release-details/western-digital-authorizes-additional-40-billion-share)
- [SNDK 424B7（2026-02-18 debt-for-equity exchange）](https://investor.sandisk.com/static-files/2319dcd3-1ea8-4624-a024-e08be4e266fc)
- [WDC equity-for-equity exchange（2026-05-06）](https://www.westerndigital.com/company/newsroom/press-releases/2026/2026-05-06-wd-announces-equity-for-equity-exchange)
- [SNDK 分拆 Information Statement（2024-11，保留 19.9% 条款）](https://www.sec.gov/Archives/edgar/data/2023554/000119312524264578/d835366dex991.htm)

**媒体/第三方**
- [Stock Titan：WDC 10-K 客户集中度摘要](https://www.stocktitan.net/sec-filings/WDC/10-k-western-digital-corp-files-annual-report-900919bf9936.html)
- [Sherwood：$4B 回购与 SNDK 股权处置（2026-02-03）](https://sherwood.news/markets/western-digital-announces-additional-usd4-billion-in-share-buybacks-with/)
- [Simply Wall St / Yahoo：Kioxia 合并传闻（2026-07-21，【尚无法验证】）](https://finance.yahoo.com/markets/stocks/articles/western-digital-wdc-reenters-merger-042833228.html)
- [Simply Wall St / Yahoo：SNDK share swap（2026-05-07）](https://finance.yahoo.com/markets/stocks/articles/western-digital-share-swap-highlights-182227941.html)

**stock_data 库（2026-08-27 查询）**
- `us_financial_current_annual`：WDC FY2021–FY2025、STX FY2022–FY2026 年度财务；`us_financial_current_ttm`：WDC（至 2026-04-03）/STX（至 2026-07-03）TTM；`daily_quote`：WDC/STX 2026-08-26 行情、市值、PE TTM。
- 注意：库表结构已改版（原 `us_income_statement` 等表不存在；新统一表 `income_statement` 无 WDC 数据，美股数据在 `us_financial_current_*` 系列），无 SBC/股数字段、无 standalone 列。

### 核实/整合记录

- **2026-08-27（本次整合）**：
  1. 将原文件两个回答（业务结构篇 + 五年周期篇）按 SOP 模板整合为完整研究笔记；采用强周期变体，供需框架与周期位置前置。
  2. 库核实：FY2023–25 营收/毛利率/营业利润率与库一致；库 FY2021/22 为合并口径、净利润含已终止业务，正文已标注口径差异；FY2026 库无年报行，用 10-K 外部口径并标注。
  3. 新增第 8 章（订单与客户承诺，来自 Q2'26 电话会）、第 10 章（Deal Radar：SNDK 股权退出三步、$4B 回购、Kioxia 传闻标记【尚无法验证】）、第 11 章（Reverse DCF 估值）。
  4. 新增同行对比章（STX 五年库数据）。
  5. 估值纪律执行：Reverse DCF 先行；自估与市价偏离 -27%~-41%，触发 ⚠️ caution 并解释分歧来源；模型输入全部标"假设"。
  6. 硬规则 6：所有分部/利润结论均基于 3–5 年序列；硬规则 7：FY2026 NI>OP 已查明为 $6.5B SNDK 一次性收益。
