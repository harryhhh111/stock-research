"""检验说法："BTC涨时SOL跟着涨，BTC跌之前SOL先跌"。

两个可证伪断言：
 H1（跟涨）：BTC上涨时SOL同步上涨——已有多尺度beta支持，这里补命中率；
 H2（跌前先导）：BTC下跌事件发生前，SOL已系统性下跌——主检验。

数据：全年1分钟K线（BTC/SOL/ETH，2025-10-04~2026-10-04）+ aggTrades 1秒网格（2026-07-04~10-03）。

五部分（全部四币同口径，SOL为主，ETH为对照）：
A. 跟涨命中率：P(币涨|BTC 1m>0.25%)、条件均值比；
B. 跌前漂移（主终点）：BTC 5m<-0.5%事件（全年，30分钟去簇），事件bar之前1/2/3根
   币的累计收益 vs 无条件基线，块聚类bootstrap(288根≈24h) diff CI；涨事件(+0.5%)做
   对称性对照；ETH同算（区分SOL特有 vs alt共性）；
C. 峰顶时差（1秒网格）：BTC 1m<-0.25%事件分钟，前15分钟+事件分钟内SOL/ETH/BTC各自
   log价格argmax时刻之差（负=币先见顶），中位数与先行占比；涨事件同算；
D. 大下跌秒条件互相关（1秒网格）：rB_1s<-99.9分位秒，corr(rB_t, rX_{t+k}) k=-5..+5，
   涨秒对照，三币并列；
E. 若存在先导的描述性收益：SOL 5m<-0.5%后BTC随后5/15分钟收益（非回测，仅描述）。

主要终点事前登记：B部 SOL 事件前3根(15分钟)跌前漂移 diff vs 基线。其余探索性。
"""
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m

BASE = Path(__file__).resolve().parent
TOKENS = ['SOL', 'ETH', 'HYPE']
BLOCK = 288
REPS = 20000
RNG = np.random.default_rng(20261008)
EP0 = int(__import__('datetime').datetime(2026, 8, 18, tzinfo=__import__('datetime').timezone.utc).timestamp())


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
    if boot.ndim == 1:
        lo, hi = np.percentile(boot, [2.5, 97.5])
        return dict(estimate=[float(x) for x in center], ci95_lo=[float(lo)], ci95_hi=[float(hi)])
    lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
    return dict(estimate=[float(x) for x in center], ci95_lo=[float(x) for x in lo],
                ci95_hi=[float(x) for x in hi])


def part_a(rb1, rk):
    out = {}
    for th in (0.0025, 0.005):
        up = rb1 > th
        dn = rb1 < -th
        out[f'up_{th}'] = dict(n=int(up.sum()), p_token_up=float((rk[up] > 0).mean()),
                               mean_ratio=float(rk[up].mean() / rb1[up].mean()),
                               token_mean=float(rk[up].mean() * 100), btc_mean=float(rb1[up].mean() * 100))
        out[f'dn_{th}'] = dict(n=int(dn.sum()), p_token_dn=float((rk[dn] < 0).mean()),
                               mean_ratio=float(rk[dn].mean() / rb1[dn].mean()),
                               token_mean=float(rk[dn].mean() * 100), btc_mean=float(rb1[dn].mean() * 100))
    out['p_up_uncond'] = float((rk > 0).mean())
    return out


