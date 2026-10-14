"""常驻pair前期回撤归因：为什么前4个月浮亏、第4个月末才回本。

pair每日盈亏 = r_HYPE − r_BTC（等名义），净值=累计和 ⇒ 净值曲线≈HYPE/BTC汇率的
对数走势。前期回撤=HYPE/BTC比值下跌。本脚本回答：这段下跌是 (a) BTC涨HYPE不涨
 (b) HYPE独立下跌 (c) 同跌但HYPE跌更多 中的哪一种，以及回本拐点的驱动。

输出：逐月三列收益（BTC/HYPE/pair）、比值最大回撤区间、滚动30日beta、
前期亏损日内分解（最差10天 BTC腿/HYPE腿各贡献多少）。
"""
import datetime as dt
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m

BASE = Path(__file__).resolve().parent
N_DAY = 365


def iso_bj(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone(dt.timedelta(hours=8))).strftime('%Y-%m-%d')


def main():
    t1m, cb = m.load_klines('BTC')[0], m.load_klines('BTC')[1]
    ch = m.load_klines('HYPE')[1]
    r_h = np.r_[0.0, np.log(ch[1:] / ch[:-1])].reshape(N_DAY, 1440).sum(1)
    r_b = np.r_[0.0, np.log(cb[1:] / cb[:-1])].reshape(N_DAY, 1440).sum(1)
    pnl = r_h - r_b
    eq = np.cumsum(pnl)
    days = [iso_bj(t1m[i * 1440]) for i in range(N_DAY)]

    print('== 逐月分解（自然月，%) ==')
    print('%8s %8s %8s %8s %8s' % ('月份', 'BTC', 'HYPE', 'pair', 'HYPE/BTC'))
    cur = None
    acc = np.zeros(3)
    monthly = []
    for i, d in enumerate(days):
        mon = d[:7]
        if cur is None:
            cur = mon
        if mon != cur:
            ratio = (cb[(i) * 1440 - 1] / cb[0]) / (ch[i * 1440 - 1] / ch[0])
            monthly.append((cur, *acc * 100))
            print('%8s %8.1f %8.1f %8.1f' % (cur, acc[1] * 100, acc[0] * 100, acc[2] * 100))
            cur, acc = mon, np.zeros(3)
        acc += [r_h[i], r_b[i], pnl[i]]
    print('%8s %8.1f %8.1f %8.1f' % (cur, acc[1] * 100, acc[0] * 100, acc[2] * 100))

    trough = int(np.argmin(eq))
    peak_i = int(np.argmax(eq[:trough + 1])) if trough > 0 else 0
    print('\n== 回撤区间 ==')
    print('净值最低日: %s (day %d) 累计 %+0.1f%%' % (days[trough], trough, eq[trough] * 100))
    print('前高日: %s 累计 %+0.1f%%' % (days[peak_i], eq[peak_i] * 100))
    print('回本日(净值重新>0): %s' % next((days[i] for i in range(N_DAY) if eq[i] > 0 and i > trough), '未回本'))

    seg_h = r_h[:trough + 1].sum() * 100
    seg_b = r_b[:trough + 1].sum() * 100
    print('\n== 前 %d 天亏损分解: pair %+0.1f%% = HYPE腿 %+0.1f%% − BTC腿 %+0.1f%% ==' % (
        trough + 1, eq[trough] * 100, seg_h, seg_b))
    print('同期 BTC 价格 %+.1f%%, HYPE 价格 %+.1f%%' % (seg_b, seg_h))

    print('\n== 前期(pair净值<0期间)最差10天 ==')
    neg = [(i, pnl[i]) for i in range(trough + 1)]
    neg.sort(key=lambda x: x[1])
    print('%11s %8s %8s %8s' % ('日期', 'pair%', 'HYPE%', 'BTC%'))
    for i, p in neg[:10]:
        print('%11s %+8.2f %+8.2f %+8.2f' % (days[i], p * 100, r_h[i] * 100, r_b[i] * 100))

    print('\n== 滚动30日beta与corr（日收益, 月末取样） ==')
    for i in range(29, trough + 1, 15):
        bh, bb = r_b[i - 29:i + 1], r_h[i - 29:i + 1]
        beta = np.cov(bb, bh, ddof=1)[0, 1] / np.var(bh, ddof=1)
        corr = np.corrcoef(bb, bh)[0, 1]
        print('%s beta=%5.2f corr=%5.2f' % (days[i], beta, corr))

    ratio = (ch / cb)
    r_eq = ratio / ratio[0]
    print('\n== HYPE/BTC 比值: 年末(%s) %+.1f%% | 全年 %+.1f%% | 最低点 %s %+.1f%% ==' % (
        days[87], (r_eq[88] - 1) * 100, (r_eq[-1] - 1) * 100,
        days[int(np.argmin(r_eq[:200]))], (r_eq[:200].min() - 1) * 100))
    out = dict(date='2026-10-10', trough_day=days[trough], trough_pct=float(eq[trough] * 100),
               breakeven_day=next((days[i] for i in range(N_DAY) if eq[i] > 0 and i > trough), None),
               seg_hype_pct=float(seg_h), seg_btc_pct=float(seg_b))
    (BASE / '2026-10-10-pair前期回撤归因-结果.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
