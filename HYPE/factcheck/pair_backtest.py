"""pair策略净值曲线回测：把点估计变成可投资决策的数字。

在归因(2026-10-08)与资金费(2026-10-09)基础上，构建逐分钟净值曲线并输出：
累计/年化收益、最大回撤（日/分钟口径）、日夏普、胜率、成本敏感性。

组合A 常驻pair：多1份HYPE/空1份BTC（等名义，逐bar r_h−r_b），资金费时刻叠加
  rate_BTC−rate_HYPE。该口径等价于"每日再平衡回固定1:1名义"（腿的名义不变、
  盈亏线性累积），再平衡交易成本按 fee×Σ|日收益| 双边扣除。
组合B 事件驱动：BTC 5m<−0.5%（30分钟去簇）后次bar开盘进 多HYPE/空βBTC，
  持有4h，逐分钟 mark-to-market，窗口内资金费按实际发生时刻叠加，
  往返成本三档(0.1/0.2/0.3%)。

收益口径：每腿单位名义的线性累计（非复利）。杠杆/保证金不在本脚本内。
"""
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
FUND = ROOT / '数字资产' / 'factcheck' / 'data' / 'normalized' / 'binance-perp' / 'funding'
WINDOW = '1759515300000-1791051300000'
N_MIN = 525600
N_DAY = 365
FEE_SIDE = 0.0005                     # taker 5bp/边，再平衡成本近似


def load_funding(tok):
    doc = json.loads((FUND / tok / f'{WINDOW}.json').read_bytes())
    return (np.array([e['funding_time_ms'] for e in doc['events']], dtype=np.int64),
            np.array([e['funding_rate'] for e in doc['events']]))


def curve_stats(equity_daily, label):
    eq = np.asarray(equity_daily, dtype=float)
    rets = np.diff(eq)
    dd = eq - np.maximum.accumulate(eq)
    sharpe = (rets.mean() / rets.std() * np.sqrt(365)) if rets.std() > 0 else float('nan')
    return dict(label=label, total_pct=float(eq[-1] * 100),
                ann_pct=float(eq[-1] * 100),             # 窗口恰为1年
                max_dd_pct=float(dd.min() * 100),
                sharpe_daily=float(sharpe),
                up_day_share=float((rets > 0).mean()),
                worst_day_pct=float(rets.min() * 100), best_day_pct=float(rets.max() * 100))


