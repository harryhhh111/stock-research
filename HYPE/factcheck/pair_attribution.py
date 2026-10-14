"""pair盈亏归因：空BTC+多HYPE，"涨跌不对称"到底贡献了多少。

用户逻辑：HYPE上涨跟随比(1.20)>下跌跟随比(1.16) → 常驻pair(空BTC多HYPE)在涨跌中
不对称受益。本脚本做两件事：
1. 常驻pair全年盈亏归因：总盈亏 = 涨时贡献 + 跌时贡献 + 横盘贡献（全部按 1分钟bar、
   等名义口径逐bar加总）。涨/跌贡献即为"不对称收割"部分，剩余为趋势(ε)。
2. 事件驱动版：BTC 5m<-0.5% 事件后开 pair（多HYPE空BTC，beta对冲版与等名义版），
   持有4小时，报均值/中位/胜率/bootstrap CI；并按三档往返成本(0.1%/0.2%/0.3%)估净期望。

数据：全年1分钟K线（HYPE/BTC）。纯描述。
"""
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m

BASE = Path(__file__).resolve().parent
REPS = 20000
RNG = np.random.default_rng(20261008)


def load_k(tok):
    p = m.K1M / tok / '1759515300000-1791051300000.json'
    doc = json.loads(p.read_bytes())
    return np.array([c['close'] for c in doc['candles']])


def block_boot(rows, block_ids, reps=REPS):
    uniq = np.unique(block_ids)
    loc = {b: np.where(block_ids == b)[0] for b in uniq}
    sums = np.array([rows[loc[b]].sum(axis=0) for b in uniq])
    cnts = np.array([len(loc[b]) for b in uniq], dtype=float)
    draws = RNG.integers(0, len(uniq), size=(reps, len(uniq)))
    out = np.empty((reps, rows.shape[1]))
    for r in range(reps):
        w = np.bincount(draws[r], minlength=len(uniq)).astype(float)
        out[r] = (w @ sums) / (w @ cnts)
    return out


def ci(boot, center):
    center = np.atleast_1d(np.asarray(center, dtype=float))
    boot = np.asarray(boot, dtype=float)
    if boot.ndim == 1:
        lo, hi = np.percentile(boot, [2.5, 97.5])
        return dict(estimate=[float(x) for x in center], ci95_lo=[float(lo)], ci95_hi=[float(hi)])
    lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
    return dict(estimate=[float(x) for x in center],
                ci95_lo=[float(x) for x in lo], ci95_hi=[float(x) for x in hi])


