"""NBIS/CRWV 常驻 pair 回测（pair_lib 的首个股票用例）。

数据：data/{日期}-{nbis|crwv|qqq}-1d.csv（sync_stock_daily.py 产出；Polygon 免费档，原始保留）
口径：日线收盘、等名义多空、对数收益线性累计（非复利）、日度回等名义
成本：佣金 fee_side=2bp/边；借券费 4 档场景（0/3/5/10% 年化，按日历日间隔计提于短腿）
基准：QQQ（IR/beta/corr，日频）
输出：{运行日}-nbis-crwv-pair-结果.json
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parents[1] / '研究流程'))
import pair_lib as pl
from pair_lib import ANN_STOCK, curve_stats, metrics, relative_metrics

DATA = BASE / 'data'
FEE_SIDE = 2e-4                      # 美股佣金 2bp/边（近似，不含冲击）
BORROW_SCENARIOS = (0.0, 0.03, 0.05, 0.10)
DIRECTIONS = [('NBIS', 'CRWV'), ('CRWV', 'NBIS')]


def newest(sym):
    fs = sorted(DATA.glob(f'*-{sym}-1d.csv'))
    if not fs:
        sys.exit(f'缺少 *-{sym}-1d.csv：先运行 sync_stock_daily.py（需 Polygon 免费 key，见脚本头说明）')
    return fs[-1]


def load(sym, snapshot):
    path = DATA / f"{snapshot}-{sym.lower()}-1d.csv" if snapshot else newest(sym)
    return pl.load_stock_bars(path)


def day_reduce(r, dk):
    return np.add.reduceat(r, np.flatnonzero(np.r_[True, dk[1:] != dk[:-1], True])[:-1])


def month_labels(t_ms, day_key):
    edges = np.flatnonzero(np.r_[True, day_key[1:] != day_key[:-1], True])
    last = edges[1:] - 1
    return [f'{x.year}-{x.month:02d}' for x in
            [dt.datetime.fromtimestamp(t_ms[i] / 1000, dt.timezone.utc) for i in last]]


def month_returns(net_eq, labels):
    rets = np.diff(np.r_[0.0, net_eq])
    out = {}
    for lab, r in zip(labels, rets):
        out[lab] = out.get(lab, 0.0) + float(r)
    return {k: round(v * 100, 2) for k, v in out.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=dt.date.fromisoformat, help="固定 CSV 快照日期（YYYY-MM-DD）")
    args = parser.parse_args()
    run_date = dt.date.today().isoformat()
    t_a, c_a = load('nbis', args.snapshot)
    t_b, c_b = load('crwv', args.snapshot)
    t_q, c_q = load('qqq', args.snapshot)
    t, pa, pb = pl.align_pair(t_a, c_a, t_b, c_b)
    r_a = np.r_[0.0, np.log(pa[1:] / pa[:-1])]
    r_b = np.r_[0.0, np.log(pb[1:] / pb[:-1])]
    dk = pl.day_keys(t, 'stock')
    labels = month_labels(t, dk)

    r_q = np.r_[0.0, np.log(c_q[1:] / c_q[:-1])]
    eq_q = np.cumsum(day_reduce(r_q, pl.day_keys(t_q, 'stock')))

    d0 = dt.datetime.fromtimestamp(t[0] / 1000, dt.timezone.utc)
    d1 = dt.datetime.fromtimestamp(t[-1] / 1000, dt.timezone.utc)
    print(f'对齐后 {len(t)} bars / {len(labels)} 个交易日, {d0:%Y-%m-%d} ~ {d1:%Y-%m-%d} UTC')

    result = dict(date=run_date, source='Polygon.io 免费档(日线)',
                  granularity='1d', fee_side=FEE_SIDE, ann_factor='sqrt(252)',
                  n_days=int(len(labels)),
                  months=labels, directions={})
    for (long, short) in DIRECTIONS:
        r_long, r_short = (r_a, r_b) if long == 'NBIS' else (r_b, r_a)
        dir_res = {}
        for br in BORROW_SCENARIOS:
            ct, cr = pl.stock_borrow_events(t, dk, br)
            res = pl.standing_pair(t, r_long, r_short, dk, ct, -cr, fee_side=FEE_SIDE,
                                   carry_map='clock')
            m = metrics(res['net_eq'], ANN_STOCK)
            rel = relative_metrics(np.diff(res['net_eq']), np.diff(eq_q), ANN_STOCK)
            key = f'borrow_{br * 100:.0f}pct'
            dir_res[key] = dict(
                metrics=m, vs_QQQ=rel,
                attribution={k: round(v * 100, 2) for k, v in res['attribution'].items()},
                month_returns=month_returns(res['net_eq'], labels),
                max_dd_daily_pct=round(res['max_dd_bar'] * 100, 2))
            print('%s/%s 借券%2.0f%%: 净 %+.1f%% | 回撤(日) %.1f%% | Sharpe %.2f | 对QQQ IR %.2f beta %.2f' % (
                long, short, br * 100, m['total_return_pct'], m['max_dd_pct'],
                m['sharpe'], rel['ir'], rel['beta']))
        result['directions'][f'{long}/{short}'] = dir_res

    # 阈值再平衡（真实美元口径，复利净值）：tau 0(=每日)/2%/5%/10% × 借券 0%/5%
    TAUS = (0.0, 0.02, 0.05, 0.10)
    print('\n== 阈值再平衡（美元口径） ==')
    result['threshold'] = {}
    for (long, short) in DIRECTIONS:
        r_long, r_short = (r_a, r_b) if long == 'NBIS' else (r_b, r_a)
        rows = []
        for tau in TAUS:
            for br in (0.0, 0.05):
                d = pl.standing_pair_dollar(t, r_long, r_short, dk, tau,
                                            fee_side=FEE_SIDE, borrow_ann=br)
                m = metrics(d['equity'], ANN_STOCK)
                rows.append(dict(tau=tau, borrow=br,
                                 net_pct=round(float((d['equity'][-1] - 1) * 100), 2),
                                 max_dd_pct=round(m['max_dd_pct'], 2),
                                 sharpe=round(m['sharpe'], 2),
                                 n_rebalance=d['n_rebalance'],
                                 cost_pct=round(d['cost_total'] * 100, 2),
                                 borrow_cost_pct=round(d['borrow_total'] * 100, 2)))
                print('%s/%s tau=%3.0f%% 借券%2.0f%%: 净 %+7.1f%% | 回撤 %6.1f%% | SR %.2f | 再平衡 %3d 次 | 佣金 %.2f%%' % (
                    long, short, tau * 100, br * 100, (d['equity'][-1] - 1) * 100,
                    m['max_dd_pct'], m['sharpe'], d['n_rebalance'], d['cost_total'] * 100))
        result['threshold'][f'{long}/{short}'] = rows

    # 各腿表现：价格收益（简单口径，首末收盘）+ 对数累计 + 曲线统计
    result['legs'] = {}
    for sym, t_s, c_s in (('NBIS', t_a, c_a), ('CRWV', t_b, c_b), ('QQQ', t_q, c_q)):
        result['legs'][sym] = dict(
            price_return_pct=round(float(c_s[-1] / c_s[0] - 1) * 100, 2))
    for sym, r in (('NBIS', r_a), ('CRWV', r_b)):
        eq = np.cumsum(day_reduce(r, dk))
        result['legs'][sym]['log_sum_pct'] = round(float(eq[-1] * 100), 2)
        result['legs'][sym]['stats'] = curve_stats(eq, ANN_STOCK)
    result['legs']['QQQ']['log_sum_pct'] = round(float(eq_q[-1] * 100), 2)
    result['legs']['QQQ']['stats'] = curve_stats(eq_q, ANN_STOCK)

    # ===== 半年窗口检验（回答"高收益是否只因一年前 CRWV 大跌"）=====
    # 与 HYPE/factcheck/half_year_windows.py 同口径：日历 6 个月窗口（每月起点）
    # + 滚动 182 自然日窗口 min/中位/max。pair 取对数线性 standing（借券 0/5%），
    # 单腿取对数累计，均可与全年数字直接相减核对。
    end_idx = np.flatnonzero(np.r_[dk[1:] != dk[:-1], True])
    days = [dt.datetime.fromtimestamp(t[i] / 1000, dt.timezone.utc) for i in end_idx]
    starts = [(2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2), (2026, 3), (2026, 4)]

    t_qa, _, p_q = pl.align_pair(t_a, c_a, t_q, c_q)
    dk_q = pl.day_keys(t_qa, 'stock')
    days_q = [dt.datetime.fromtimestamp(t_qa[i] / 1000, dt.timezone.utc)
              for i in np.flatnonzero(np.r_[dk_q[1:] != dk_q[:-1], True])]
    r_qa = np.r_[0.0, np.log(p_q[1:] / p_q[:-1])]
    curves = {'NBIS': (np.cumsum(day_reduce(r_a, dk)), days),
              'CRWV': (np.cumsum(day_reduce(r_b, dk)), days),
              'QQQ': (np.cumsum(day_reduce(r_qa, dk_q)), days_q)}
    for br in (0.0, 0.05):
        ct, cr = pl.stock_borrow_events(t, dk, br)
        res = pl.standing_pair(t, r_a, r_b, dk, ct, -cr, fee_side=FEE_SIDE,
                               carry_map='clock')
        curves[f'pair_borrow_{br * 100:.0f}pct'] = (res['net_eq'][end_idx], days)

    result['half_year'] = {}
    print('\n== 半年窗口检验 ==')
    for name, (eq_d, dd) in curves.items():
        cal = pl.calendar_windows(eq_d, dd, starts, 6, ANN_STOCK)
        roll = pl.rolling_window_stats(eq_d, dd, 182, ANN_STOCK, step_days=21)
        result['half_year'][name] = dict(calendar=cal, rolling_182d=roll)
        print('[%s] 日历半年窗口:' % name)
        for w in cal:
            print('  %s: 净%+6.1f%% 回撤%6.1f%% Sharpe %5.2f 年化波动%.0f%%' % (
                w['window'], w['net_pct'], w['max_dd_pct'], w['sharpe'], w['ann_vol_pct']))
        print('  滚动182自然日: min=%+.1f%% 中位=%+.1f%% max=%+.1f%% (n=%d)' % (
            roll['min'], roll['median'], roll['max'], roll['n']))

    out = BASE / f'{run_date}-nbis-crwv-pair-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('已写出', out.name)


if __name__ == '__main__':
    main()
