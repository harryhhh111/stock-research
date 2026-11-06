"""pair 回测数据层：统一 crypto 分钟线与股票 1h 线的加载、对齐与分日。

所有 loader 返回 (t_ms:int64[], close:float[])，升序、等标的各自完整。
align_pair 按时间戳 inner join 对齐两腿（停牌/假日差异直接丢掉不对齐的 bar）。
day_keys 把 bar 序列映射为分日标签（相邻两天标签必不同，同一天内标签恒定）：
- kind='crypto'：连续 7×24 分钟线 → 自首个 bar 的整天数（与旧脚本 reshape(N,1440) 分块等价）
- kind='stock'  ：交易时段 1h 线 → 日内 bar 间隔 ≤1h、隔夜/周末 >4h，按 >4h 断点分桶（免时区处理）

carry 事件流：
- crypto_funding_events：币安永续资金费 JSON → 多腿收 +rate、空腿付 −rate，调用方合成差额
- stock_borrow_events  ：借券费按日历日精确计提（相邻交易日间隔含周末），rate=短腿年化借券费
"""
import importlib.util
import json
import csv
import datetime as dt
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]                     # 研究流程/pair_lib → 工作区根目录

_hype_mod = None


def _leadlag():
    """惰性加载 HYPE/factcheck/leadlag_btc_hype_1s.py（该模块含币安数据路径常量）。"""
    global _hype_mod
    if _hype_mod is None:
        p = ROOT / 'HYPE' / 'factcheck' / 'leadlag_btc_hype_1s.py'
        spec = importlib.util.spec_from_file_location('leadlag_btc_hype_1s', p)
        _hype_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_hype_mod)
    return _hype_mod


def load_crypto_minutes(tok):
    t, c, _ = _leadlag().load_klines(tok)
    return np.asarray(t, dtype=np.int64), np.asarray(c, dtype=float)


def crypto_funding_events(tok):
    """币安永续资金费 → (t_ms, rate)。rate 语义：多腿每单位名义收到的金额。"""
    fund = ROOT / '数字资产' / 'factcheck' / 'data' / 'normalized' / 'binance-perp' / 'funding'
    doc = json.loads((fund / tok / '1759515300000-1791051300000.json').read_bytes())
    return (np.array([e['funding_time_ms'] for e in doc['events']], dtype=np.int64),
            np.array([e['funding_rate'] for e in doc['events']], dtype=float))


def load_stock_bars(csv_path):
    """Polygon CSV（日线或 1h，列须含 t_ms/close）→ (t_ms, close)。"""
    t, c = [], []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            if not row.get('t_ms'):
                continue
            t.append(int(row['t_ms']))
            c.append(float(row['close']))
    return np.array(t, dtype=np.int64), np.array(c, dtype=float)


def align_pair(ta, pa, tb, pb):
    """按时间戳 inner join。"""
    ib = np.flatnonzero(np.isin(tb, ta))
    ia = np.flatnonzero(np.isin(ta, tb[ib]))
    order = np.argsort(ta[ia])
    return ta[ia][order], pa[ia][order], pb[ib][order]


def day_keys(t_ms, kind):
    if kind == 'crypto':
        return (t_ms - t_ms[0]) // 86_400_000
    if kind == 'stock':
        gap = np.empty(len(t_ms), dtype=bool)
        gap[0] = True
        gap[1:] = (t_ms[1:] - t_ms[:-1]) > 4 * 3600_000
        return np.cumsum(gap) - 1
    raise ValueError(kind)


def stock_borrow_events(t_ms, day_key, borrow_ann):
    """借券费事件：每个交易日桶按其最后bar到上一桶最后bar的实际日历间隔计提。

    rate = borrow_ann × gap_days / 365，记在该交易日最后一根 bar。
    首日不计（视作建仓日）。borrow_ann=0 时返回空事件。
    """
    if borrow_ann <= 0:
        return np.array([], dtype=np.int64), np.array([], dtype=float)
    edges = np.flatnonzero(np.r_[True, day_key[1:] != day_key[:-1], True])
    last_idx = edges[1:] - 1                                    # 每个交易日桶的最后bar下标
    times = t_ms[last_idx]
    gaps = np.empty(len(times), dtype=float)
    gaps[0] = 0.0
    gaps[1:] = (times[1:] - times[:-1]) / 86_400_000.0
    rates = borrow_ann * gaps / 365.0
    keep = gaps > 0
    return times[keep], rates[keep]
