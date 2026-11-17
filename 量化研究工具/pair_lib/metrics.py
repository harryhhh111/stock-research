"""pair 回测指标层：绩效指标全表、曲线统计、滚动/日历窗口、相对基准。

从 HYPE/factcheck/strategy_metrics.py 与 half_year_windows.py 抽象：
- ann_factor 参数化（crypto 用 √365，股票用 √252）
- metrics(eq, ann_factor)：收益/风险/风险调整/回撤/尾部/胜率 streak 全表
- curve_stats(eq, ann_factor)：旧脚本口径的紧凑统计
- relative_metrics(r_p, r_b, ann_factor)：对基准的 IR/beta/corr
- rolling_window_stats / calendar_windows：任意日度序列的滚动窗口与日历月窗口
"""
import numpy as np

ANN_CRYPTO = np.sqrt(365.0)
ANN_STOCK = np.sqrt(252.0)


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


def curve_stats(eq, ann_factor=ANN_CRYPTO, label=''):
    eq = np.asarray(eq, dtype=float)
    rets = np.diff(eq)
    dd = eq - np.maximum.accumulate(eq)
    sharpe = (rets.mean() / rets.std() * ann_factor) if rets.std() > 0 else float('nan')
    return dict(label=label, total_pct=float(eq[-1] * 100),
                max_dd_pct=float(dd.min() * 100),
                sharpe_daily=float(sharpe),
                up_day_share=float((rets > 0).mean()),
                worst_day_pct=float(rets.min() * 100),
                best_day_pct=float(rets.max() * 100))


def metrics(eq, ann_factor=ANN_CRYPTO):
    eq = np.asarray(eq, dtype=float)
    r = np.diff(eq)
    cum = eq[-1] - eq[0]
    vol = r.std(ddof=1) * ann_factor
    sharpe = r.mean() / r.std(ddof=1) * ann_factor if r.std(ddof=1) > 0 else np.nan
    dn = r[r < 0]
    sortino = r.mean() / dn.std(ddof=1) * ann_factor if len(dn) > 1 and dn.std(ddof=1) > 0 else np.nan
    dd = eq - np.maximum.accumulate(eq)
    mdd = dd.min()
    calmar = cum / abs(mdd) if mdd < 0 else np.nan
    var95, var99 = np.percentile(r, [5, 1])
    wins, losses = r[r > 0], r[r <= 0]
    return dict(
        total_return_pct=float(cum * 100), ann_vol_pct=float(vol * 100),
        sharpe=float(sharpe), sortino=float(sortino),
        calmar=float(calmar), max_dd_pct=float(mdd * 100),
        longest_dd_days=int(max_run(dd < 0)),
        pain_index_pct=float(dd.mean() * 100),
        var95_daily_pct=float(var95 * 100), var99_daily_pct=float(var99 * 100),
        cvar95_daily_pct=float(r[r <= var95].mean() * 100),
        cvar99_daily_pct=float(r[r <= var99].mean() * 100),
        skew=float(stats_skew(r)), ex_kurtosis=float(stats_kurt(r)),
        daily_win_rate=float((r > 0).mean()),
        profit_factor=float(wins.sum() / abs(losses.sum())) if losses.sum() != 0 else np.nan,
        payoff_ratio=float(wins.mean() / abs(losses.mean())) if len(wins) and len(losses) else np.nan,
        expectancy_daily_pct=float(r.mean() * 100),
        best_day_pct=float(r.max() * 100), worst_day_pct=float(r.min() * 100),
        tail_ratio=float(np.percentile(r, 95) / abs(np.percentile(r, 5))),
        longest_win_streak=int(max_run(r > 0)), longest_loss_streak=int(max_run(r < 0)))


def relative_metrics(r_p, r_b, ann_factor=ANN_CRYPTO):
    r_p, r_b = np.asarray(r_p, float), np.asarray(r_b, float)
    te = (r_p - r_b).std(ddof=1) * ann_factor
    ir = (r_p.mean() - r_b.mean()) * (ann_factor ** 2) / te if te > 0 else np.nan
    beta = np.cov(r_p, r_b, ddof=1)[0, 1] / np.var(r_b, ddof=1)
    corr = np.corrcoef(r_p, r_b)[0, 1]
    return dict(ir=float(ir), beta=float(beta), corr=float(corr))


def _window_stats(d, i0, i1, ann_factor, L=1.0):
    seg = L * (d[i1] - d[i0])
    eq = L * (d[i0:i1 + 1] - d[i0])
    dd = (eq - np.maximum.accumulate(eq)).min()
    rets = L * np.diff(d[i0:i1 + 1])
    sharpe = float(rets.mean() / rets.std() * ann_factor) if rets.std() > 0 else float('nan')
    ann_vol = float(rets.std() * ann_factor * 100)
    return dict(net_pct=float(seg * 100), max_dd_pct=float(dd * 100),
                sharpe=float(sharpe), ann_vol_pct=ann_vol)


def rolling_window_stats(eq, days, width_days, ann_factor, step_days=30):
    """滚动窗口净收益 min/中位/max。days 为与 eq 对齐的日期序列（datetime）。"""
    eq = np.asarray(eq, float)
    span = (days[-1] - days[0]).days
    rows = []
    for start in range(0, max(span - width_days, 0) + 1, step_days):
        d0 = days[0] + dt_timedelta(days=start)
        d1 = d0 + dt_timedelta(days=width_days)
        i0 = int(np.searchsorted([d.toordinal() for d in days], d0.toordinal()))
        i1 = min(int(np.searchsorted([d.toordinal() for d in days], d1.toordinal())), len(eq) - 1)
        if i1 > i0:
            rows.append(_window_stats(eq, i0, i1, ann_factor)['net_pct'])
    if not rows:
        return dict(min=None, median=None, max=None, n=0)
    return dict(min=float(min(rows)), median=float(np.median(rows)),
                max=float(max(rows)), n=len(rows))


def calendar_windows(eq, days, start_yms, n_months, ann_factor):
    """日历窗口：从每个 (y,m) 起 n 个月。days 与 eq 对齐（len(days)==len(eq)）。"""
    eq = np.asarray(eq, float)
    out = []
    for (y, mo) in start_yms:
        i0 = next((i for i, d in enumerate(days) if d.year == y and d.month == mo), None)
        if i0 is None:
            continue
        end_y = y + (mo + n_months - 1) // 12
        end_m = (mo + n_months - 1) % 12 + 1
        i1 = next((i for i, d in enumerate(days)
                   if (d.year, d.month) >= (end_y, end_m)), len(eq) - 1)
        if i1 <= i0:
            continue
        w = _window_stats(eq, i0, min(i1, len(eq) - 1), ann_factor)
        w['window'] = f'{y}-{mo:02d} ~ {days[min(i1, len(eq)-1)].year}-{days[min(i1, len(eq)-1)].month:02d}'
        out.append(w)
    return out


def dt_timedelta(**kw):
    import datetime as dt
    return dt.timedelta(**kw)
