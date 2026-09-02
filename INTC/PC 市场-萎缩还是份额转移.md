# PC 市场：萎缩还是份额转移？（Intel CCG vs AMD Client）

> 回答《后续研究方向》第 1 题：Intel PC 业务过去五年到底是市场本身萎缩，还是被 AMD 抢了份额？
> 结论先行：**两个阶段答案不同——2022–2023 主要是市场萎缩（两家一起跌），2024–2025 市场回暖后 Intel 仍在跌，是纯份额流失。2026 年又叠加了新变量（内存危机 + Intel 自己把产能让给服务器）。**

## 1. PC 市场总量（IDC 口径，含台式+笔记本+工作站）

| 年份 | 出货量 | 同比 |
|---|---:|---:|
| 2021 | 350.1M | 疫情高点 |
| 2022 | 292.3M | **-16.5%** |
| 2023 | 259.5M | **约 -13.9%** |
| 2024 | 262.7M | +1.0% |
| 2025 | 284.7M | **+8.1%** |
| 2026（IDC 预测） | 约 -11.3% | 内存/闪存短缺冲击 |

要点：2022–2023 是疫情需求透支后的真实大萎缩（高点回落约 26%）；2024 企稳、2025 明显回暖（Windows 10 停服换机 + 关税前抢跑 + 年末抢内存备货）；**2026 市场再度转跌，Q1 桌面 CPU 出货暴跌约 20%，Q2 PC 出货 -4.9%（68.2M），IDC 预测全年 -11.3%、Q4 假日季可能 -20%**。([IDC 2022][1])([IDC 2023][2])([IDC 2025 全年][3])([IDC 2026 预测][4])

## 2. Intel CCG vs AMD Client：收入趋势对比

| 年份 | Intel CCG/CCPG | AMD Client | PC 市场背景 |
|---|---:|---:|---|
| 2021 | $41.08B | — | 疫情高点 |
| 2022 | $31.77B（-23%） | $6.2B | 市场 -16.5% |
| 2023 | $29.26B（-8%） | $4.65B（-25%） | 市场 -13.9% |
| 2024 | $33.35B（新口径，含 NEX） | $7.05B（**+52%**） | 市场 +1% |
| 2025 | $32.23B（**-3%**） | $10.64B（**+51%**） | 市场 +8.1% |
| 2026 H1 | Q1 $7.7B(+1%) / Q2 $8.88B(+13%) | AMD 总收入 Q2 $11.5B | 市场转跌 |

⚠️ 口径提示：Intel 2025 Q1 把 NEX 并入 CCG/DCAI 并追溯调整了 2024 年数据，2021–2023 是旧口径、2024–2025 是新口径，跨年直接比 2023→2024 会高估反弹幅度。([Intel FY2025][5])([ycharts CCG 旧口径][6])([AMD FY2025][7])([AMD FY2024][8])

## 3. 两家的份额（Mercury Research）

- AMD 整体 x86 出货份额：2025 Q1 27.1% → **2026 Q1 32.6%**（历史新高区）；2025 Q4 曾创 29.2% 纪录
- **客户端（PC）CPU**：Intel 份额 2025 Q1 75.9% → 2026 Q1 **70.4%**；AMD 24.1% → **29.6%**；营收口径 AMD 已达 **31.4%**（高端 Ryzen 占比高）
- 桌面：AMD 2026 Q1 33.2%（2025 Q4 曾达纪录 36.4%）；笔记本：AMD 28.3%（一年前 22.5%）
- ARM PC（Apple M 系列 + Snapdragon X）合计已占 PC 约 **14.4%**

