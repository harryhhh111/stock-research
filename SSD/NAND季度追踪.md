# NAND / eSSD 季度追踪表

> 建立日期：2026-08-21。用途：用"卖方实际出货 + HDD 缺口 + BOM 模型 + 第三方年度锚"四方对账，把 AI 数据中心 SSD 需求的估算误差收到 ±10–15%。
> 上游文档：`NAND需求测算.md`（BOM 自下而上模型）、[Kioxia 主报告](Kioxia/Kioxia.md)（供给侧）。

## 一、每季收集清单（财报季执行）

### A. 卖方：六家 NAND 原厂 eSSD bit 出货（最硬数据）

| 厂商 | 披露位置 | 每季记录 |
|---|---|---|
| Samsung | 季报电话会（DS 部门） | eSSD/DC bit 出货 QoQ%、DC 收入占比 |
| SK hynix / Solidigm | 季报电话会 | NAND bit 出货 QoQ%、eSSD 占比评论 |
| Micron | 季报（FQ 比自然季快一个月） | data center SSD 收入、bit QoQ% |
| Kioxia | 季报 | "SSD & Storage" 收入、bit 出货 QoQ% |
| SanDisk | 季报 | data center bit 出货、价格评论 |
| YMTC | 无公开财报，靠 Counterpoint 季度份额 | bit shipment 份额 |

**汇总动作**：六家 eSSD bit 出货加总 → 得到当季 eSSD 市场实际值 → 年化后与 Goldman 年度锚对账。

### B. HDD 对照：Seagate / WD 近线 EB 出货（测 QLC 替代缺口）

| 厂商 | 披露位置 | 每季记录 |
|---|---|---|
| Seagate | 季报 | nearline EB 出货量、均价 |
| WD | 季报 | nearline/cloud EB 出货量 |

**对账公式**：AI 海量存储需求增速（TrendForce 定性+第三方估）− NL HDD 实际 EB 出货增速 = 流向 QLC eSSD 的缺口。

### C. 买方/中间环节（交叉验证）

| 来源 | 指标 |
|---|---|
| Dell / NetApp / Pure / VAST / WEKA / DDN | 存储收入、AI 相关收入增速 |
| Phison（群联，月度营收） | enterprise 口径评论、主控出货 |
| 八大 CSP 季报 | capex 总额与指引（2026 锚：合计 $7,100 亿、+61%） |

### D. 第三方季度面板（白嫖校准）

- Counterpoint 季度 NAND bit shipment 份额 + server-led eSSD 占比
- TrendForce 月度 NAND/SSD 合约价、eSSD 合约价 QoQ
- TrendForce / TechInsights 年度需求预测的修订

## 二、对账结构

```
① 卖方六家 eSSD bit 加总（实测）
② NL HDD 缺口 → QLC 替代量（半实测）
③ BOM 自下而上（../数据中心/factcheck/nand_demand.py，模型）
④ Goldman/TrendForce/TechInsights 年度锚（预测）

规则：任意一口径偏离其余三方 >20%，当季标记复核，找原因（口径/锁货/CMX 起量）。
```

## 三、基线数据（截至 2026-08，已收集）

| 指标 | 数值 | 时点 | 来源 |
|---|---|---|---|
| 全球 NAND 需求 | 997 / 1,216 / 1,484 / 1,807 EB | 2025/26E/27E/28E | TechInsights（Kioxia 引用） |
| 企业级 SSD 需求 | 474 EB / 619 EB | 2026E / 2027E | Goldman |
| Server-led eSSD 占 NAND 出货 | **48%** | 2026 Q2 | Counterpoint |
| NAND bit 份额 | Samsung 25 / SK+Solidigm 22 / YMTC 14 / Kioxia 14 / Micron 13 / SanDisk 11（%） | 2026 Q2 | Counterpoint |
| 2026 NAND 供需 | 缺口 -4~-5%；2027 H2 转松 | 2026-07 | TrendForce |
| NL HDD 交期 | >52 周；WD 自述 2026 年基本售罄 | 2025 Q4–2026 | TrendForce / WD |
| QLC 状态 | 产能订满至 2026 年底；2027 年初或反超 TLC | 2026 中 | TrendForce / 行业报道 |
| eSSD 合约价 | **Q1 约 +80% QoQ、Q2 +48~53% QoQ**；Q3 涨幅放缓（整体 NAND +10~15% QoQ，不能直接等同 eSSD） | 2026Q1–Q3 | TrendForce；口径说明见 `2026-09-11-SSD价格多口径调研.md` |
| NVIDIA 机柜 SSD 模型 | 2026 ~17.6EB（含基准 CMX） | 2026E | 本工作区 `../数据中心/factcheck/nand_demand.py` |