def part_b(rb5, rk5, theta):
    """事件前漂移。rb5[i]=bar i+1收益；事件bar=i+1；之前k根=rb5[i-k..i-1]。"""
    n = len(rb5)
    side = {}
    for name, cond in (('down', rb5 < -theta), ('up', rb5 > theta)):
        raw = np.where(cond)[0]
        keep = raw[np.concatenate([[True], np.diff(raw) >= 6])]
        valid = keep[(keep >= 3) & (keep <= n - 2 - 12)]
        base_idx = np.arange(3, n - 14)
        K = 3
        def pre(ret, idx):
            return np.column_stack([ret[idx - k] for k in range(1, K + 1)])
        pre_k = pre(rk5, valid)
        cum_k = np.cumsum(pre_k, axis=1)
        pre_b = pre(rb5, valid)
        cum_b = np.cumsum(pre_b, axis=1)
        base = pre(rk5, base_idx)
        base_cum = np.cumsum(base, axis=1)
        M = np.column_stack([pre_k, cum_k])
        boots = block_boot(M, valid // BLOCK)
        bc = np.concatenate([base.mean(axis=0), base_cum.mean(axis=0)])
        delta = boots - bc
        side[name] = dict(events=int(len(valid)),
                          pre_bars_pct=[float(x * 100) for x in cum_b.mean(axis=0)],
                          token_pre_diff=ci(delta[:, K:], cum_k.mean(axis=0) - base_cum.mean(axis=0)),
                          token_pre_event_mean=ci(boots[:, K:], cum_k.mean(axis=0)),
                          base_pre_mean=[float(x * 100) for x in base_cum.mean(axis=0)])
    return side


def part_c(rb1, pff, grids, theta):
    """峰顶时差（1秒网格）。事件分钟bar m（rb1[m-1]为事件收益）。窗口=[m_open-900, m_open+60)。"""
    out = {}
    for name, sel in (('down', rb1 < -theta), ('up', rb1 > theta)):
        raw = np.where(sel)[0]
        keep = raw[np.concatenate([[True], np.diff(raw) >= 30])]
        bars = keep + 1
        ms = bars * 60000 + 1759515300000
        w = (ms >= m.S0 * 1000 + 900000) & (ms + 60000 <= m.S1 * 1000)
        bars, ms = bars[w], ms[w]
        base = (ms // 1000 - m.S0).astype(np.int64)
        W0 = 900
        peak = {}
        for tok in ['BTC'] + TOKENS:
            g = pff if tok == 'BTC' else grids[tok]
            pk = np.array([int(np.argmax(np.log(g[b - W0:b + 60]))) for b in base])
            peak[tok] = pk - W0                     # 相对事件分钟开盘的秒偏移
        d = {tok: (peak[tok] - peak['BTC']).astype(float) for tok in TOKENS}
        out[name] = dict(events=int(len(base)),
                         peak_offset_btc_mean=float(peak['BTC'].mean()),
                         median_lag_s={tok: float(np.median(d[tok])) for tok in TOKENS},
                         frac_lead={tok: float((d[tok] < 0).mean()) for tok in TOKENS},
                         q25_lag_s={tok: float(np.percentile(d[tok], 25)) for tok in TOKENS},
                         q75_lag_s={tok: float(np.percentile(d[tok], 75)) for tok in TOKENS})
    return out


def part_d(rs_b, grids):
    """大秒条件互相关。k<0=币在BTC之前k秒。"""
    lags = list(range(-5, 6))
    q_dn = float(np.quantile(rs_b, 0.001))
    q_up = float(np.quantile(rs_b, 0.999))
    idx_all = np.arange(20, m.NSEC - 1 - 20)
    out = {}
    for name, mask in (('down', rs_b < q_dn), ('up', rs_b > q_up)):
        ev = idx_all[mask[idx_all]]
        row = {}
        for tok in TOKENS:
            rs_k = grids[tok]
            corrs = []
            for k in lags:
                x, y = rs_b[ev], rs_k[ev + k]
                corrs.append(float(np.corrcoef(x, y)[0, 1]))
            row[tok] = corrs
        out[name] = dict(n=int(len(ev)), lags=lags, corr=row)
    return out


def part_e(rb5_sol, rb5_btc):
    """SOL 5m<-0.5% 后 BTC 的前向收益（描述性）。SOL领跌→BTC后续应偏弱。"""
    raw = np.where(rb5_sol < -0.005)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 6])]
    valid = keep[keep <= len(rb5_sol) - 2 - 12]
    per = np.column_stack([rb5_btc[valid + k] for k in range(1, 13)])
    cum = np.cumsum(per, axis=1)
    fwd = cum[:, [2, 5, 11]]                    # k=3/6/12根 → 15/30/60分钟
    boots = block_boot(fwd, valid // BLOCK)
    return dict(events=int(len(valid)),
                btc_fwd=ci(boots, fwd.mean(axis=0)),
                horizon_min=[15, 30, 60])


def main():
    cb = load_k('BTC')
    rb1 = np.log(cb[1:] / cb[:-1])
    b5 = cb.reshape(-1, 5)
    rb5 = np.log(b5[:, -1][1:] / b5[:, -1][:-1])
    grids = {}
    rs = {}
    for tok in TOKENS:
        z = np.load(m.AGG / tok / '2026-07-04-2026-10-04.npz')
        g, _, _ = m.build_grid(z['t_ms'], z['price'], z['qty'])
        grids[tok] = g
        r = np.empty(m.NSEC)
        r[0] = 0.0
        r[1:] = np.log(g[1:] / g[:-1])
        rs[tok] = r
    _, rs_b = None, None
    zb = np.load(m.AGG / 'BTC' / '2026-07-04-2026-10-04.npz')
    pffb, _, _ = m.build_grid(zb['t_ms'], zb['price'], zb['qty'])
    rs_b = np.empty(m.NSEC)
    rs_b[0] = 0.0
    rs_b[1:] = np.log(pffb[1:] / pffb[:-1])

    result = dict(date='2026-10-08', question='SOL是否BTC涨时跟涨、跌时领先',
                  pre_registered='BTC 5m<-0.5%事件前SOL 3根(15分钟)累计收益 vs 基线',
                  A={}, B={}, C={}, D={}, E={})
    for tok in TOKENS:
        ck = load_k(tok)
        rk1 = np.log(ck[1:] / ck[:-1])
        k5 = ck.reshape(-1, 5)
        rk5 = np.log(k5[:, -1][1:] / k5[:, -1][:-1])
        result['A'][tok] = part_a(rb1, rk1)
        result['B'][tok] = part_b(rb5, rk5, 0.005)
        result['C'][tok] = part_c(rb1, pffb, grids, 0.0025)
        result['D'][tok] = part_d(rs_b, rs)
    cs = load_k('SOL')
    s5 = cs.reshape(-1, 5)
    rb5_sol = np.log(s5[:, -1][1:] / s5[:, -1][:-1])
    result['E'] = part_e(rb5_sol, rb5)

    out = BASE / '2026-10-08-SOL领先BTC下跌检验-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for tok in TOKENS:
        a = result['A'][tok]
        print('%s 跟涨: 1m>0.25%% n=%d 命中率%.1f%% 比%.2f | 跟跌: n=%d 命中率%.1f%% 比%.2f' % (
            tok, a['up_0.0025']['n'], a['up_0.0025']['p_token_up'] * 100, a['up_0.0025']['mean_ratio'],
            a['dn_0.0025']['n'], a['dn_0.0025']['p_token_dn'] * 100, a['dn_0.0025']['mean_ratio']))
        b = result['B'][tok]
        for side in ('down', 'up'):
            d = b[side]
            est = d['token_pre_diff']
            print('  B %s %s n=%d 前3根累计diff%% CI: %s' % (
                tok, side, d['events'],
                ['%+.4f[%+.4f,%+.4f]' % (est['estimate'][j] * 100, est['ci95_lo'][j] * 100, est['ci95_hi'][j] * 100) for j in range(3)]))
        c = result['C'][tok]
        for side in ('down', 'up'):
            d = c[side]
            print('  C %s %s n=%d 峰顶时差中位 %+gs 先行占比 %.1f%% [q25 %g, q75 %g]' % (
                tok, side, d['events'], d['median_lag_s'][tok],
                d['frac_lead'][tok] * 100, d['q25_lag_s'][tok], d['q75_lag_s'][tok]))
    d = result['D']['SOL']
    for side in ('down', 'up'):
        print('D SOL %s大秒 n=%d corr k=-3..+3: %s' % (side, d[side]['n'], [round(x, 3) for x in d[side]['corr']['SOL'][2:9]]))
    e = result['E']
    print('E SOL领跌后BTC前向: n=%d 15/30/60min %%: %s' % (e['events'], [
        '%+.4f[%+.4f,%+.4f]' % (e['btc_fwd']['estimate'][j] * 100, e['btc_fwd']['ci95_lo'][j] * 100, e['btc_fwd']['ci95_hi'][j] * 100) for j in range(3)]))


if __name__ == '__main__':
    main()