def main():
    ch, cb = load_k('HYPE'), load_k('BTC')
    r_h = np.log(ch[1:] / ch[:-1])
    r_b = np.log(cb[1:] / cb[:-1])
    pnl = r_h - r_b                                   # 等名义 pair 每bar盈亏
    total = float(pnl.sum())
    up = r_b > 0
    dn = r_b < 0
    fl = ~(up | dn)
    contrib = dict(
        total_pct=total * 100,
        up_contrib_pct=float(pnl[up].sum()) * 100,
        down_contrib_pct=float(pnl[dn].sum()) * 100,
        flat_contrib_pct=float(pnl[fl].sum()) * 100,
        n_bars=int(len(pnl)), n_up=int(up.sum()), n_down=int(dn.sum()), n_flat=int(fl.sum()),
        pnl_up_bar_mean_pct=float(pnl[up].mean()) * 100,
        pnl_down_bar_mean_pct=float(pnl[dn].mean()) * 100,
        btc_up_move_total_pct=float(r_b[up].sum()) * 100,
        btc_down_move_total_pct=float(r_b[dn].sum()) * 100)
    # 事件/非事件分解：用户看中的 1.16/1.08 不对称发生在极端事件分钟
    evu = r_b > 0.0025
    evd = r_b < -0.0025
    contrib['event_split'] = dict(
        up_event=dict(n=int(evu.sum()), ratio=float(r_h[evu].sum() / r_b[evu].sum()),
                      pair_contrib_pct=float(pnl[evu].sum()) * 100,
                      btc_move_sum_pct=float(r_b[evu].sum()) * 100),
        down_event=dict(n=int(evd.sum()), ratio=float(r_h[evd].sum() / r_b[evd].sum()),
                        pair_contrib_pct=float(pnl[evd].sum()) * 100,
                        btc_move_sum_pct=float(r_b[evd].sum()) * 100),
        nonevent_up_ratio=float(r_h[up & ~evu].sum() / r_b[up & ~evu].sum()),
        nonevent_down_ratio=float(r_h[dn & ~evd].sum() / r_b[dn & ~evd].sum()),
        nonevent_net_pct=float((pnl[up & ~evu].sum() + pnl[dn & ~evd].sum()) * 100),
        event_net_pct=float((pnl[evu].sum() + pnl[evd].sum()) * 100))
    # 事件驱动版
    beta = float(np.cov(r_b, r_h, ddof=1)[0, 1] / np.var(r_b, ddof=1))
    b5 = cb.reshape(-1, 5)
    rb5 = np.log(b5[:, -1][1:] / b5[:, -1][:-1])
    raw = np.where(rb5 < -0.005)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 6])]
    valid = keep[keep <= len(rb5) - 2 - 200]
    HOLD_SET = (3, 12, 48)                               # 15分钟/1小时/4小时
    h5 = ch.reshape(-1, 5)
    rh5 = np.log(h5[:, -1][1:] / h5[:, -1][:-1])         # 与rb5同口径：5分钟收盘价对齐
    fwd_rows = {}
    for HOLD in HOLD_SET:
        f_h = np.array([rh5[v + 1:v + 1 + HOLD].sum() for v in valid])
        f_b = np.array([rb5[v + 1:v + 1 + HOLD].sum() for v in valid])
        p_eq = f_h - f_b
        p_bh = f_h - beta * f_b                            # 因子中性: 多1份HYPE 空β份BTC
        fwd_rows[HOLD] = dict(f_h=f_h, f_b=f_b, p_eq=p_eq, p_bh=p_bh)
    HOLD = 48
    p_eq, p_bh = fwd_rows[HOLD]['p_eq'], fwd_rows[HOLD]['p_bh']
    boots = block_boot(np.column_stack([p_eq, p_bh]), valid // 288)
    ev = dict(events=int(len(valid)), hold_h=HOLD // 12, beta=beta,
              by_horizon={str(k): dict(
                  equal_mean=float(v['p_eq'].mean()), equal_median=float(np.median(v['p_eq'])),
                  equal_win=float((v['p_eq'] > 0).mean()),
                  beta_mean=float(v['p_bh'].mean()), beta_median=float(np.median(v['p_bh'])),
                  beta_win=float((v['p_bh'] > 0).mean())) for k, v in fwd_rows.items()},
              equal=ci(boots[:, 0], p_eq.mean()), equal_median=float(np.median(p_eq)),
              equal_win=float((p_eq > 0).mean()),
              beta_hedged=ci(boots[:, 1], p_bh.mean()), beta_hedged_median=float(np.median(p_bh)),
              beta_hedged_win=float((p_bh > 0).mean()))
    costs = {}
    for c in (0.001, 0.002, 0.003):
        costs[f'rt_{c * 100:.1f}pct'] = dict(
            equal_net_per_event_pct=float((p_eq.mean() - c) * 100),
            beta_hedged_net_per_event_pct=float((p_bh.mean() - c) * 100),
            naive_annual_net_pct=float((p_bh.mean() - c) * len(valid) * 100))
    ev['cost_scenarios'] = costs

    result = dict(date='2026-10-08', pair='long HYPE / short BTC',
                  standing=contrib, event_driven=ev)
    out = BASE / '2026-10-08-pair盈亏归因-HYPE-BTC-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('常驻pair全年(等名义): 总 %+0.1f%% = 涨时 %+0.1f%% + 跌时 %+0.1f%% + 横盘 %+0.1f%%' % (
        contrib['total_pct'], contrib['up_contrib_pct'], contrib['down_contrib_pct'], contrib['flat_contrib_pct']))
    es = contrib['event_split']
    print('  事件分解: 涨事件(n=%d, 比%.3f)贡献 %+.1f%% + 跌事件(n=%d, 比%.3f)贡献 %+.1f%% = 事件净 %+.1f%% | 非事件净 %+.1f%% (非事件比 %.3f/%.3f)' % (
        es['up_event']['n'], es['up_event']['ratio'], es['up_event']['pair_contrib_pct'],
        es['down_event']['n'], es['down_event']['ratio'], es['down_event']['pair_contrib_pct'],
        es['event_net_pct'], es['nonevent_net_pct'], es['nonevent_up_ratio'], es['nonevent_down_ratio']))
    print('  其中 BTC全年: 上涨分钟合计 %+0.1f%%(n=%d), 下跌分钟合计 %+0.1f%%(n=%d)' % (
        contrib['btc_up_move_total_pct'], contrib['n_up'],
        contrib['btc_down_move_total_pct'], contrib['n_down']))
    print('  pair每bar均值: 涨时 %+0.4f%%, 跌时 %+0.4f%%' % (
        contrib['pnl_up_bar_mean_pct'], contrib['pnl_down_bar_mean_pct']))
    print('事件驱动(BTC 5m<-0.5%%, 对齐口径): n=%d β=%.2f' % (ev['events'], ev['beta']))
    for k in ('3', '12', '48'):
        d = ev['by_horizon'][k]
        print('  持有%sbar: 等名义 %+.3f%%(中位%+.3f 胜率%.0f%%) | beta对冲 %+.3f%%(中位%+.3f 胜率%.0f%%)' % (
            k, d['equal_mean'] * 100, d['equal_median'] * 100, d['equal_win'] * 100,
            d['beta_mean'] * 100, d['beta_median'] * 100, d['beta_win'] * 100))
    for k, v in ev['cost_scenarios'].items():
        print('  成本%s: 对冲版净/事件(4h) %+.3f%% → 朴素年化净 %+0.0f%%' % (
            k, v['beta_hedged_net_per_event_pct'], v['naive_annual_net_pct']))


if __name__ == '__main__':
    main()
