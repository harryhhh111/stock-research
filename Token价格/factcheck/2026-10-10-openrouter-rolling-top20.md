# OpenRouter 不同时间窗口的滚动 Top-20 模型核验

核验日期：2026-10-10；数据截止：2026-10-08 UTC。

## 结论

可以用公开数据重建**不同日期的滚动 30 日 Top-20**，并不是只能做半年累计榜。按每月 10 日（10 月取 8 日）作为窗口终点，公开可见、具名模型的 Top-20 从 2026-04-10 的 **69.904T Token** 增至 2026-10-08 的 **485.361T（6.94×）**；其占所有公开 Token（包含无法拆分的 `other` 长尾）的比例在 **64.4%–77.8%**。

在与 Top-10 核验完全相同的**逐日挂牌价、75% 输入 / 25% 输出**情景中，可定价部分的 Top-20 挂牌消费额为：4 月 **$112.1M**、5 月 **$146.4M**、6 月 **$216.0M**、7 月峰值 **$313.7M**、8 月 **$245.0M**、9 月 **$300.9M**、10 月 **$290.3M**。因此，7 月以后 Token 仍从 155.947T 增至 485.361T，但挂牌消费额没有同步创新高；在可定价 Token 上的隐含挂牌价从 7 月约 **$2.12/M Token** 降至 10 月约 **$0.69/M Token**。

这份数据适合回答“某个 30 日窗口中，哪些模型占据用量、份额如何迁移，以及按公开挂牌价对应多大的消费额情景”；不适合回答完整市场份额、真实收入或各厂商 Token 总量。

| 30 日窗口终点 | 具名 Top-20 Token | 可定价覆盖率 | 3:1 挂牌消费额情景 | 全按输入价 | 全按输出价 | 隐含 3:1 挂牌价 / M 可定价 Token | Top-20 / 所有公开 Token |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-04-10 | 69.904T | 94.28% | $112.1M | $59.0M | $271.3M | $1.70 | 72.89% |
| 2026-05-10 | 62.246T | 99.93% | $146.4M | $73.3M | $365.7M | $2.35 | 64.40% |
| 2026-06-10 | 96.880T | 93.20% | $216.0M | $109.3M | $536.0M | $2.39 | 69.44% |
| **2026-07-10** | **155.947T** | **94.67%** | **$313.7M** | **$160.0M** | **$774.7M** | **$2.12** | **76.66%** |
| 2026-08-10 | 200.538T | 100.00% | $245.0M | $130.4M | $588.9M | $1.22 | 75.89% |
| 2026-09-10 | 350.700T | 92.13% | $300.9M | $167.5M | $701.1M | $0.93 | 77.78% |
| 2026-10-08 | 485.361T | 86.62% | $290.3M | $154.8M | $696.7M | $0.69 | 77.43% |

“可定价覆盖率”是有历史挂牌价或公开免费零价的 Token 占 Top-20 Token 的比例；未公开价格不被补零。故美元金额只对应这个可定价子集，且每行给出全按输入/全按输出的机械边界。它不是 OpenRouter、模型实验室或供应商披露的营收。

### 为什么 Top-20 也是 2026-07-10 最高？Claude 没有消失，但其高价消费额回落

**是同一类“高价 Claude 组合”机制，但不能照搬 Top-10 的说法。** 在 Top-10 中，三款 Claude 到 8 月都已不在前十；但在 Top-20 中，Claude 仍然存在，甚至从 7 月的 3 款变成 8 月的 5 款。7 月峰值和 8 月回落的主因，是这些 Claude 型号的合计 Token 和对应挂牌消费额下降、同时部分量转向较低价的 Sonnet 5，而不是它们集体跌出 Top-20。

| 30 日窗口终点 | Top-20 挂牌消费额 | Anthropic 型号数（Top-20 内） | Anthropic Token | Anthropic 挂牌消费额 | Anthropic 占 Top-20 金额 | 非 Anthropic 挂牌消费额 |
|---|---:|---:|---:|---:|---:|---:|
| 2026-06-10 | $216.0M | 4 | 20.043T | $168.3M | 77.9% | $47.6M |
| **2026-07-10** | **$313.7M** | **3** | **24.645T** | **$221.2M** | **70.5%** | **$92.5M** |
| 2026-08-10 | $245.0M | 5 | 19.566T | $154.0M | 62.9% | $91.0M |

从 6 月到 7 月，Top-20 情景金额增加 **$97.7M**；其中 Anthropic 增加 **$52.9M（54.1%）**，其他模型增加 $44.8M。从 7 月到 8 月，Top-20 情景金额减少 **$68.6M**；其中 Anthropic 减少 **$67.2M（97.9%）**，非 Anthropic 部分只少 $1.4M。因此，7 月仍是最高点的直接算术解释是：当期 Claude 的高价 Token 组合最多。

具体而言，7 月的 Claude 4.7 Opus、4.8 Opus、4.6 Sonnet 分别对应 $104.0M、$79.3M、$37.9M；8 月它们仍在 Top-20，但分别降至 $37.9M、$49.1M、$22.6M。8 月新增的 Opus 5（$26.7M）和 Sonnet 5（$17.7M）只能部分填补缺口；其中 Sonnet 5 的公开价为 $2/$10 每百万输入/输出 Token，低于 Sonnet 4.6 的 $3/$15。公开排名没有请求级迁移原因或实际结算价，所以这只能说明**挂牌价组合与 Token 量的变化**，不能证明用户为何切换。