([Mercury/Tom's Hardware][9])([Mercury/The Register][10])([PCWorld][11])

## 4. 结论：分三个阶段回答

**阶段一（2022–2023）：主要是市场萎缩。**
PC 出货两年跌了约 26%，Intel CCG 从 $41.1B 跌到 $29.3B（-29%），但 **AMD Client 同期也在跌**（2023 -25%）。两家一起跌 = 市场问题为主。Intel 的 $25B 营收流失（2021→2023，含 DCAI 下滑）大半发生在这个阶段，是"行业潮水退去 + 份额缓慢流失"的叠加，其中市场萎缩是主因。

**阶段二（2024–2025）：市场回暖，Intel 没回来——纯份额流失。**
市场 +1% 再 +8.1%，AMD Client 连续两年 +50% 以上（$4.65B → $10.64B，翻了一倍多），而 Intel CCG 反而 -3%。**这一阶段 Intel 的停滞 100% 是份额问题**：Mercury 数据显示 Intel 客户端份额从 75.9% 跌到 70.4%，丢的份额主要去了 AMD，其次是 Apple/ARM（ARM PC 已到 14.4%）。

**阶段三（2026）：新变量叠加，不能再简单归因。**
- 市场因内存危机再度转跌（IDC 全年 -11.3%），Intel CCPG 销量 -8% 与市场方向一致
- 但 ASP +27% 暴涨，除了产品升级，还有一个新原因：**Intel 主动把产能让给更赚钱的 Xeon（server），PC CPU 供应受限**，Mercury 明确提到 Intel 笔记本 CPU 因产能约束缺货、份额让给了 AMD
- Q1 2026 桌面 CPU -20% 时 AMD 跌得比 Intel 更惨（此前抢跑备货后的库存修正），说明短期份额波动受库存周期扰动很大

## 5. 对 Intel 投资逻辑的意义

1. **CCPG 的基本盘侵蚀是真实的、持续多年的**：即便不算市场萎缩期，Intel 在回暖期也在丢份额。CCPG +13% 的增长质量（ASP 堆出来的）要打折看。
2. **但 2026 年的剧本变了**：Intel 的问题不再是"卖不动"，而是"**产能不够，主动优先喂 DCAI**"。PC 端的 ASP 上涨和销量下滑，部分是主动取舍的结果——这和 2022–2024 年被动丢份额性质不同。
3. **接下来要盯的不是"Intel 能否夺回 PC 份额"，而是**：内存危机 2026 下半年对 PC 市场的冲击有多深；Intel 产能分配（PC vs Server）怎么平衡；Nova Lake 发布后笔记本份额能否稳住。
4. 对 AMD 的判断也要更新：AMD Client 的高增长（+51%）发生在市场回暖 + 抢份额双重顺风期；2026 市场转跌后，AMD Q1 桌面已经先跌为敬，它的 PC 业务同样暴露在内存危机下。

## 来源

[1]: https://tadviser.com/index.php/Article:Computers_(Global_Market) "TAdviser 汇总 IDC/Gartner/Canalys 2022"
[2]: https://tadviser.com/index.php/Article:Computers_(Global_Market) "IDC 2023：259.5M"
[3]: https://www.fonearena.com/blog/473498/global-pc-shipments-q4-2025.html "IDC 2025 全年 284.7M，+8.1%"
[4]: https://www.idc.com/promo/pcdforecast/ "IDC 2026 预测 -11.3%"
[5]: https://www.intc.com/news-events/press-releases/detail/1759/intel-reports-fourth-quarter-and-full-year-2025-financial "Intel FY2025 财报：CCG $32.2B（新口径）"
[6]: https://ycharts.com/indicators/intel_corp_intc_client_computing_group_revenue "CCG 旧口径 2021–2023"
[7]: https://ir.amd.com/news-events/press-releases/detail/1276/amd-reports-fourth-quarter-and-full-year-2025-financial-results "AMD FY2025：Client $10.64B，+51%"
[8]: https://ir.amd.com/financial-information/sec-filings/content/0000002488-25-000009/0000002488-25-000009.pdf "AMD FY2024：Client $7.1B，+52%"
[9]: https://www.tomshardware.com/pc-components/cpus/amd-reaches-46-percent-of-server-x86-cpu-revenue-intel-still-controls-70-percent-of-the-consumer-pc-market-share "Mercury 2026 Q1 客户端份额"
[10]: https://www.theregister.com/systems/2026/06/04/amd-takes-a-third-of-server-cpu-market-as-shipments-grow/ "Mercury 2026 Q1 各细分"
[11]: https://www.pcworld.com/article/3156252/desktop-cpu-shipments-plunge-20-percent-and-it-could-get-worse.html "2026 Q1 桌面 CPU -20%，内存危机"
