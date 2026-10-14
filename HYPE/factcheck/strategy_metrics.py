"""pair策略绩效指标全表：基准(常驻) vs 事件规避overlay(R1固定/R2趋势确认)。

口径：日收益=日末净值差分（对数收益累加，每日再平衡隐含），rf=0，年化因子√365。
指标：收益/风险/风险调整/回撤/尾部/胜率 streak/相对BTC 八大类。
杠杆 L 不影响比率类指标（Sharpe/Sortino/胜率/beta），收益与波动类按 L=1 名义口径。
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
N_MIN, N_DAY = 525600, 365
ANN = np.sqrt(365)


def load_funding(tok):
    doc = json.loads((FUND / tok / f'{WINDOW}.json').read_bytes())
    return (np.array([e['funding_time_ms'] for e in doc['events']], dtype=np.int64),
            np.array([e['funding_rate'] for e in doc['events']]))


def build():
    t1m, cb = m.load_klines('BTC')[0], m.load_klines('BTC')[1]
    ch = m.load_klines('HYPE')[1]
    r_h = np.r_[0.0, np.log(ch[1:] / ch[:-1])]
    r_b = np.r_[0.0, np.log(cb[1:] / cb[:-1])]
    pmin = (r_h - r_b).copy()
    for t, r in zip(*load_funding('BTC')):
        pmin[min(max(t // 60000 - t1m[0] // 60000 - 1, 0), N_MIN - 1)] += r
    for t, r in zip(*load_funding('HYPE')):
        pmin[min(max(t // 60000 - t1m[0] // 60000 - 1, 0), N_MIN - 1)] -= r
    curve = np.cumsum(pmin) - (0.010 / N_MIN) * np.arange(N_MIN)
    d = curve.reshape(N_DAY, 1440)[:, -1]
    d_btc = np.cumsum(r_b).reshape(N_DAY, 1440)[:, -1]
    days = [dt.datetime.fromtimestamp(t1m[i * 1440] / 1000, dt.timezone(dt.timedelta(hours=8))) for i in range(N_DAY)]
    return d, d_btc, days


def metrics(eq, btc_eq=None):
    r = np.diff(eq)
    T = len(r)
    cum = eq[-1] - eq[0]
    vol = r.std(ddof=1) * ANN
    sharpe = r.mean() / r.std(ddof=1) * ANN
    dn = r[r < 0]
    downside = dn.std(ddof=1) * ANN if len(dn) > 1 else np.nan
    sortino = r.mean() / dn.std(ddof=1) * ANN if len(dn) > 1 else np.nan
    dd = eq - np.maximum.accumulate(eq)
    mdd = dd.min()
    calmar = cum / abs(mdd) if mdd < 0 else np.nan
    underwater = dd < 0
    longest_dd = max_run(underwater)
    pain = float(dd.mean())
    var95, var99 = np.percentile(r, [5, 1])
    cvar95 = r[r <= var95].mean()
    cvar99 = r[r <= var99].mean()
    wins, losses = r[r > 0], r[r <= 0]
    profit_factor = wins.sum() / abs(losses.sum())
    payoff = wins.mean() / abs(losses.mean())
    streak_w = max_run(r > 0)
    streak_l = max_run(r < 0)
    months = {}
    return dict(
        total_return_pct=float(cum * 100), ann_return_pct=float(cum * 100),
        ann_vol_pct=float(vol * 100), sharpe=float(sharpe), sortino=float(sortino),
        calmar=float(calmar), max_dd_pct=float(mdd * 100), longest_dd_days=int(longest_dd),
        pain_index_pct=float(pain * 100),
        var95_daily_pct=float(var95 * 100), var99_daily_pct=float(var99 * 100),
        cvar95_daily_pct=float(cvar95 * 100), cvar99_daily_pct=float(cvar99 * 100),
        skew=float(stats_skew(r)), ex_kurtosis=float(stats_kurt(r)),
        daily_win_rate=float((r > 0).mean()),
        profit_factor=float(profit_factor), payoff_ratio=float(payoff),
        expectancy_daily_pct=float(r.mean() * 100),
        best_day_pct=float(r.max() * 100), worst_day_pct=float(r.min() * 100),
        tail_ratio=float(np.percentile(r, 95) / abs(np.percentile(r, 5))),
        longest_win_streak=int(streak_w), longest_loss_streak=int(streak_l),
        omega=float(wins.sum() / abs(losses.sum())))


def max_run(mask):
    best = cur = 0
    for x in mask:
        cur = cur + 1 if x else 0
        best = max(best, cur)
    return best


def stats_skew(x):
    n = len(x)
    m2 = ((x - x.mean()) ** 2).mean()
    m3 = ((x - x.mean()) ** 3).mean()
    return m3 / m2 ** 1.5


def stats_kurt(x):
    m2 = ((x - x.mean()) ** 2).mean()
    m4 = ((x - x.mean()) ** 4).mean()
    return m4 / m2 ** 2 - 3


def main():
    d, d_btc, days = build()
    ire = next(i for i, x in enumerate(days) if x.year == 2026 and x.month == 2)
    ratio = None
    keep_r2 = np.ones(N_DAY)
    # R2: 每日可算的 HYPE/BTC 30MA 信号（与 event_overlay_sim 同口径）
    ch = m.load_klines('HYPE')[1]
    cb = m.load_klines('BTC')[1]
    r = (ch / cb).reshape(N_DAY, 1440)[:, -1]
    ma = np.convolve(r, np.ones(30) / 30, mode='valid')
    ev = next(i for i, x in enumerate(days) if (x.year, x.month) >= (2025, 12))
    for j in range(ev + 1, N_DAY):
        if j - 29 >= 0 and r[j] > ma[j - 29]:
            keep_r2[:j] = 0.0
            break
    dd = d - d[0]
    d_r1 = np.cumsum(np.diff(np.r_[0.0, dd]) * np.r_[np.zeros(ire), np.ones(N_DAY - ire)]) - 0.0015
    d_r2 = np.cumsum(np.diff(np.r_[0.0, dd]) * keep_r2) - 0.0015
    res = {}
    for name, eq in (('A基准', np.r_[0.0, d]), ('A+R1', np.r_[0.0, d_r1]), ('A+R2', np.r_[0.0, d_r2])):
        res[name] = metrics(eq)
        print('== %s ==' % name)
        for k, v in res[name].items():
            print('  %-22s %s' % (k, ('%+.2f' % v) if isinstance(v, float) else v))
    # 相对BTC
    rA = np.diff(dd)
    rb = np.diff(d_btc)
    te = (rA - rb).std(ddof=1) * ANN
    ir = (rA.mean() - rb.mean()) * 365 / te
    beta = np.cov(rA, rb, ddof=1)[0, 1] / np.var(rb, ddof=1)
    corr = np.corrcoef(rA, rb)[0, 1]
    print('== 相对BTC ==')
    print('  IR(对BTC,年化) %.2f | beta %.2f | corr %.2f | BTC全年 %+.1f%%' % (
        ir, beta, corr, (d_btc[-1] - d_btc[0]) * 100))
    res['vs_BTC'] = dict(ir=float(ir), beta=float(beta), corr=float(corr),
                         btc_ann_return_pct=float((d_btc[-1] - d_btc[0]) * 100))
    (BASE / '2026-10-13-pair绩效指标全表-结果.json').write_text(
        json.dumps(res, ensure_ascii=False, indent=2) + '\n')
    print('已写出 2026-10-13-pair绩效指标全表-结果.json')


if __name__ == '__main__':
    main()
