"""半年窗口检验：常驻pair在任意连续6个月的表现，回答"半年回测预期收益"。

构造同 pair_backtest（资金费在分钟层、再平衡成本线性），输出：
1) 7个日历半年窗口的净收益与窗口内最大回撤（L=1名义 与 L=0.7实际）；
2) 滚动182天窗口的 min/中位/max；
3) Oct-Mar 窗口叠加事件规避 overlay（2026-02-01 回场）的对照。
结论指向：半年样本无法定义"预期收益"，regime 依赖极强。
"""
import datetime as dt
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
FUND = ROOT / '数字资产' / 'factcheck' / 'data' / 'normalized' / 'binance-perp' / 'funding'
WINDOW = '1759515300000-1791051300000'
N_MIN, N_DAY = 365 * 1440, 365


def load_funding(tok):
    doc = json.loads((FUND / tok / f'{WINDOW}.json').read_bytes())
    return (np.array([e['funding_time_ms'] for e in doc['events']], dtype=np.int64),
            np.array([e['funding_rate'] for e in doc['events']]))


def build_daily():
    t1m, cb = m.load_klines('BTC')[0], m.load_klines('BTC')[1]
    ch = m.load_klines('HYPE')[1]
    r_h = np.r_[0.0, np.log(ch[1:] / ch[:-1])]
    r_b = np.r_[0.0, np.log(cb[1:] / cb[:-1])]
    pmin = (r_h - r_b).copy()
    t_fb, r_fb = load_funding('BTC')
    t_fh, r_fh = load_funding('HYPE')
    for t, r in zip(t_fb, r_fb):
        pmin[min(max(t // 60000 - t1m[0] // 60000 - 1, 0), N_MIN - 1)] += r
    for t, r in zip(t_fh, r_fh):
        pmin[min(max(t // 60000 - t1m[0] // 60000 - 1, 0), N_MIN - 1)] -= r
    curve = np.cumsum(pmin) - (0.010 / N_MIN) * np.arange(N_MIN)
    d = curve.reshape(N_DAY, 1440)[:, -1]
    days = [dt.datetime.fromtimestamp(t1m[i * 1440] / 1000, dt.timezone(dt.timedelta(hours=8))) for i in range(N_DAY)]
    return d, days


def window_stats(d, i0, i1, L=1.0):
    seg = L * (d[i1] - d[i0])
    eq = L * (d[i0:i1 + 1] - d[i0])
    dd = (eq - np.maximum.accumulate(eq)).min()
    rets = L * np.diff(d[i0:i1 + 1])
    sharpe = float(rets.mean() / rets.std() * np.sqrt(365)) if rets.std() > 0 else float('nan')
    ann_vol = float(rets.std() * np.sqrt(365) * 100)
    return seg * 100, dd * 100, sharpe, ann_vol


def main():
    d, days = build_daily()
    print('全年: 净%+0.1f%%' % (d[-1] * 100))
    print('\n== 日历半年窗口（净收益% / 窗口内最大回撤%，L=1名义 | L=0.7实际） ==')
    starts = [(2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2), (2026, 3), (2026, 4)]
    rows = []
    for (y, mo) in starts:
        i0 = next(i for i, x in enumerate(days) if x.year == y and x.month == mo)
        end = dt.datetime(y + (mo + 5 > 12), (mo + 5 - 1) % 12 + 1, 1, tzinfo=days[0].tzinfo)
        i1 = min(next((i for i, x in enumerate(days) if x >= end), N_DAY - 1), N_DAY - 1)
        r1, dd1, sr1, vol1 = window_stats(d, i0, i1, 1.0)
        r07, dd07, sr07, _ = window_stats(d, i0, i1, 0.7)
        label = '%d-%02d ~ %d-%02d' % (y, mo, days[i1].year, days[i1].month)
        rows.append(dict(window=label, net_L1=float(r1), dd_L1=float(dd1), sharpe=float(sr1),
                         ann_vol_pct=float(vol1),
                         net_L07=float(r07), dd_L07=float(dd07), sharpe_L07=float(sr07)))
        print('  %s: 净%+6.1f%% 回撤%6.1f%% Sharpe(日,年化)%.2f 年化波动%.0f%% | L=0.7: %+6.1f / %6.1f / SR %.2f' % (
            label, r1, dd1, sr1, vol1, r07, dd07, sr07))
    r182 = [window_stats(d, i, min(i + 182, N_DAY - 1))[0] for i in range(0, N_DAY - 182, 30)]
    print('\n滚动182天净收益(L=1): min=%+.1f%% 中位=%+.1f%% max=%+.1f%%' % (
        min(r182), float(np.median(r182)), max(r182)))
    # Oct-Mar 叠加 overlay：空仓至 2026-02-01 再进（复用 event_overlay_sim 口径）
    i0 = 0
    i1 = next(i for i, x in enumerate(days) if x.year == 2026 and x.month == 4) - 1
    ire = next(i for i, x in enumerate(days) if x.year == 2026 and x.month == 2)
    keep = np.ones(N_DAY)
    keep[:ire] = 0.0
    dd = d - d[0]
    ov = np.cumsum(np.diff(np.r_[0.0, dd]) * keep) - 0.0015
    print('Oct~Mar +overlay(2/1回场, L=1): 净%+0.1f%% 窗口内回撤%0.1f%%' % (
        (ov[i1] - ov[i0]) * 100, (ov[i1] - ov[i0]) * 100 - 0))  # 回撤另算
    eq = ov[i0:i1 + 1]
    print('  其中窗口内最大回撤: %0.1f%%' % (eq - np.maximum.accumulate(eq)).min() * -1 * np.sign(1))
    result = dict(date='2026-10-13', rows=rows,
                  roll182=dict(min=float(min(r182)), median=float(np.median(r182)), max=float(max(r182))))
    (BASE / '2026-10-13-半年窗口检验-结果.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('已写出 2026-10-13-半年窗口检验-结果.json')


if __name__ == '__main__':
    main()
