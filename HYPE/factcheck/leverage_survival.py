"""常驻pair杠杆生存线：不同每腿名义杠杆下，全年分钟级净值能否活下来。

口径：权益E0=1，每腿名义=L×E0（多HYPE/空BTC），分钟权益 = 1 + L×curve(t)。
curve=逐分钟(r_h−r_b)+资金费，再平衡成本按1.0%/年线性日扣。
维持保证金按总名义的 mm_total 近似（Binance USDT-M：BTC约0.4%、HYPE档位更高，
跨仓合并取保守值1.5%）；强平近似判据：1 + L×curve − mm_total×2L ≤ 0。
输出：每档L的期末权益收益、权益最大回撤、最低权益、是否触发强平。
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
MM_TOTAL = 0.015                    # 维持保证金/总名义(两腿合计)，保守取值


def load_funding(tok):
    doc = json.loads((FUND / tok / f'{WINDOW}.json').read_bytes())
    return (np.array([e['funding_time_ms'] for e in doc['events']], dtype=np.int64),
            np.array([e['funding_rate'] for e in doc['events']]))


def main():
    t1m, cb = m.load_klines('BTC')[0], m.load_klines('BTC')[1]
    ch = m.load_klines('HYPE')[1]
    r_h = np.r_[0.0, np.log(ch[1:] / ch[:-1])]
    r_b = np.r_[0.0, np.log(cb[1:] / cb[:-1])]
    curve = (r_h - r_b).copy()
    t_fb, r_fb = load_funding('BTC')
    t_fh, r_fh = load_funding('HYPE')
    for t, r in zip(t_fb, r_fb):
        curve[min(max(t // 60000 - t1m[0] // 60000 - 1, 0), N_MIN - 1)] += r
    for t, r in zip(t_fh, r_fh):
        curve[min(max(t // 60000 - t1m[0] // 60000 - 1, 0), N_MIN - 1)] -= r
    curve = np.cumsum(curve)
    reb = 0.010 / N_DAY / 1440                                  # 1%/年线性日扣
    curve = curve - reb * np.arange(N_MIN)
    worst = float(curve.min())
    print('curve: 期末 %+0.1f%% | 最低点 %+.1f%% | 最大回撤(分钟) %.1f%%' % (
        curve[-1] * 100, worst * 100,
        (curve - np.maximum.accumulate(curve)).min() * 100))
    print('每腿名义杠杆 L | 期末权益 | 权益最大回撤 | 最低权益 | 强平?')
    rows = []
    for L in (0.3, 0.5, 0.7, 1.0, 1.2, 1.4, 2.0):
        eq = 1 + L * curve
        liq_level = -(1 - MM_TOTAL * 2 * L) / L                 # 触发强平的curve值
        liq = bool(eq.min() - MM_TOTAL * 2 * L <= 0)
        dd = (eq - np.maximum.accumulate(eq)).min()
        rows.append(dict(leverage_per_leg=L, end_eq=float(eq[-1]),
                         end_return_pct=float((eq[-1] - 1) * 100),
                         max_dd_pct=float(dd * 100),
                         min_eq_pct=float((eq.min() - 1) * 100),
                         liquidation=liq))
        print('  L=%.1f | %+.0f%% | %+.0f%% | %+0.0f%% | %s' % (
            L, (eq[-1] - 1) * 100, dd * 100, (eq.min() - 1) * 100,
            '强平' if liq else '存活'))
    # 不触发强平的最大L（解析）：curve.min = worst → L×worst = -(1-2mm L) → L = -1/(worst-2mm)
    L_star = -1.0 / (worst - 2 * MM_TOTAL)
    print('按今年最低点解析生存上限: L = %.2f（每腿名义/权益）' % L_star)
    result = dict(date='2026-10-10', mm_total=MM_TOTAL, curve_worst_pct=worst * 100,
                  curve_end_pct=float(curve[-1] * 100), L_star=float(L_star), rows=rows)
    out = BASE / '2026-10-10-pair杠杆生存线-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('已写出', out.name)


if __name__ == '__main__':
    main()
