# Token K线同步工具

最新数据归档：2026-10-05已完成HYPE/BTC完整一年**1分钟**K线（各525,600根，与5分钟快照同窗口并逐根交叉核对一致），详见《2026-10-05-一年1分钟K线同步.md》；此前2026-10-04已完成完整一年5分钟K线（各105,120根），详见《2026-10-04-HYPE与BTC一年5分钟K线同步.md》。最近一年同步可使用`--months 12`。

整理及接口核对日期：2026-10-02。

## 统一方法

指定币种、市场来源、周期和时间 → 下载并保留原始响应 → 统一OHLCV结构 → 核对缺口、重复和价格边界 → 保存结果与来源清单。

脚本：`factcheck/sync_prices.py`。运行环境：Python 3、requests。命令从stock_research工作区根目录运行。

## 常用命令

ETH最近三个自然月、5分钟K线：

```sh
python3 数字资产/factcheck/sync_prices.py --tokens ETH --source binance-perp --months 3 --interval 5m
```

批量同步，固定区间：

```sh
python3 数字资产/factcheck/sync_prices.py --tokens HYPE BTC ETH --source binance-perp --interval 5m --start 2026-07-02T00:00:00+08:00 --end 2026-10-02T00:15:00+08:00
```

Hyperliquid近期原生永续行情：

```sh
python3 数字资产/factcheck/sync_prices.py --tokens HYPE ETH --source hyperliquid-perp --interval 5m --start 2026-10-01T00:00:00+08:00
```

需要ETH现货，改用 `--source binance-spot`。币种必须在指定市场存在；不支持的币种会报错，不承诺任何token均可下载。

## 参数

| 参数 | 含义 |
|---|---|
| --tokens | 空格分隔币种代码，如ETH BTC HYPE，不加USDT |
| --source | 必选：binance-perp、binance-spot、hyperliquid-perp |
| --interval | 默认5m；可选1m/3m/5m/15m/30m/1h/2h/4h/8h/12h/1d |
| --months | 向前自然月数量，以北京时间计算，月底按目标月天数调整 |
| --start | 固定起点，必须附时区；与months二选一 |
| --end | 左闭右开的终点；默认最近已完成K线边界 |
| --allow-partial | 显式接受缺口，重复及异常OHLC仍不通过 |

时间须对齐UTC K线周期，不含未完成K线。months使用同一北京时间时刻推算起点，不额外延长到起始日午夜。

## 限流与并发

- Binance合约/现货K线接口按weight限流：默认每IP **2,400 weight/分钟**，`limit=1000`时每请求权重10。工具以**不低于0.30秒/请求**的节奏分页（约2,000 weight/分钟，留约20%余量），并检查响应头`X-MBX-USED-WEIGHT-1M`：超过2000时打印警告并等待下一分钟窗口。
- 收到**429/418**时按`Retry-After`退避（限流等待不消耗三次传输重试次数），连续退避10次仍被限制则该币报❌同步失败；已下载页面都在缓存里，直接重跑即可免费续传。
- 不要并行运行多个同步实例，也不要与其他高频API请求共用出口IP；云端/共享IP的限额可能更严格，被限流时工具会自动放慢，失败则稍后重跑。
- Hyperliquid为单请求快照，每次请求前有1秒礼貌间隔；其接口另有自身的IP限制。
- 缓存命中的页不发起任何请求，重跑、核对、滚动区间的重叠部分都不产生流量。

## Hyperliquid的历史限制

HYPE是token；Hyperliquid是平台。不是HYPE不能同步，而是Hyperliquid官方candleSnapshot只保留最近5,000根。5分钟×5,000≈17.36天，三个月约需26,000根。分页不能找回已不在该接口保留范围内的数据。[官方文档](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)。

如果要Hyperliquid真实交易场所价格，近期可直接下载；更久历史需要核验过的历史归档，或持续采集积累。如果研究token长期市场价格，可选其他有足够历史的交易所，并明确现货/永续口径。

工具不自动跨平台补齐。Hyperliquid过早起点默认报错；显式allow-partial可取实际可用部分并列出缺口，不伪装成完整区间，不计算完整区间收益率。保留数量含当期未完成K线时，完整可取数量略少于5,000根。

本版Hyperliquid只支持**原生永续**，未接入需要编号映射的现货或需要dex前缀映射的HIP-3。Hyperliquid价格单位标USD，保证金机制另行区分；quote_volume未由接口提供，留null，不用成交量×收盘价冒充实际成交额。Binance两类市场以USDT计价。

## 保存及重复同步

```text
数字资产/factcheck/
  sync_prices.py
  data/raw/<来源>/<周期>/<币种>/
    <请求哈希>.json           # 原始响应，原样保留
    <请求哈希>.request.json   # URL、参数、首次下载时间
  data/normalized/<来源>/<周期>/<币种>/
    <起点毫秒>-<终点毫秒>.json
  runs/<来源>-<周期>-<区间>-<币种>.json
```

缓存键包括来源、周期、币种和区间，避免市场混用。同一请求复跑使用缓存，更改终点形成新快照。当前是可重复的区间下载工具，不是只追加最新记录的增量数据库，未配置定时任务，尚无跨快照离线合并功能。频繁更新时可进一步做按日缓存与连续归档。

统一字段：open_time_ms、open_time_utc、close_time_ms、open、high、low、close、volume、quote_volume、trades。原始价格字符串保留；整理值使用浮点数，适合研究，不用于精确订单结算。

## 核对和失败处理

- 理论根数=(end−start)/周期；列出缺失时间，不插值。
- 检查重复、时间对齐、收盘边界、正价格、有限数值、OHLC及非负成交量。
- 一个币种失败仍继续其他币种；有未接受的结果则退出码2。
- 上市前空白、历史不足、接口错误均不自动换源。
- 校验通过说明结构与区间完整，不等于用第二家交易所核验过每个价格。

## 2026-10-02验证记录

- 实际下载Binance ETH永续、Hyperliquid HYPE/ETH永续各3根5分钟K线（北京时间00:00—00:15），均连续且OHLC通过。**这不是ETH三个月数据已下载。**
- 旧HYPE/BTC三个月各26,499根，用新归一化及核对逻辑复算，收盘价逐根一致。
- 验证缺口、重复、异常OHLC、无时区日期拒绝及Hyperliquid过长请求拒绝。
- 旧HYPE脚本转为兼容入口，默认HYPE/BTC、Binance永续；已验证它能转发ETH参数及使用新缓存。旧数据留在HYPE，后续产物进入公共目录。

收益率按区间开盘至最终收盘计算，不包含资金费、手续费或杠杆。未使用相同市场和时间区间的数据，不宜直接当作精确可比的收益。