## 四、2026 Q2 回填（2026-08-21 完成，数据为自然季 4–6 月）

### A. 卖方：六家原厂 Q2 实际值

> 财年口径注意：Micron 为 FQ3（3–5 月）、SanDisk 为 FQ4（4–6 月）、Kioxia 为 FY26Q1（4–6 月），Samsung/SK 为自然 Q2。

> **取数分工**（2026-08-21 起）：财务总量（收入/毛利/净利/EPS）以 `stock_data` 库（my-t-vinci PostgreSQL）口径为准，标【库核实】；运营指标（bit 出货、EB、ASP、eSSD/数据中心占比、长协）不在财务报表内，仍取财报电话会/新闻稿。库当前滞后：SNDK/WDC 缺 FQ4、STX 缺 FQ3+FQ4（且 STX 近两季毛利字段为 NULL），滞后季度暂以电话会口径为准、待库更新后复核。

| 厂商 | Q2 实际值 | 来源（财报日期） |
|---|---|---|
| Samsung | DRAM+NAND bit 出货双创新高；NAND bit QoQ 低个位数增长（未单独披露 eSSD）；Memory 收入 ₩120.8T（+62% QoQ）；第六代 eSSD 放量；预期缺货持续到 2027+ | 财报电话会 2026-07-29 |
| SK hynix | NAND bit **+mid-teens% QoQ**；NAND ASP **+mid-50s% QoQ**；**eSSD 收入环比翻倍**；Solidigm 30TB+ eSSD 收入环比 3 倍；~10 个 LTA（含保证金）；电话会点名 **KV cache offloading / near-GPU storage** | 财报电话会 2026-07-29 |
| Micron（FQ3） | 【库核实】收入 **$414.6亿**（QoQ +73.7%）、毛利率 **84.6%**、净利 $282.4亿、摊薄 EPS $24.67；运营口径：**数据中心 SSD 收入 >$5B，环比翻倍以上**；NAND 收入 $9.9B（+99% QoQ）；NAND bit +mid-single digit，ASP **+mid-80s% QoQ**；16 个 SCA 长协（覆盖 1/3 NAND 产量、take-or-pay 到 2030、$22B 保证金）；原话确认 "AI context memory storage and HDD displacement" 扩大 SSD TAM | 财报 2026-06-24；财务总量 stock_data 库 |
| Kioxia（FY26Q1） | 收入 ¥1,767.1B（+76.2% QoQ）；blended **ASP +70% QoQ**，bit 低个位数增长；**SSD & Storage 收入 ¥1,174.7B（+95.7% QoQ），其中数据中心/企业级占比超 60%**、量创纪录；LTA 目标 2028 年覆盖 50% 出货；提醒"高价使 QLC 替代 HDD 的 transition 可能比预期慢" | 财报 2026-07-31 |
| SanDisk（FQ4） | 收入 $8.97B（+51% QoQ；库最新仅到 FQ3 $59.5亿，5.95×1.51≈8.98 衔接一致 ✅，待库更新后复核 FQ4）；**数据中心收入 $2.98B（+103% QoQ）；数据中心占 bit 出货从一年前 12% → 38%**；QLC Stargate 当季开始贡献收入；NBM 长协保底收入 $93.9B；bit 配给制持续到 2027+；预计 2026 NAND TAM >$3,000 亿、数据中心占比 ~50% | 财报 2026-08-05；FQ3 已库核实 |
| YMTC | Counterpoint 份额 14%（首进前三）；bit +22% YoY | Counterpoint 2026-08-11 |

### B. HDD 对照（两家财年均 7/3 结束，即自然 Q2）

| 厂商 | Q2 实际值 | 来源 |
|---|---|---|
| Seagate（FQ4） | 总出货 218EB（+34% YoY）；**数据中心近线 195EB（+43% YoY，+11% QoQ）**；每 EB 价格 +~10% YoY；近线产能基本锁定到 CY2028，客户谈到 2029+；HAMR 占近线 EB run-rate 40% | 财报 2026-07-28 |
| WD（FQ4） | 总出货 231EB（+22% YoY）；**近线 209EB（+5% QoQ）**；云占收入 ~90%；LTA 到 CY2029 | 财报 2026-08-05 |
| **合计** | **数据中心近线 ≈ 404EB/季**，YoY +22~34% —— 供给刚性确认 | 复算值 |

