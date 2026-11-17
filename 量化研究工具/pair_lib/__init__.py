"""通用 pair 回测库：从 HYPE/BTC 研究抽象而来，适用于任意两个等名义多空标的。

数据层 data.py   ：crypto 分钟线（币安标准化 JSON）/ 股票 1h 线（Polygon CSV）→ 统一 (t_ms, close)
引擎层 engine.py ：standing_pair 常驻等名义 pair，carry（资金费/借券费）事件叠加 + 日度聚合
指标层 metrics.py：绩效指标全表、滚动/日历窗口、相对基准 IR/beta/corr

正确性基准：regress_hype_btc.py 用本库重跑 HYPE/BTC 必须与 2026-10-09 归档结果一致（<0.1pp）。
"""
from .data import (load_crypto_minutes, load_stock_bars, align_pair, day_keys,
                   crypto_funding_events, stock_borrow_events)
from .engine import standing_pair, standing_pair_dollar
from .metrics import (ANN_CRYPTO, ANN_STOCK, metrics, curve_stats, max_run, rolling_window_stats,
                      calendar_windows, relative_metrics)

__all__ = ['load_crypto_minutes', 'load_stock_bars', 'align_pair', 'day_keys',
           'crypto_funding_events', 'stock_borrow_events', 'standing_pair',
           'standing_pair_dollar',
           'ANN_CRYPTO', 'ANN_STOCK',
           'metrics', 'curve_stats', 'max_run', 'rolling_window_stats',
           'calendar_windows', 'relative_metrics']
