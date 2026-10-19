# HYPE与Hyperliquid基本面研究

合并整理：2026-10-10｜本文档由以下研究文档合并而成，内容完整保留：

1. 2026-09-30-Hyperliquid研究报告.md
2. 2026-09-30-HYPE代币研究.md

本轮更新：2026-10-15｜补充 AF 链上执行、系统地址、销毁口径、金额对账与监听要点；未配置自动监听。旧行情及财务快照仍保留各自截止日。

## Hyperliquid 研究报告：链上交易所、生态扩张与 HYPE 价值捕获（原整理日期：2026-09-30）

整理与核对日期：2026-09-30（北京时间）。除特别注明，价格、流通量和近 30 日财务数据截至 2026-09-29 查询快照；数据平台可能追溯修订。本报告研究**协议及生态**，不是 Hyperliquid Labs 的公司财报。HYPE 的供应、回购、解锁和持仓（见本文第二部分：HYPE 代币研究）。

### 核心判断

Hyperliquid 已从链上永续合约交易所，扩展为允许外部团队部署市场和应用的交易基础设施。其最值得跟踪的商业变量是：**交易活跃度能否持续产生手续费，以及新增市场的费用有多少最终进入 Assistance Fund 买入 HYPE**。按 DeFiLlama 的 2025 年分季数据自己复算，用户费用约 **9.72 亿美元**、协议归属收入约 **8.18 亿美元**；但这些数字不是 Labs 的公司营收或净利润，历史高收入也不能保证未来持续。[DeFiLlama 分季损益表](https://investors.defillama.com/protocol/hyperliquid?events=false&fees=true&tvl=false)

研究 HYPE 时需要同时看三条线：**市场份额及实际收费能力、基金回购量、未来代币释放**。只看交易量容易高估协议留存；只看回购又会忽略解锁。验证者集中度、HIP-3 部署方预言机及稳定币基础设施，是这套模式的主要运行风险。

### 一、协议与用户

Hyperliquid 是围绕链上订单簿构建的 Layer 1。**HyperCore** 执行永续和现货订单簿、保证金、清算等交易逻辑；**HyperEVM** 提供 EVM 智能合约环境，使借贷等第三方应用可与交易流动性结合。项目方称订单、取消、成交与清算均在链上执行，系统支持高吞吐；这是**官方能力描述，尚未独立压测**，不能把设计吞吐等同持续实际成交量。[官方技术概览](https://hyperliquid.gitbook.io/hyperliquid-docs)、[HyperEVM 文档](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/hyperevm)

核心用户包括自行交易的个人和机构、提供流动性的做市商、通过 API 接入的程序化交易者，以及使用 HIP-3 部署新市场的团队。相较中心化交易所，其吸引力是自托管、公开的交易状态与接近订单簿交易所的操作方式；用户仍承担杠杆清算、链运行、预言机、桥接资产和前端可用性等风险。**非托管不等于没有运行与治理风险。**

#### 产品体系

| 模块 | 当前作用 | 收入或风险含义 |
| --- | --- | --- |
| 原生永续 | HyperCore 的主要交易产品，支持市价、限价、止损、止盈、Scale、TWAP 等订单及不同保证金模式。[订单类型](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/order-types) | 交易手续费是价值捕获主线；基础档 maker/taker 为 **0.015%/0.045%**，随交易量、质押等变化。官方订单类型页未列“追踪止损”，故不把它写为已核实原生功能。[费率](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees) |
| 现货、HIP-1、HIP-2 | HIP-1 是原生代币标准及现货订单簿部署机制；HIP-2 是与订单簿结合的自动流动性策略。[HIP-1](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-1-native-token-standard)、[HIP-2](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-2-hyperliquidity) | 现货交易费、部署方分成和 HIP-1 拍卖直接销毁应分开统计；部署拍卖不能自动计为基金市场回购。 |
| HIP-3 永续市场 | 外部团队质押 **50 万 HYPE** 后可部署独立永续市场，负责合约定义、预言机和运营。[官方规则](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals) | 扩大股票、商品等可交易标的，但部署方取得部分手续费；增量交易量不等于同等增量协议收入，价格源风险也随之增加。 |
| HIP-4 结果市场 | 可用于预测类产品的、有到期日的结果合约。2026 年已从有限主网市场走向第三方部署。[相关披露](https://www.sec.gov/Archives/edgar/data/2078856/000119312526399511/d168095d424b3.htm) | 需单独验证交易需求、费用和结算风险；不能把它等同整个 Polymarket 产品。 |
| HLP、Vault、Builder Code | HLP 是参与做市和清算的协议金库；普通 Vault 承担策略盈亏。第三方前端可经用户授权对订单附加 builder fee。[HLP](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/protocol-vaults)、[Builder Code](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes) | HLP 收益与 builder fee 不等于 Assistance Fund 收入；Vault 不保本。 |
| HyperEVM 与质押 | 智能合约生态与验证者委托质押，为交易之外的应用和链安全提供基础。[HyperEVM](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/hyperevm)、[质押](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/staking) | HYPE 是 gas 与质押资产；质押奖励来自预留代币，涉及代币释放。 |

#### trade[XYZ]：HIP-3 的具体案例

`xyz` 是 trade[XYZ] 的 HIP-3 永续市场部署名称，trade.xyz 是其交易前端。`xyz:NVDA` 等合约参照股票价格，却是**以 USDC 保证金和结算的永续衍生品**：交易者不拥有股票，也没有股息、投票或交割权。杠杆上限、保证金模式和费用按具体合约变化。[trade[XYZ] 架构](https://docs.trade.xyz/overview/relationship-to-hyperliquid)、[合约说明](https://docs.trade.xyz/perpetuals)、[规格表](https://docs.trade.xyz/perpetuals/specifications-and-schedules/specification-index)

外部股票市场休市时，`xyz` 的价格发现仍可能受其订单簿影响，预言机并非简单冻结在美股收盘价。资金费率可能为正或负，是多空之间的支付，不应一律当作做多成本。2026-09-30 公开市场参数显示，XYZ 的 NVDA、TSLA、AAPL 等股票市场启用 Growth Mode，deployerFeeScale=1.0；普通账户无优惠、无额外 Builder fee 的基础吃单总费率为 **0.009%**，一万美元成交，trade.xyz 与协议各取得 **0.45 美元**。GOLD 等未标记启用 Growth Mode 的市场同条件基础吃单费率为 **0.09%**，双方各取得 **4.50 美元**。实际费用还受账户折扣和前端附加费影响；用户本人 Builder fee 未确认。（见 factcheck/基本面数据核对合集）。[预言机规则](https://docs.trade.xyz/perpetuals/mechanics/oracle-price)、[XYZ 费用](https://docs.trade.xyz/perpetuals/mechanics/fees)、[资金费率](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding)

这一案例说明 Hyperliquid 能吸引外部团队引入新标的；要验证它是否增强 HYPE 价值，仍须看**协议扣除部署方分成后的实际收入**，并检查休市定价和清算表现。“XYZ 占 HIP-3 持仓 90%”尚缺同日同口径数据，本报告不采纳为已核实结论。

### 二、收入从哪里来，最终归谁

主要收入源是**永续及现货交易费**。用户付费后，按产品规则分配给 HLP、做市返佣、HIP-3/现货部署方、builder 等；Assistance Fund 将其获得的交易费用自动换成 HYPE。官方把基金中的 HYPE 视同销毁，但原始 API 的 `totalSupply` 仍包含基金地址余额，因此要区分**基金持币视同销毁**与**原始总供应实际减少**。[官方费用与基金说明](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees)、[官方 API 说明](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)

稳定币储备收益是第二条潜在收入线。USDH 发行方曾承诺把储备收益的 50% 贡献基金；AQAv2 要求符合条件的发行方将其在 Hyperliquid 供应对应约 **90% 经成本调整后储备收益**分给协议，按 30 日计提、期末 8 日后转基金。它是**发行储备收益分成**，不是直接拿用户 USDC 保证金本金放贷；截至本报告数据窗口，AQAv2 首笔预期款项尚未核实到账，不能提前算入历史回购。[USDH 发行方说明](https://docs.usdh.com/usdh/reserves)、[AQAv2 官方规则](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/aligned-quote-assets)

| 指标与期间 | 金额 | 解释 |
| --- | ---: | --- |
| 2025 全年用户费用 | **9.7167 亿美元** | 自己复算 DeFiLlama 四季 *fees*，是用户支付的毛费用。 |
| 2025 全年归属收入 | **8.1779 亿美元** | 自己复算同口径四季 *revenue/earnings*；不等于 Labs 净利润。 |
| 2026-09-29 快照：近 12 月费用／归属收入 | **9.1146 亿／6.8795 亿美元** | 第三方滚动统计；与自然年口径不同。 |
| 同日快照：近 30 日费用／归属收入 | **7266 万／5633 万美元** | 其中永续归属收入约 **5415 万**，现货及相关直接销毁项目约 **218 万**；原生永续与 HIP-3 未在此数据中精确分开。 |

数据来自 [DeFiLlama 分季损益表](https://investors.defillama.com/protocol/hyperliquid?events=false&fees=true&tvl=false)及其[永续](https://api.llama.fi/summary/fees/hyperliquid-perps?dataType=dailyRevenue)、[现货](https://api.llama.fi/summary/fees/hyperliquid-spot-orderbook?dataType=dailyRevenue)子协议接口，含数据商分类假设。不能把 *fees*、*revenue*、基金实际买入美元额和 Labs 公司利润混用。约 **99%** 的常见说法只适用于符合第三方统计规则的特定手续费基数，不代表所有毛费用的 99% 都买 HYPE。基金近 30 日市场回购的独立追踪值约 **5690 万美元**，与上述收入接近，但不是逐笔对账；方法（见本文第二部分：HYPE 代币研究）。[Strata 回购追踪](https://app.strata-terminal.com/buybacks/hype)

Labs 自称自筹资金，但工资、研发、服务器、法律等成本及净利润没有完整公开报表，**协议收入不能推导为 Labs 净利润**。社区网站 hl.eco 提供汇总，其页面明确表示不隶属 Hyper Foundation，不应称“半官方财报”。[Labs 介绍](https://hyperliquid.gitbook.io/hyperliquid-docs/about-hyperliquid/core-contributors)、[hl.eco](https://hl.eco/financials)

### 三、HYPE 代币与估值边界

基金会 2024 年创世公告将 HYPE 最大供应设为 **10 亿枚**，其中 31% 预留创世分配、23.8% 给当前和未来核心贡献者、38.888% 给未来发行及社区奖励。预留份额不等于已由公众持有；核心贡献者完整逐月归属表未公开。[基金会公告](https://hyperfnd.medium.com/hype-genesis-1830a4dc2e3f)

流通量存在重要统计分歧：2026-09-29 DeFiLlama 约 **2.2245 亿枚**，同期 Hyperliquid 官方 API 约 **2.9868 亿枚**，相差约 **7623 万枚**。按同一价格计算，流通市值会显著不同。DeFiLlama 当日快照的 HYPE 价格约 **86.74 美元**、流通市值约 **192.97 亿美元**、FDV 约 **828.74 亿美元**；按其近 12 月归属收入 **6.8795 亿美元**，**自己复算** FDV／归属收入约 **120.5 倍**。这不是企业市盈率，也不表示代币持有人可直接领取这些现金流。[DeFiLlama 快照](https://investors.defillama.com/protocol/hyperliquid?events=false&fees=true&tvl=false)、[官方 API 说明](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)

真正的资本分配问题是：**新增可交易供应和质押奖励释放，与基金买入并视同退出流通的 HYPE，谁在相同时间窗内变化更快**。不同数据商的流通定义未完全对账，估值比较必须固定口径；详情和验证者质押集中度（见本文第二部分：HYPE 代币研究）。

### 四、竞争、护城河与核心风险

Hyperliquid 的潜在壁垒是订单簿流动性与做市网络、统一的链上交易基础设施，以及 HIP-3 开放部署带来的市场覆盖。**这些是待验证的竞争优势，而非仅凭技术宣称即可确认的护城河**：如果低费率竞争者吸走交易者或做市商、部署方拿走更多费用、或市场扩张引入高风险标的，交易量可能增长而基金买盘不增长。对比 dYdX、GMX、Aster、Lighter 及中心化交易所时，应统一永续成交量、未平仓量、费率、执行质量和可留存收入的统计范围。

主要风险按传导路径看：

1. **交易景气与竞争**：交易量和实际费率下降，会先压低手续费，再压低基金回购；30 天收入年化在行情波动时尤其不稳定。
2. **HIP-3 市场质量**：部署方设置预言机、杠杆和合约规格；休市价格发现、极端行情和清算会影响用户信任。[HIP-3 官方规则](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals)
3. **链与治理集中度**：质押决定验证者权重。2026-09-30 官方接口显示 27 个活跃验证者；自己复算活跃质押前五名约占 **52.3%**。这是验证者获得的委托权重，不能误写成五个实体拥有相应数量的代币。[官方 API](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
4. **代币供给与估值**：基金回购不等于净通缩；团队归属、社区奖励、基金视同销毁及真实链上销毁属于不同口径。
5. **资产与监管**：非托管交易仍依赖跨链桥、稳定币和前端；高杠杆衍生品及股票等参考标的面临因地区而异的监管约束。

### 五、待验证事项

| 问题 | 本报告状态 | 所需证据 |
| --- | --- | --- |
| 原生永续与 HIP-3 各贡献多少基金买盘？ | ⚠️ 无法用现有近 30 日聚合数精确复算。 | 导出逐市场费用、部署方分成与基金逐笔成交，按同一 UTC 窗口汇总。 |
| 竞争份额与用户留存是否支持护城河？ | ⚠️ 尚缺统一市场分母和去重活跃用户序列。 | 按月比较市场份额、订单簿深度、有效费率、做市商和交易者留存。 |
| Labs 实际盈利和成本结构如何？ | ⚠️ 没有公开的完整法人损益表。 | 若有公司披露，另行核查；协议收入不能替代。 |
| “2025 年份额 70–80%”“数百万用户”“团队约 11 人”“0.07 秒出块”等流传说法？ | ⚠️ 未独立按同一时点和口径复算。 | 分别取得原始市场分母、去重用户定义、人事披露与网络实测数据。 |
| 基金回购能否覆盖代币释放？ | ⚠️ 需要同窗对账。 | 跟踪官方供应 API、贡献者实际划转、质押奖励、基金持币增量和买入成本。 |

### 资料口径

**项目方披露**用于说明产品机制与分配规则；**DeFiLlama、Strata 等第三方**用于估算费用、收入和回购；文中注明“自己复算”的合计、比例及倍数按列示快照计算。官方技术指标尚未独立压测，社区汇总不等于审计报表。早期人物传记、排行榜和未经固定日期核对的市场份额未作为本报告结论前提。

## HYPE 代币研究：供应、回购、解锁与持仓（原整理日期：2026-09-30）

整理与核对日期：2026-09-30（北京时间）。供应、价格、验证者质押采用 2026-09-30 约 01:30 北京时间的接口快照；第三方流通及收入数据采用 2026-09-29 查询快照。数值随区块和市场变化，不能把不同时间、不同定义的分母混算。本文的“官方”指 Hyper Foundation 公告或 Hyperliquid 文档/API，不等于经审计的财报。

### 核心结论

HYPE 的**最大供应上限为 10 亿枚**，但“当前有多少枚”至少有四种口径：原始已铸造总量、官方 API 流通量、数据商流通量，以及扣除 Assistance Fund 后的经济供给。2026-09-30 官方 API 显示约 **9.989 亿已铸造、2.987 亿流通**；2026-09-29 DeFiLlama 显示约 **2.2245 亿流通**。两者差约 **7623 万枚**，目前未取得可逐地址复核的完整桥接表。因此不能直接把任一“流通市值”当成唯一事实。[基金会创世公告](https://hyperfnd.medium.com/hype-genesis-1830a4dc2e3f)、[Hyperliquid API](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)、[DeFiLlama](https://investors.defillama.com/protocol/hyperliquid?events=false&fees=true&tvl=false)

### 1. 初始分配与用途

以下是**基金会 2024-11-28 公告的分配额度，不是目前各类持有人实持数量**。[原始公告](https://hyperfnd.medium.com/hype-genesis-1830a4dc2e3f)

| 类别 | 占上限 | 名义额度 |
| --- | ---: | ---: |
| 未来发行及社区奖励 | 38.888% | 3.8888 亿枚 |
| 创世用户分配 | 31.000% | 3.1000 亿枚 |
| 当前及未来核心贡献者 | 23.800% | 2.3800 亿枚 |
| Hyper Foundation 预算 | 6.000% | 6000 万枚 |
| 社区资助 | 0.300% | 300 万枚 |
| HIP-2 流动性 | 0.012% | 12 万枚 |

基金会称创世合格参与者获得的代币完全解锁，**未分发部分移入未来发行及社区奖励**；核心贡献者份额创世后锁定一年，大多在 2027–2028 年完成归属，部分更晚。公告称没有私募投资者、中心化交易所或做市商预留份额。这些是项目方原始披露；“社区占 76.2%”是其按分配用途的划分，不能直接理解成 76.2% 已由散户持有。[基金会创世公告](https://hyperfnd.medium.com/hype-genesis-1830a4dc2e3f)

HYPE 的主要用途：验证者质押与委托、HyperEVM gas、交易费质押折扣、HIP-3 部署保证金，以及生态应用使用。质押奖励来自未来发行储备，属于增量供给；不能把质押收益当成无稀释的协议分红。[创世公告](https://hyperfnd.medium.com/hype-genesis-1830a4dc2e3f)、[质押规则](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/staking)、[费率和质押折扣](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees)、[HIP-3](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals)

### 2. 供应量：四个容易混淆的数字

官方 API 查询：`POST https://api.hyperliquid.xyz/info`，请求体 `{"type":"tokenDetails","tokenId":"0x0d01dc56dcaaca66ad901c959b4011ec"}`。以下是接口值取约数；不是按分配比例推算。第三方值来自 DeFiLlama 2026-09-29 页面。[官方 API 说明](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)、[DeFiLlama](https://investors.defillama.com/protocol/hyperliquid?events=false&fees=true&tvl=false)

| 指标 | 数量 | 应如何理解 |
| --- | ---: | --- |
| 最大供应 `maxSupply` | 10.0000 亿 | 发行上限，并非当前已流通。 |
| 原始已铸造 `totalSupply` | 9.9890 亿 | API 原始链上总量，**仍含 Assistance Fund 地址余额**。与 10 亿上限相差约 110.09 万枚；差额不能全归因于回购。 |
| 官方 API `circulatingSupply` | 2.9868 亿 | API 在原始总量中剔除未来发行、指定非流通地址等后的口径。约占最大供应 **29.87%**（自己复算）。 |
| DeFiLlama 流通量 | 2.2245 亿 | 第三方更窄口径，约占最大供应 **22.25%**（自己复算）；与官方 API 相差约 **7623 万枚**。 |
| DeFiLlama `total supply` | 9.5531 亿 | 数据商调整后的总量，不能直接与官方原始 `totalSupply` 同义使用。 |

官方 API 同时列出 `futureEmissions` 约 **4.1116 亿枚**、一个非流通地址 `0x43e9…a251` 约 **2.4148 亿枚**、Assistance Fund `0xfefe…fefe` 约 **4757.28 万枚**，另有极小额零地址/死地址余额。**自己复算**：9.9890 亿 − 4.1116 亿 − 2.4148 亿 − 0.4757 亿 ≈ 2.9868 亿，与官方流通量吻合；最后的小额余额解释尾差。`0x43e9…a251` 的余额不能仅凭大小认定全部属于某一类团队份额，仍需官方地址归属表。[同一 API](https://api.hyperliquid.xyz/info)

按接口中间价约 **86.17 美元**乘官方流通量，**自己复算**约 **257.4 亿美元**；DeFiLlama 当日按其流通口径约 **193 亿美元**。这约 64 亿美元的市值差距主要是统计分母差异，不是价格瞬间异动。估值比较时必须同时列出价格、流通定义和截止时点。

### 3. 回购和“销毁”：两种不同动作

官方费率文档：交易费按产品和参与者分配，部分流向 HLP、部署方、做市返佣和 Assistance Fund；基金地址 `0xfefefefefefefefefefefefefefefefefefefefe` 在 L1 执行过程中自动将其收到的交易费换成 HYPE。官方表述为基金里的 HYPE 被销毁、从流通和总量中移除。[费率与基金规则](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees)

**实务上要分清：**

1. **基金买入并视同销毁**：接口快照基金地址约 **4757.28 万枚 HYPE**，约为最大供应的 **4.76%**（自己复算）。官方文档将这部分视为永久退出经济流通，但原始链上 `totalSupply` 尚包含其余额；它不是已经在链上全部执行 `burn` 的数量。
2. **直接减少原始供应**：原始 `totalSupply` 与 10 亿上限的差约 **110.09 万枚**。这只是当前相对上限的净差额，受实际铸造与销毁共同影响，不能等同“历史累计销毁量”。要算直接销毁必须逐笔汇总销毁事件。
3. **回购美元额、买入枚数、基金余额**是三个不同指标。基金余额是存量；历史累计买入可能更高，价格变动也改变美元估值。将基金地址余额乘现价，不等于历史回购花费。

“99% 收入回购”是容易误读的简称。DeFiLlama 对部分**符合规则的费用**使用 99% 流入基金的统计假设，但 HIP-3 部署方、builder fee、HLP、做市返佣等另行分配；不能说全部毛手续费的 99%、全部协议收入的 99% 或 Labs 利润的 99% 用于回购。[官方费用分配](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees)、[DeFiLlama 方法及损益](https://investors.defillama.com/protocol/hyperliquid?events=false&fees=true&tvl=false)

2026-09-29 DeFiLlama 近 12 月约 **9.11 亿美元费用**、**6.88 亿美元协议收入**，二者不可混称为回购额。稳定币 AQAv2 的约 90% **经成本调整后储备收益**分成预期进入基金，但截至核对时首笔款项尚未到帐，不能提前计入历史回购。[AQAv2 规则](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/aligned-quote-assets)、[首笔时间披露](https://blockworks.com/token-transparency/filing/hyperliquid)

#### 链上执行、地址与单笔金额（2026-10-15 补充）

【项目方披露】AF 自动把交易费转为 HYPE，是 **HyperCore / L1 内置执行机制**，不是需在 HyperEVM 上调用的普通 EVM 回购合约。官方系统地址为 `0xfefefefefefefefefefefefefefefefefefefefe`，可在 [HypurrScan](https://hypurrscan.io/address/0xfefefefefefefefefefefefefefefefefefefefe) 查看。[官方手续费文档](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees)（2026-10-15 查阅）。本文不把这个系统账户当作已公开 Solidity 源码的合约。

**销毁不必表现为再转给 `0xdead`。** 官方将 AF 地址中的 HYPE 认定为永久移出供应；2025 年末治理提案明确描述对不可提取余额的销毁认定，而非必须另发一次销毁交易。因此，地址保有余额与经济口径销毁并不矛盾；仍须与原始 API 的总量定义分别核对，避免把 AF 余额和包含 AF 的销毁汇总重复相加。【媒体转述】[The Block 的治理提案报道](https://www.theblock.co/news/defi/2025-12-17-hyper-foundation-proposes-removing-1-billion-hype-tokens-from-circulating-supply-by-zeroing-out-hyperliquids-assistance-fund-383091)（2025-12-17）；当前状态以官方费率文档为准。

**频率：持续自动执行，日/月是统计窗口，不是固定日/月预算。** 官方未在已查费率文档中承诺固定秒数或分钟数的下单周期。【社区观察】[hl.eco AF 页面](https://hl.eco/assistance-fund)描述分钟级回购；这不能当作协议保证。储备收益入账周期、订单提交时间和实际成交时间是三件事。未完成逐笔历史采集前，不宣称已经独立验证当前分钟频率。

**资金分配规则不等于单笔订单算法。** 已查官方说明没有完整披露单笔触发门槛、订单大小、价格偏移和拆单公式；不将“99%”解读为每笔手续费到账立即以其99%提交市价单。买盘能力来自实际进入 AF 的费用、其他收益及可用余额，实际支出以成交为准。

核验公式（方法定义，尚非执行结果）：

- 期间买入名义金额 = Σ（每笔 HYPE 买入数量 × 该笔实际成交价）；按报价币记录，再按明确汇率换算美元。执行费用如有另列。
- 回购买入均价 = 同一窗口买入名义金额 / 买入数量。
- 按每种资金资产分别对账：期初可用余额 + 期间流入 − 买入结算支出 − 执行费用 ± 其他净变动 = 期末可用余额；未成交订单占用与余额口径须一致。
- AF 的 HYPE 余额增量须剔除非买入转入及其他调整，才可与成交数量对比；初始分配不算市场回购。

**AQAv2 的历史窗口与后续披露分开。** 上文“首笔尚未核实到账”对应2026-09-29快照，不是截至本次更新仍未到账。【第三方披露】[Blockworks token transparency filing](https://blockworks.com/token-transparency/filing/hyperliquid)称截至2026-10-06已记录首笔约1,458万USDC于10月4日UTC进入AF；本轮未独立重建该流水，不回填为9月已完成回购，也不将该入账额直接当作当日成交支出。

#### 情报监听要点（研究建议，尚未配置）

目标是识别回购买盘、资金来源及供给压力的变化，不对每次正常买入发通知。

| 对象 | 保存内容 | 研究用途 |
| --- | --- | --- |
| AF 实际买入 | 成交标识、时间、币对、方向、价格、数量、名义金额、执行费用、来源与采集时间 | 汇总实际金额/枚数/均价；成交去重，避免把挂单当成交 |
| AF 资金和余额 | 资金流水标识、来源地址、资产、金额、时间、余额及占用口径 | 分开手续费、储备收益、其他转入与未花资金 |
| 费用及分成 | 原生永续、HIP-3、现货等费用、部署方/前端分成和数据商定义 | 分析收入可持续性；来源未核实则保留未知，不强行分摊 |
| 供给和治理 | 实际解锁/分配、奖励、AF视同销毁、直接销毁及规则公告 | 同窗比较供给与买盘；不把解锁自动当实际卖出 |

【我的推演】初始可考虑分钟级采集成交及资金、每日UTC汇总、每周比较7/30日趋势；采集频率不代表协议下单频率。先补最近90天并核验来源覆盖、分页限制、去重和对账，再依据历史分布设报警阈值；目前未承诺该90天可完整追回。

值得提示的变化：大额非手续费入账；回购显著偏离历史水平；有可用资金却持续未成交；费用来源结构变化；官方更改费用分配或权限。阈值和通知渠道尚未设定。**抓取失败、记录缺口与真实回购中断必须分别标记。** 单笔资金来源无法追溯时不能把所有买入都归因为某一收入。

日表至少包括：日期、实际买入金额/枚数/均价、费用及储备收益等已识别流入、未知流入、期末资金、实际新增流通及数据完整性。重点比较持续/一次性收入、7/30日买入趋势，以及同窗移除数量相对新增流通数量；零分母或流通定义不一致时不输出比例。

#### 最近一个月实际回购量级（2026-09-29 快照）

第三方 [Strata Terminal](https://app.strata-terminal.com/buybacks/hype) 用成交记录和早期基金余额曲线复原的**过去 30 天实际回购美元额约 5690 万美元**，约合 **每天 190 万美元**；该来源注明 2026-06-24 以后使用交易所 API 的精确成交记录，之前的数据为复原值。另一个独立索引 [HypeBasis](https://hypebasis.io/revenue) 比较 2026-08-30 至 09-28 的基金地址快照，显示净增加约 **67.18 万枚 HYPE**，约合每天 **2.27 万枚**。两个来源的时间窗相差约一天、方法也不同，因此只可合并表述为**近期每 30 天约 5500–6000 万美元、约 65–70 万枚 HYPE 的量级**，不能宣称是精确匹配的一组交易账。按 5690 万美元 ÷ 67.18 万枚，隐含均价约 **84.7 美元/枚**，仅供量级校验；完整同窗均价应从逐笔成交复算。

这不是固定月度预算。交易量、费率、部署方分成、HYPE 成交价格都会改变美元额和枚数。DeFiLlama 同期约 **5633 万美元的 30 日协议收入**与 Strata 回购额接近，但定义不完全相同，不能逐美元画等号。AQAv2 储备收益尚未计入上述已完成回购。

#### Assistance Fund 的资金如何进来

**先有用户交易费，再有基金买入。** HyperCore 每笔永续/现货交易按交易者的 14 日交易量、质押折扣、maker/taker 身份和市场设置计算费用。原生永续基础档为 taker **0.045%**、maker **0.015%**；现货基础档为 taker **0.070%**、maker **0.040%**。实际费率可能低得多，不能用固定费率乘全平台交易量直接推基金收入。[官方费用表](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees)

| 流入渠道 | 先经过什么分配 | 基金实际得到什么 |
| --- | --- | --- |
| 原生永续交易费 | 交易者支付费用；做市返佣、推荐激励及 HLP 等按规则分配。 | 剩余符合规则的交易费份额由协议自动换成 HYPE，进入基金。官方文档未给出可适用于所有产品的统一总费比例；第三方 [DeFiLlama](https://investors.defillama.com/protocol/hyperliquid?events=false&fees=true&tvl=false) 的特定适用费基模型使用 99%。 |
| HIP-3 永续交易费 | 市场部署方可以设置额外 fee share；官方范围为基础协议费的 0–300%，growth mode 另有约束。builder code 如果被用户授权，还会另收前端费用。 | **协议保留的交易费份额**进入常规费用分配，再有一部分进入基金；部署方和 builder 收入不归基金。growth mode 可将综合费率大幅降低，故 HIP-3 交易量增长不必然同比例增加基金买盘。[HIP-3](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals)、[费用公式](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees)、[builder code](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes) |
| 现货交易费 | USDC 计价部分按协议及部署方设置分配；对非 USDC 本币资产，代币发行方可获得其代币计价手续费的一部分。 | 符合规则的协议费用进入基金。非 USDC 报价代币的相关费用，官方 HIP-1 文档明确指向基金；**本币资产手续费未给部署方的部分则直接销毁该本币**，应与基金买 HYPE 区分。[HIP-1 费用说明](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-1-native-token-standard) |
| 稳定币储备收益 | USDH 发行方文档承诺将 **50% 储备收益**贡献基金；AQAv2 要求符合条件的发行方将其 Hyperliquid 供应对应约 **90% 经成本调整后储备收益**与协议分享，按 30 日计提、结束后 8 日转基金。 | 这是与交易费分开的收入线。USDH 实际汇款须按转账查；截至 2026-09-29，AQAv2 的预期首笔收入尚未证实入帐，不能计入过去 30 日实际回购。[USDH 发行方](https://docs.usdh.com/usdh/reserves)、[AQAv2 官方规则](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/aligned-quote-assets) |

**不要混入基金的项目：**资金费率是多空交易者之间的转移，协议不从资金费支付中收费；builder code 费用属于获得授权的应用开发者；HLP 的手续费份额与做市/清算收益属于金库及其存款人；HIP-1/HIP-3 部署拍卖以 HYPE 计的费用、HIP-3 罚没和 HyperEVM gas 销毁等可能减少 HYPE 供应，但不能自动记作 Assistance Fund 的 USDC 流入或其市场回购。[资金费率](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding)、[builder code](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes)、[HLP](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/protocol-vaults)、[Blockworks 财务分类](https://blockworks.com/analytics/hyperliquid/hyperliquid-financials)

**数量级对账：**[DeFiLlama](https://investors.defillama.com/protocol/hyperliquid?events=false&fees=true&tvl=false) 2026-09-29 快照的近 30 日总费用约 **7266 万美元**，其定义下协议收入约 **5633 万美元**；[Strata](https://app.strata-terminal.com/buybacks/hype) 的同阶段基金实际买入约 **5690 万美元**。三者的覆盖项目、采样边界和日期稍有不同，**7266 万 ≠ 全部进基金**，而后两个数字接近只能作为合理性检查，不能作为逐笔财务勾稽。要做精确对账需汇总基金地址逐笔 HYPE/USDC 成交、各市场费用与稳定币转账。

#### 近 30 日来源金额拆分（2026-09-29 数据快照）

依据 DeFiLlama 公开 API 的同日父协议及子协议 `dailyRevenue` 口径，**自己复算**如下；这里的 *revenue* 是数据商归于协议/代币持有人的价值，**并非 Assistance Fund 地址逐笔入账表**。[永续 API](https://api.llama.fi/summary/fees/hyperliquid-perps?dataType=dailyRevenue)、[现货 API](https://api.llama.fi/summary/fees/hyperliquid-spot-orderbook?dataType=dailyRevenue)、[母协议 API](https://api.llama.fi/summary/fees/hyperliquid?dataType=dailyRevenue)

| 来源 | 近 30 日归属收入 | 占合计 | 与 Assistance Fund 的关系 |
| --- | ---: | ---: | --- |
| 原生永续 + HIP-3 永续（合并） | **5414.56 万美元** | **96.1%** | DeFiLlama 模型中的主要基金买盘来源；未提供可核验的同窗原生/HIP-3 二级拆分。 |
| 现货（含少量直接拍卖销毁项目） | **218.24 万美元** | **3.9%** | 大部分是交易费流向基金；其 `revenue` 方法也计入 HIP-1 部署拍卖直接销毁，故不能把全额都说成基金入账。 |
| **合计** | **5632.81 万美元** | **100%** | 与 Strata 实测 5690 万美元买入数值接近，但来源、日界和分类不同。 |
| AQAv2 储备收益 | **本窗口尚无已核实到账额** | — | 不应把未来预期计入。 |
| USDH 储备收益 | **本窗口缺少可复核的基金转账拆分** | — | 发行方规则存在，但本表不填假定金额。 |

HIP-3 的**毛费用**和协议收到的份额也须分开。例如 [DeFiLlama tradeXYZ 页面](https://defillama.com/protocol/tradexyz?events=false&fees=true&tvl=false) 同期显示其部署市场近 30 日用户支付约 **640 万美元**费用、其自身收入约 **212 万美元**；这两个数都不能直接加到上表的 5415 万美元上，因为该永续合并项已经包含协议从 HIP-3 收到的部分，前述两项还包含不同口径的部署方费用和折扣。

作为费用去向的另一个视角，DeFiLlama 截至 2026-09-29 的**2026 Q3 未完结季度**表列毛费用约 **1.9064 亿美元**，其中永续约 **1.6185 亿**、现货约 **454 万**、builder code 约 **2258 万**、Unit 现货约 **119 万**、部署拍卖直接销毁约 **47 万**；分给 builder 约 **2258 万**、做市返佣约 **780 万**、HIP-3 部署方约 **864 万**、HLP 约 **144 万**，加上其余成本后列示归属收入约 **1.4272 亿**、代币回购栏约 **1.4225 亿美元**。这是**季度费用分类**，不可与上表近 30 日合并求和。[DeFiLlama 分季损益表](https://investors.defillama.com/protocol/hyperliquid?events=false&fees=true&tvl=false)

**供给净变化的判断式**：下一期可交易供应 ≈ 本期可交易供应 + 实际释放/新发行 − 实际锁定/退出流通。质押锁定可降低短期可售量，但不减少代币所有权；解押后可重新流通。基金买入与新发行需按相同时间窗比较，不能仅凭回购就断言净通缩。

### 4. 解锁：已披露的边界比“每月 992 万”重要

基金会只公开了贡献者总分配、创世后一年锁定、大多数在 2027–2028 年完成归属的原则，**没有可逐月核验的完整人员归属表**。[基金会创世公告](https://hyperfnd.medium.com/hype-genesis-1830a4dc2e3f) 社区页 [hl.eco](https://hl.eco/revenue-buybacks) 明确因未公布团队归属时间表而不预测未来团队解锁。因此外部流传的“每月约 992 万枚直到 2027 年”至多是理论摊销/模型假设，不能当成每月确定的链上转账，更不等于每月卖压。研究时应分开记录：**可归属额度、实际划转、进入交易所的数量、实际卖出**。目前仅凭公开材料无法完整核定这四项。

#### 各部分如何进入可交易供给

| 部分 | 释放路径 | 公开日程与观察方法 |
| --- | --- | --- |
| 未来发行与社区奖励 | 用于验证者/委托者质押奖励，以及未来社区激励；质押奖励从**既有预留额度**支付，不突破 10 亿上限。 | 无完整固定发行日程。官方称奖励按分钟计提、每日发放并自动复投；速度随总质押量变化。应跟踪 `futureEmissions` 余额和实际奖励流出。[质押文档](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/staking) |
| 核心贡献者 | 一年锁定期后按各自归属安排取得代币；归属、钱包划转与出售是三件事。 | 大部分 2027–2028 年完成，少数更晚。外部日历常列每月约 992 万枚，但完整个人归属表未公开；DeFiLlama 的解锁页改用 Labs 钱包向贡献者实际转账跟踪，2026-09-06 列示一笔约 43.34 万枚，亦不能据此推断该月只有这一笔。[基金会公告](https://hyperfnd.medium.com/hype-genesis-1830a4dc2e3f)、[DeFiLlama 解锁方法](https://defillama.com/unlocks/hyperliquid) |
| 基金会预算与社区资助 | 基金会按预算/资助用途划转，收款者之后可能持有、质押或卖出。 | 基金会未公布可逐月核验的完整支出时间表；按链上实际转账统计，而非按 60 个月机械摊销。[基金会公告](https://hyperfnd.medium.com/hype-genesis-1830a4dc2e3f)、[DeFiLlama 解锁备注](https://defillama.com/unlocks/hyperliquid) |
| 创世分配未领取部分 | 按基金会规则转入未来发行与社区奖励池。 | 不应再重复计为待领取的原始创世空投。[基金会公告](https://hyperfnd.medium.com/hype-genesis-1830a4dc2e3f) |

尤其要避免一个算术误区：官方 API 当前 `futureEmissions` 约 **4.1116 亿枚**，大于创世公告的 3.8888 亿初始额度，原因之一是创世未分发部分会转入该池；两者不是同一时点的数值。**不能**简单把 `10 亿 − 官方流通约 2.987 亿 ≈ 7.013 亿` 全部解释成“未来按固定日期解锁”。这部分同时包含未来奖励储备、指定非流通地址及被视同销毁的 Assistance Fund，机制与可售性各不相同。[基金会公告](https://hyperfnd.medium.com/hype-genesis-1830a4dc2e3f)、[官方 API](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)

#### 补充（2026-10-12 更新）：cliff 之后实际是“月度 announced claim”机制，且真实申领远小于理论上限

上文“无逐月日历”的判断仍成立（官方从未公布未来逐月实际分配表），但 2025 年 12 月起出现新的披露机制，第三方追踪数据显著改变了供给压力的画面。以下关键事实来自 [tokenomist.ai 研究](https://tokenomist.ai/research/hype-tokenomics-330k-or-9-9m-hype-unlocks)（2026-04-01，二手转述、链上数据待自核）并经媒体交叉印证：

- **每月 6 日分配节奏**：2025-12-28 联合创始人 Iliensinc 在 Discord 宣布解押 120 万枚用于 2026-01-06 分配，确立“每月 6 日”分配节奏（crypto.news 转述）。
- **归属时间表更新**：Hyper Foundation 于 2025-12-29 更新 Core-contributor Token Release Schedule，但第三方投影仍按 238M ÷ 24 个月 = 每月 991.67 万枚的**理论上限**计算。
- **实际 announced claim 记录**（占理论上限比例）：2025-11 为 17.6%、2026-01 为 120 万枚、2026-02 仅 1.4%（约 13.9 万枚）、2026-03 为 173,217 枚、2026-04 公告约 33 万枚——**实际申领比投影低 30~57 倍**。
- **合同层面已解锁 405.41M vs 累计实际申领仅约 3.19M**（申领率 0.79%，截至 2026-03-23），约 402.22M 枚仍留在归属钱包未领取。“解锁”与“申领/卖出”是两个量级完全不同的事件。
- **市场曾按上限定价引发恐慌**：CoinTelegraph 报道“$314M 解锁引发清晰度呼吁与卖压警告”，社区有公开信要求主动沟通——2025-12~2026-01 的价格下跌部分是**按 9.92M/月上限的恐慌定价**，而非真实卖压（这也解释了 2026-01-21 后 V 型修复之干脆）。媒体曾流传“2026-01-06 解锁 1,200 万枚”，与另一来源的 120 万枚相差 10 倍，采信 1.2M（与 Discord 公告一致）。
- **2026-10-14 更新：2026-10 期次公告已落地，且金额跳升一个量级**。2026-09-30 Iliensinc 在官方 Discord 宣布：Hyperliquid Labs 解押 **375 万枚 HYPE**（约 $3.3 亿），10-07 分配给团队成员；该批代币属于**与一家机构达成的 OTC 交易，不在公开市场出售**（[Foresight News](https://foresightnews.pro/news/detail/105873)、[PANews](https://www.panewslab.com/en/articles/01a106e2-b707-716e-9aa8-b89445729ef3)、[BingX 快讯](https://bingx.com/en/flash-news/post/hyperliquid-team-says-m-hype-tokens-to-be-sold-otc-to-institution-not-on-open-market)，2026-09-30/10-01，媒体转述 Discord、链上待自核）。对比：4 月公告仅 33 万枚，10 月跳升约 11 倍，为 2026-01（120 万）以来最大单次。性质与此前不同：**OTC 不走公开市场，不直接构成现货卖压**，但说明团队开始将归属份额货币化、且新增一个机构级持币方——两者都应在基本面中记为供给结构变化。
- **下一次日历节点**：2026-11-06 前后（每月 6 日分配节奏）。官方 API 不提供归属表查询（info 端点 `genesis`/`tokenDistribution` 已不可用，2026-10-14 实测），逐月核对依赖 Discord 公告 + 链上 vesting 合约监听（方案见 pair 全记录实盘章节）；tokenomist 三阶段数据（Whitepaper Estimate → Committed → Completed）可作交叉验证，而非日历投影。
- **2026-10-15 事件复盘（自己复算，币安 1m 线 + Hyperliquid 永续 1h/1m）**：① **公告日 9-30 不是下跌而是大涨**：HYPE/BTC 单日 **+5.83%**（公告 15:34 UTC 前比率还在日内低位 −0.8%，随后拉升）——"OTC 不走公开市场"被解读为利空出尽；② 10-01 获利回吐 −5.19%，10-02 收复 +2.18%；③ **真正的相对下跌在分配日当周**：10-07 ~ 10-09 HYPE/BTC 累计 **−11.8%**（10-07 分配日全天 −3.83%，日内持续走低），但同期 BTC 自身每日 −3% ~ −4.5%，属大盘普跌中 HYPE 高 beta 放大，**无法干净归因于解锁事件**；④ 10-04 → 10-14 比率累计 −13.5%，同期 BTC 现货 84.8k→81.7k。30MA 状态：币安日口径 10-04 一度跌破 30MA；HL 1h 口径 10-14 仍在 30MA 上方（0.000977 vs 0.000877）但快速逼近——**overlay 信号处于临界区**。教训重申：跟踪 announced claim 而非日历投影者，9-30 的 +5.83% 与 10-01 的 −5.19% 都吃得到也躲得开；按"10-29 投影 1,417 万枚"提前空仓者两边挨打。

### 5. 持仓分析：所有权与验证者控制权不能混为一谈

#### 5.1 质押和验证者控制

官方 `validatorSummaries` 接口于 2026-09-30 约 01:30 北京时间返回 **35 个验证者，其中 27 个活跃**；全部委托质押约 **4.4097 亿 HYPE**，活跃验证者对应约 **4.4091 亿**。与 10 亿上限相比约 **44.1%**（自己复算），但其中可能包含非流通分配；**不能从官方流通量中再减去全部质押量**。[验证者 API](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)、[质押规则](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/staking)

按活跃质押权重自己复算：前 3 个验证者约 **36.7%**，前 5 个约 **52.3%**，前 10 个约 **76.1%**。名称为 `Hyper Foundation 1` 至 `Hyper Foundation 5` 的五个验证者合计约 **2.1146 亿 HYPE**、占活跃质押约 **48.0%**。这是**验证者获得委托的投票/出块权重**，不是基金会自有代币持仓：外部用户也可能委托给这些节点，节点运营方不因此拥有委托者代币。集中度值得持续跟踪，但不能表述为“基金会持有总供应 21%”。

#### 5.2 现货地址榜不能直接当作持有人榜

第三方 [Hypurrscan HYPE holders API](https://api.hypurrscan.io/holders/HYPE) 在 2026-09-29 17:21 UTC 的索引显示约 **26.02 万个 HyperCore 现货持币地址**、这些地址现货余额合计约 **1.2910 亿 HYPE**。其中榜首 `0x2222…2222` 约 **5133.52 万枚**是 HyperCore ↔ HyperEVM 转移的系统地址；第二位 `0xfefe…fefe` 约 **4757.26 万枚**是 Assistance Fund。两者合计约占该索引现货余额的 **76.6%**（自己复算），**都不能当作单一私人巨鲸**。[系统跨层转移说明](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/hyperevm/hypercore-less-than-greater-than-hyperevm-transfers)、[基金地址说明](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees)

剔除上述两系统地址后，索引中的现货余额约 **3019.43 万 HYPE**；前 10 个非系统地址合计约 **606.79 万枚**，占这个**有限的现货样本**约 **20.1%**（自己复算）。这不是全链前十持有人占比：质押余额、HyperEVM、托管账户和多地址实体无法从这一张榜单完整归集。地址数也不等于去重人数。当前没有可靠的全链受益所有人分布，故“散户占多少/团队实际持有多少/前十巨鲸控制多少”均标记为 **⚠️ 无法复算**。

### 6. 投资研究应盯的五个序列

| 序列 | 要回答的问题 | 优先来源 |
| --- | --- | --- |
| 同口径流通量与指定非流通地址余额 | 可出售供给有没有上升？不同平台差额如何变化？ | 官方 `tokenDetails`，对照 DeFiLlama |
| Assistance Fund HYPE 净增加量、对应买入成本 | 费用转化为多少代币需求？基金持币有无异常流出？ | 官方基金地址、链上成交记录 |
| 实际团队/基金会划转和交易所流入 | 理论归属是否变成真实卖压？ | 官方已知地址加链上追踪，未知归属须保留 |
| 质押总量、验证者前五/前十权重 | 网络安全和治理是否过度集中？ | 官方 `validatorSummaries` |
| 交易量 → 毛费用 → 留存收入 → 基金买入 | 业务增长能否持续覆盖新增发行？ | Hyperliquid 费率、DeFiLlama、基金地址 |

### 资料与复核限制

- **项目方/当事人披露**：Hyper Foundation [创世公告](https://hyperfnd.medium.com/hype-genesis-1830a4dc2e3f)；Hyperliquid [费用](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees)、[质押](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/staking)、[API](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint) 文档。API 实时返回值是链状态快照，地址归属仍可能需人工解释。
- **第三方统计**：[DeFiLlama](https://investors.defillama.com/protocol/hyperliquid?events=false&fees=true&tvl=false) 的流通、费用及收入；[Hypurrscan](https://api.hypurrscan.io/holders/HYPE) 的 HyperCore 现货地址索引。第三方口径与官方 API 暂未完全对账。
- **自己复算**：文中比例、两个流通口径差额、市值乘法、系统地址剔除与质押集中度；计算均基于所列快照，四舍五入可能有少量尾差。未取得审计级、跨 HyperCore/HyperEVM/质押账户的统一受益持有人清单。

## 市场看空 HYPE 的理由清单（整理日期：2026-10-10）

背景：常驻 pair 净值在前期（2025-10 ~ 2026-01）回撤的归因显示，HYPE/BTC 比值 −60% 的滑落由"HYPE 独立下跌"主导（最差 10 天中多次 BTC 涨/HYPE 跌，滚动 beta 1.80→0.69、corr→0.30，与 2025-11-28 创世周年解锁窗口吻合，见 `factcheck/dd_decompose.py` 与 pair策略全记录）。本条清单系统盘点市场可能看空 HYPE 的理由，按证据强度分层，同时作为 pair 策略的风险清单。标注口径：✅自己复算／官方披露 🟡媒体转述。

### 总览

| # | 理由 | 性质 | 证据强度 |
|---|---|---|---|
| 1 | 贡献者解锁：2.38 亿枚 2027–2028 归属 | 供给 | ✅ 官方公告+复算 |
| 2 | 流通口径不透明：两口径差 7,623 万枚 | 供给/治理 | ✅ 复算 |
| 3 | 创世空投零成本筹码长期悬顶 | 供给 | ✅ 官方分配 |
| 4 | FDV/收入约 120 倍，且收入是周期顶部 | 估值 | ✅ 复算 |
| 5 | 手续费周度趋势已在回落 | 基本面 | ✅ 复算 |
| 6 | 竞争对手补贴可买走份额，Hyperliquid 不补贴 | 竞争 | 🟡 媒体+数据商 |
| 7 | 收入单一依赖永续手续费 | 基本面 | ✅ 本文研究 |
| 8 | HIP-3 预言机/部署方分成 | 结构 | ✅ 本文研究 |
| 9 | 验证者集中 + JELLY 投票改规则先例 | 治理 | ✅ 复算+多方报道 |
| 10 | HLP 是全员对手盘，极端市况接刀 | 运行 | ✅ 事件记录 |
| 11 | 高 beta + 浅流动性，普跌放大 | 市场结构 | ✅ 已验证 |
| 12 | 资金费长期为正，做多 carry 差 | 市场结构 | ✅ 复算 |

### A. 供给端：最大的空头理由

1. **解锁悬崖**：贡献者 2.38 亿枚（23.8%）创世锁一年、2027–2028 归属——对现流通 2.2~3.0 亿枚接近再造一个流通盘。官方无逐月日历，"每月 991.67 万枚"是 24 个月直线假设（见本文第二部分第 4 节）。媒体另报道 2026-01-06 一次 1,200 万枚解锁（原定 1,700 万缩减，[LinkedIn 转述](https://www.linkedin.com/posts/cryptobhrata_hyperliquid-hype-tokenunlock-activity-7412830282321604608-b8CV)），时间落在 2025-12~2026-01 的 HYPE 独立下跌窗口内。**市场在解锁前 1–2 个月抢跑定价**，这也是 2026-01-21 谷底后 V 型修复的机制。
2. **流通口径混乱本身就是折价理由**：官方 API 2.987 亿 vs DeFiLlama 2.2245 亿，差 7,623 万枚（约 $64 亿市值分母差），无逐地址桥接表可核。分母不确定时市场倾向按保守口径定价。
3. **零成本筹码**：创世用户 3.1 亿枚完全解锁、成本为零，任何价位都有理性卖家，反弹即卖压。

### B. 估值端：贵，且分母在缩小

4. **FDV/归属收入约 120.5 倍**（2026-09-29 快照自己复算：FDV $828.7 亿 ÷ 近 12 月归属收入 $6.88 亿；非市盈率，持有人不直接获得现金流）。8 月底已有直接以估值质疑为题的空头分析（[Investing.com](https://www.investing.com/analysis/hype-the-18-billion-question--can-hyperliquid-outgrow-its-valuation-200686830)）。
5. **分母在缩**：周度核对结论是 ❌"手续费持续上涨"不符，最近 13 周 fees 与回购明显低于最初 13 周（见 factcheck/基本面数据核对合集）。分子高、分母缩，是戴维斯双杀配方。

### C. 竞争与基本面

6. **份额可被补贴买走**：2025Q4 Aster 积分激励把日成交份额一度抢到 ~70%、Hyperliquid 跌至 ~10%（[Buildix](https://www.buildix.trade/blog/perp-dex-market-share-august-2026)、[CleanSky](https://cleansky.io/blog/hyperliquid-vs-gmx-vs-dydx/)；后续分析指对手有刷量成分，Hyperliquid 已恢复至 ~38%）。要害不在那一次输赢，而是 Hyperliquid 不补贴的策略意味着份额存在真实下行风险。
7. **收入结构单一**：几乎全部来自永续手续费，链上永续是波动率驱动的周期生意。
8. **HIP-3 双刃剑**：股票类永续（如 xyz:NVDA）价格源是部署方预言机，操纵时损失承接无公链级确定性；部署方还分走部分手续费。

### D. 治理与运行

9. **验证者集中 + "规则可改"先例**：27 个活跃验证者、前五名占质押权重 52.3%（2026-09-30 快照自己复算）。2025-03-26 JELLY 事件：操纵者逼 HLP 承接深度浮亏空头（峰值 $12–13.5M），验证者 2 分钟投票下架并强制按 $0.0095 结算（[Blockworks 透明文件](https://blockworks.com/token-transparency/filing/hyperliquid)、[HyperAcademy](https://hyperacademy.io/en/articles/hyperliquid-security-and-hack-risk)）。结果保护了 HLP，但开创了"压力下规则可投票改写"的先例——对"链上规则不可变"叙事是根本性扣分。
10. **HLP 是全员对手盘**：2025-03-13 ETH 操纵已致 HLP 损失 ~$4M；若某次极端市况 HLP 大亏，信心危机直接传导 HYPE 价格。另发生过 Lazarus 关联地址恐慌（30 小时净流出 ~$2.56 亿）与 37 分钟 API 中断（[Datawallet](https://www.datawallet.com/crypto/hyperliquid-explained)、[CoinRadar](https://coinradardaily.com/companies/hyperliquid)）。

### E. 市场结构

11. **高 beta + 浅流动性**：2025-10~2026-01 已验证，HYPE 复利 −58% vs BTC −28%（dd_decompose.py 复算）。
12. **资金费长期为正**：HYPE 多头全年净付 5.76%（4h 间隔、80% 为正）——做多 carry 为负，压制期货多头与杠杆持仓意愿。

### 怎么读这张清单

- **一次性 vs 结构性**：解锁卖压、竞争刷量"会过去"（利空出尽即 V 回，2026-01 已演示）；估值倍数、收入周期性、验证者集中"过不去"，每次反弹都被重新定价。
- **对 pair 策略的含义**：本清单 ≈ pair 净值回撤来源清单。可日历化的跟踪项——2027–2028 贡献者归属节奏、月度解锁公告——应进监控；竞争份额与周度手续费已有数据管线（factcheck/基本面数据核对合集）。
- **反向注意**：以上均为市场共识叙事，价格已计入相当部分（120 倍仍有人买，多头有回购+销毁+份额恢复的对冲逻辑）。看空的边际信息不在"有没有这些理由"，而在"哪条在恶化"——截至 2026-10 我们自己数据里在恶化的只有手续费周度趋势，其余为存量事实。