### C/D. 第三方与价格

- **eSSD 合约价：Q1 约 +80% QoQ，Q2 +48~53% QoQ**（TrendForce）；Q3 的 eSSD 精确涨幅未从公开摘要取得，整体 NAND 合约价预测 +10~15% QoQ 仅作“涨速放缓”的方向参考，**不得直接替代 eSSD 价格**。
- 原厂交叉验证：Micron FQ3 NAND ASP +mid-80s% QoQ、Kioxia FY26Q1 blended ASP +约70% QoQ，均远快于 bit 出货，确认上半年价格主导。
- 现货案例：VDURA 称 30TB TLC eSSD 从 2025Q3 $3,460 → 2026Q3 $22,600（约 6.5 倍）。该指数由混合存储方案供应商发布、方法透明度有限且历史数值曾回溯修订，**仅作高容量现货的低可信度案例，不作为行业均价或模型锚**。完整口径和来源见 `2026-09-11-SSD价格多口径调研.md`。
- IDC：Q1 2026 外部 OEM 企业存储市场 $9.2B（+22.7% YoY）；**全闪存阵列收入占比首破 50%（52.6%）**
- Counterpoint 2026Q2：eSSD 占 NAND bit 出货 **48%**（一年前 26%）；行业收入同比 5 倍；Solidigm bit +40% QoQ；Kioxia 增长放缓因客户对涨价犹豫

### 四方对账结论（首次）

1. **① 卖方实测 vs ④ 年度锚：互洽但有口径差**。SanDisk 称 2026 数据中心占 NAND TAM ~50%，与 Counterpoint 实测 eSSD 占 bit 48% 一致；Goldman eSSD 474EB/2026 与"48% × 1,216EB ≈ 584EB"的差异来自口径——Goldman 是成品盘口径，Counterpoint 的 48% 含进服务器的所有 NAND bit。不强行拉平，标记为已知口径差。
2. **五家原厂指引完全一致**：Samsung / SK / Micron / Kioxia / SanDisk 全部称紧张持续到 2027 以后，与 [Kioxia 主报告](Kioxia/Kioxia.md) 的供给侧判断吻合。
3. **CMX 叙事首次获原厂财报确认**：SK 电话会点名 KV cache offloading / near-GPU storage，Micron 原话 "AI context memory storage"——`SSD与CMX需求模型.md` 的需求逻辑不再是纯推测，但**量仍未单独披露**，2/4/16TB 参数维持原假设。
4. **② HDD 缺口逻辑成立但有反噬信号**：Seagate+WD 近线 404EB/季、YoY 仅 +22~34%、产能锁定到 2028——供给刚性确认；但 Kioxia 明确提醒**高价本身在放慢 QLC 替代 HDD 的速度**，替代缺口不能按无限弹性假设。
5. **③ BOM 模型无需修正**：NVIDIA 机柜 SSD 2026 ~17.6EB / 2027 ~49.2EB 的估算与实测行业量级（eSSD 年 500+ EB）自洽，占比 ~4% 结论不变。
6. **长协锁定成为普遍现象**：Micron 16 个 SCA（$22B 保证金）、SanDisk NBM $93.9B 保底、SK ~10 个 LTA、Kioxia 目标 2028 年 LTA 覆盖 50%——印证"锁货"是本轮缺货的核心放大器。

## 五、下一季待填（2026 Q3 财报季，约 2026-10 起）

| 待填项 | A 卖方 eSSD bit | B NL HDD EB | C 存储商 AI 收入 | D eSSD 合约价 QoQ |
|---|---|---|---|---|
| 2026 Q3 | ☐ | ☐ | ☐ | ☐ |

## 六、特别跟踪项

- **CMX 实际部署**：CoreWeave / Nebius / NVIDIA 披露的 STX/CMX rack 配置 → 收敛 `SSD与CMX需求模型.md` 的 2/4/16TB 参数（当前最大不确定项）。*进展：SK/Micron Q2 财报首次口头确认 KV cache/context memory 需求，量未披露*
- **铠侠年度售罄声明的延续性**：Q2 已兑现为纪录业绩 + ASP +70% QoQ + LTA 推进；Q3 继续跟踪管理层口径
- **长协锁定的规模**：Micron SCA / SanDisk NBM / SK LTA / Kioxia LTA 每季披露的新增保证金与覆盖比例
- **YMTC Fab3 爬坡**：2026 年底投产是否兑现（Reuters 口径 50k→100k wpm）
- **Micron 新加坡厂**：2028 H2 首批 wafer 的时间表是否提前/推迟