def main():
    t1m, cb = m.load_klines('BTC')[0], m.load_klines('BTC')[1]
    ch = m.load_klines('HYPE')[1]
    r_h = np.r_[0.0, np.log(ch[1:] / ch[:-1])]          # 对齐到525600根bar（首bar收益记0）
    r_b = np.r_[0.0, np.log(cb[1:] / cb[:-1])]
    pnl = r_h - r_b                                     # 等名义常驻pair，每分钟
    beta = float(np.cov(r_b[1:], r_h[1:], ddof=1)[0, 1] / np.var(r_b[1:], ddof=1))
    t_fb, r_fbr = load_funding('BTC')
    t_fh, r_fhr = load_funding('HYPE')

    # ---- A 常驻pair ----
    # 资金费按发生分钟叠加（funding时刻取整到分钟；.001ms 偏移不影响归属）
    a_min = pnl.copy()
    for t, r in zip(t_fb, r_fbr):
        a_min[min(max(t // 60000 - t1m[0] // 60000 - 1, 0), N_MIN - 1)] += r
    for t, r in zip(t_fh, r_fhr):
        a_min[min(max(t // 60000 - t1m[0] // 60000 - 1, 0), N_MIN - 1)] -= r
    # 再平衡成本：每日回1:1名义 ≈ fee×(|r_h,d|+|r_b,d|) 双边，逐日扣除
    d_h = r_h.reshape(N_DAY, 1440).sum(1)
    d_b = r_b.reshape(N_DAY, 1440).sum(1)
    reb_cost = FEE_SIDE * (np.abs(d_h) + np.abs(d_b)).sum()
    a_daily = np.cumsum(a_min.reshape(N_DAY, 1440).sum(1))
    price_gross = float(pnl.sum() * 100)                 # 纯价格毛收益（与归因+94.2%同口径）
    a_net = a_daily - reb_cost
    standing = dict(
        price_gross_pct=price_gross,
        funding_contrib_pct=float((r_fbr.sum() - r_fhr.sum()) * 100),
        after_funding_pct=float(a_daily[-1] * 100),
        rebalance_cost_pct=float(reb_cost * 100),
        rebalance_cost_note='taker 5bp/边，按日回1:1名义',
        net_total_pct=float(a_net[-1] * 100),
        daily=curve_stats(a_daily, 'after_funding_daily'),
        net_daily=curve_stats(a_net, 'net_daily'),
        minute_max_dd_pct=float((a_min.cumsum() - np.maximum.accumulate(a_min.cumsum())).min() * 100),
        month_ends_pct=[round(float(v) * 100, 1) for v in a_net[29::30]],
        beta=beta)
    print('== A 常驻pair（等名义，逐分钟净值）==')
    print('  价格毛 %+.1f%% +资金费 %+.1f%% −再平衡成本 %.1f%% = 净 %+.1f%%/年' % (
        standing['price_gross_pct'], standing['funding_contrib_pct'],
        standing['rebalance_cost_pct'], standing['net_total_pct']))
    for tag in ('daily', 'net_daily'):
        s = standing[tag]
        print('  %s: 最大回撤(日) %.1f%% | 日夏普 %.2f | 上涨日占比 %.0f%% | 最差日 %+.1f%% 最好日 %+.1f%%' % (
            tag, s['max_dd_pct'], s['sharpe_daily'], s['up_day_share'] * 100,
            s['worst_day_pct'], s['best_day_pct']))
    print('  最大回撤(分钟口径) %.1f%%' % standing['minute_max_dd_pct'])

    # ---- B 事件驱动 ----
    b5 = cb.reshape(-1, 5)
    rb5 = np.log(b5[:, -1][1:] / b5[:, -1][:-1])
    raw = np.where(rb5 < -0.005)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 6])]
    valid = keep[keep <= len(rb5) - 2 - 200]
    entries = (valid + 2) * 5                            # 进场=事件bar次一根收盘(与归因口径一致)
    HOLD = 48                                            # 5m bar 数
    WIN = HOLD * 5                                       # 240分钟
    span = WIN * 60000
    cost_tiers = (0.001, 0.002, 0.003)
    ev = {}
    for cost in cost_tiers:
        b_min = np.zeros(N_MIN)
        per_event = []
        for e in entries:
            win = slice(e, e + WIN)
            seg_h = r_h[win].sum()
            seg_b = r_b[win].sum()
            fund = 0.0
            lo = np.searchsorted(t_fb, t1m[e]); hi = np.searchsorted(t_fb, t1m[e] + span)
            fund += beta * r_fbr[lo:hi].sum()
            lo2 = np.searchsorted(t_fh, t1m[e]); hi2 = np.searchsorted(t_fh, t1m[e] + span)
            fund -= r_fhr[lo2:hi2].sum()
            b_min[win] += r_h[win] - beta * r_b[win]
            for t, r in zip(t_fb[lo:hi], r_fbr[lo:hi]):
                b_min[min(t // 60000 - t1m[0] // 60000 - 1, N_MIN - 1)] += beta * r
            for t, r in zip(t_fh[lo2:hi2], r_fhr[lo2:hi2]):
                b_min[min(t // 60000 - t1m[0] // 60000 - 1, N_MIN - 1)] -= r
            p = seg_h - beta * seg_b + fund - cost
            per_event.append(p)
            b_min[e] -= cost                               # 成本计在进场分钟
        pe = np.array(per_event)
        b_daily = np.cumsum(b_min.reshape(N_DAY, 1440).sum(1))
        k = f'rt_{cost * 100:.1f}pct'
        ev[k] = dict(
            net_total_pct=float(pe.sum() * 100),
            ann_pct=float(pe.sum() * 100),                 # 窗口恰为1年
            per_event_mean_pct=float(pe.mean() * 100),
            per_event_median_pct=float(np.median(pe) * 100),
            win_rate=float((pe > 0).mean()),
            n_events=int(len(pe)),
            exposure_frac=float(len(pe) * WIN / N_MIN),
            daily=curve_stats(b_daily, k))
        print('== B 事件驱动 %s（beta=%.2f对冲, 4h, n=%d）==' % (k, beta, len(pe)))
        print('  净合计 %+.1f%%/年 | 每事件 均%+.3f%% 中位%+.3f%% 胜率%.0f%% | 敞口占比 %.0f%%' % (
            ev[k]['net_total_pct'], ev[k]['per_event_mean_pct'], ev[k]['per_event_median_pct'],
            ev[k]['win_rate'] * 100, ev[k]['exposure_frac'] * 100))
        s = ev[k]['daily']
        print('  最大回撤(日) %.1f%% | 日夏普 %.2f | 最差日 %+.1f%%' % (
            s['max_dd_pct'], s['sharpe_daily'], s['worst_day_pct']))

    result = dict(date='2026-10-09', window='2025-10-04~2026-10-04 北京',
                  fee_side=FEE_SIDE, beta=beta, n_events=int(len(valid)),
                  standing=standing, event_driven=ev,
                  convention='每腿单位名义线性累计（非复利）；A含资金费与再平衡成本，B含窗口资金费与往返成本')
    out = BASE / '2026-10-09-pair净值回测-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('已写出', out.name)


if __name__ == '__main__':
    main()