## 榜首的窗口迁移

下表只放每个窗口前五，便于先看结构变化；每个窗口完整 Top-20、排名、Token、出现于每日 Top-50 的天数、逐日价格对应的 3:1 挂牌消费额与输入/输出边界，见数据文件 [openrouter_rolling_top20_2026-10-08.csv](data/openrouter_rolling_top20_2026-10-08.csv)。

| 窗口终点 | 第 1 名 | 第 2 名 | 第 3 名 | 第 4 名 | 第 5 名 |
|---|---|---|---|---|---|
| 2026-04-10 | Xiaomi MiMo V2 Pro<br>8.880T | Qwen 3.6 Plus（免费）<br>6.263T | Step 3.5 Flash（免费）<br>5.499T | DeepSeek V3.2<br>5.075T | MiniMax M2.5<br>4.692T |
| 2026-05-10 | Tencent HY3 Preview（免费）<br>6.045T | Claude 4.6 Sonnet<br>5.801T | Kimi K2.6<br>5.006T | DeepSeek V3.2<br>4.688T | Gemini 3 Flash Preview<br>4.473T |
| 2026-06-10 | DeepSeek V4 Flash<br>14.012T | Tencent HY3 Preview<br>13.199T | Claude 4.6 Sonnet<br>7.994T | Claude 4.7 Opus<br>7.858T | OpenRouter Owl Alpha<br>6.571T |
| 2026-07-10 | DeepSeek V4 Flash<br>21.289T | Xiaomi MiMo V2.5<br>18.470T | MiniMax M3<br>17.558T | Tencent HY3 Preview<br>12.718T | Claude 4.7 Opus<br>10.400T |
| 2026-08-10 | Xiaomi MiMo V2.5<br>33.312T | DeepSeek V4 Flash<br>26.273T | Tencent HY3<br>18.579T | Tencent HY3（免费）<br>14.408T | GLM 5.2<br>14.238T |
| 2026-09-10 | DeepSeek V4 Flash 0731<br>50.949T | GPT-5.6 Luna<br>37.908T | Tencent HY4 Preview<br>30.053T | Xiaomi MiMo V2.5<br>28.515T | Tencent HY3<br>27.719T |
| 2026-10-08 | DeepSeek V4.1 Flash<br>90.514T | Space Bunny Alpha<br>56.717T | GLM 5.3 Flash<br>55.211T | Tencent HY4 Preview<br>43.715T | GPT-5.6 Luna<br>37.340T |

最值得注意的不是某一模型连续霸榜，而是**榜单换手很快**：4 月仍由 MiMo V2 Pro、Qwen、Step、V3.2 等主导；6–7 月切换到 DeepSeek V4 Flash、HY3、MiMo V2.5 与 MiniMax M3；9–10 月进一步切至 DeepSeek V4 Flash 0731 / V4.1 Flash、HY4、GLM 5.3 Flash 和 Luna。这个高换手率也解释了为什么不能用“某一固定模型的挂牌降价”代表整体 Token 市场的价格趋势。

## 口径与重要限制

1. **窗口与排名：** 每个终点向前含当日取 30 个 UTC 日；把每个具名 `model_permaslug` 在窗口内公开显示的 `total_tokens` 求和后排序。`:free` 是与付费路由分开的排名条目，按 OpenRouter 的原始口径保留；`other` 是长尾汇总，不是模型，不能放进 Top-20。
2. **并非完整模型面板：** OpenRouter 每天只公开前 50 个具名模型与一个 `other` 汇总。因此模型当天没有具名行时，可能是零用量，也可能是落在前 50 名之后；公开数据无法区分。每条结果的 `days_visible_in_daily_top50` 已保留，供判断这个风险。故“Top-20 / 所有公开 Token”是按可见具名 Token 得到的可复算下界，不应表述为精确的全平台模型份额。
3. **并非全行业：** 仅是经过 OpenRouter 且公开可见的流量，不包括直连模型厂商、Azure、Bedrock 等，也不等于模型厂商总用量。各模型采用各自 tokenizer，跨厂商 Token 亦非完全同质的算力单位。
4. **挂牌消费额不是实际消费额或收入：** 此榜只使用 `total_tokens`；没有输入/输出拆分、缓存、折扣、BYOK 或实际结算金额。本文的美元数按每日历史广告价和 75%/25% 输入输出假设复算，只能称为挂牌消费额情景，不能称为收入。

## 可复算文件与来源

- 明细： [openrouter_rolling_top20_2026-10-08.csv](data/openrouter_rolling_top20_2026-10-08.csv)
- 窗口汇总： [openrouter_rolling_top20_summary_2026-10-08.csv](data/openrouter_rolling_top20_summary_2026-10-08.csv)
- 复算脚本： [verify_openrouter_rolling_top20.py](verify_openrouter_rolling_top20.py)，固定使用 OpenRouter 数据镜像 commit `f0e8f5b17aca`。
- 字段与每日 Top-50 + `other` 的公开限制： [OpenRouter Data API](https://openrouter.ai/docs/cookbook/administration/data-api)。
