# 输入约定

模型v0.1.0。参照包内 `assets/example-input.json` 组织输入；该文件所有事实均为示意，不能用其替代真实公司数据。

| 字段 | 类型及口径 |
|---|---|
| schema_version | 整数1；未知字段或重复JSON字段报错 |
| company / share_basis | 公司与股类、股价和股数的共同证券单位，非空字符串 |
| currency | USD/CNY/HKD/EUR/JPY/GBP/TWD/KRW/CAD/AUD；本程序不换汇 |
| price / price_date | 每证券单位价格，正数；YYYY-MM-DD基准日期 |
| net_profit / profit_unit | 年度归属普通股股东净利润，正数；unit/M/B分别为原币/百万/十亿，禁止混不同金额单位 |
| profit_period_start / profit_period_end | 完整年度起止，YYYY-MM-DD，本版接受350—380天含首尾；不接受半年/单季年化或亏损 |
| profit_basis | 明确归属、GAAP或调整后、可比性；不混归母利润和非归属集团总额 |
| current_shares / target_shares | 实际证券单位数量，正数；不是百万股数。与price同单位；目标数为用户确认假设 |
| target_fiscal_year / target_date | 用户给定的财年标签及准确期末，晚于价格日/利润基期末；财年标签不从自然年猜测 |
| required_return | 必要年化回报率，小数，如0.10=10%；需>-1，不是百分数10 |
| target_pe / sensitivity_pe | 正PE及1—7个PE组成列表，含目标PE、不重复；敏感性范围也需确认 |
| assumptions_confirmed | 布尔true，表示用户实际确认模型与假设；不可自动推定同意 |
| applicability | comparable_profit=true、major_capital_changes=false、special_industry=false，均为布尔值；不满足则本模型不适用 |
| evidence | 必须含price/net_profit/current_shares三个对象，格式见下 |

每个来源对象：`source`写来源名称、URL或附件页码；`status`为user_input、verified、synthetic；`source_date`为该资料的公开/行情日；`currency`金额为上方币种，股数为shares。状态是提供者声明，脚本没有自动检查来源真伪。只有实际核对过才能标verified，报告仍明确该标签由提供者给出。

所有来源日期不得晚于价格日；价格来源日等于price_date，利润来源日不能早于利润期末。实际公司通常在财年末之后披露年报，选择历史价格时必须遵守真实披露日；演示中同日数值仅因纯示意构造而成立。

脚本返回同名JSON及HTML。JSON保留原输入、模型版本、输入哈希、基准/延迟/敏感性结果和限制；HTML从同份结果渲染。输入原文件不修改，已有报告不覆盖。日期按完整周年＋下一周年实际天数的比例计时，2月29日跨非闰年周年按2月28日处理。

增长率分母年数：从年度利润基期末到目标期末。投资回报分母年数：从价格基准日到目标期末。若基期较旧，报告提示局限，不能把旧利润当最新TTM。超出支持的年度长度或币种先说明不支持，不修改输入掩盖。
