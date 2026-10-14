"""HYPE vs ETH vs SOL：三币对 BTC 的跟随对比。

研究问题：HYPE 的跟随特征（beta≈1.2、涨紧跌松、巨震收缩、8月联动变松、秒级同秒80~89%）
是 HYPE 特有，还是 alt 永续普遍现象？需要同口径的 ETH、SOL 对照。

数据（与 HYPE 完全相同口径）：
- 全年1分钟K线 binance-perp（BTC+HYPE+ETH+SOL，2025-10-04~2026-10-04 北京）
- aggTrades 1秒网格（2026-07-04~10-03 UTC，四币）

对比项（全部四币同口径计算）：
A. 多尺度 beta：1s / 1m / 5m / 1h 回归斜率、corr、R²；
B. 涨跌不对称：上涨/下跌样本 beta 与大事件均值比；
C. 大 BTC 秒脉冲（共同事件集，1s>99.9分位）：同秒响应占比、k=0..5累计、episode内外；
D. 30天滚动 beta（1m）时变：全期分布与8月episode中位；
E. 8月21个上行段（与案例研究同口径）：各币段beta、Δ(50%)滞后。
纯描述统计。
"""
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m

BASE = Path(__file__).resolve().parent
TOKENS = ['HYPE', 'ETH', 'SOL']
EP0 = int(__import__('datetime').datetime(2026, 8, 18, tzinfo=__import__('datetime').timezone.utc).timestamp())
EP1 = int(__import__('datetime').datetime(2026, 8, 26, tzinfo=__import__('datetime').timezone.utc).timestamp())
LEG = 1800
RTH = 0.01


def beta(y, x):
    x, y = np.asarray(x, float), np.asarray(y, float)
    b = float(np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1))
    c = float(np.corrcoef(x, y)[0, 1])
    return dict(beta=b, corr=c, r2=c * c)


def load_klines(tok):
    p = m.K1M / tok / '1759515300000-1791051300000.json'
    doc = json.loads(p.read_bytes())
    t = np.array([c['open_time_ms'] for c in doc['candles']], dtype=np.int64)
    close = np.array([c['close'] for c in doc['candles']])
    return t, close


def build_grid_tok(tok):
    z = np.load(m.AGG / tok / '2026-07-04-2026-10-04.npz')
    p_ff, vol, _ = m.build_grid(z['t_ms'], z['price'], z['qty'])
    rs = np.empty(m.NSEC)
    rs[0] = 0.0
    rs[1:] = np.log(p_ff[1:] / p_ff[:-1])
    return p_ff, rs


def cross(p_ff, lo, hi, total):
    cs = np.cumsum(np.log(p_ff[lo:hi + 1] / p_ff[lo - 1]))
    for f in (0.5,):
        hit = np.where(cs >= f * total)[0]
        return int(hit[0]) if len(hit) else None


def find_legs(p_ff):
    lo = EP0 - m.S0
    hi = EP1 - m.S0
    r30 = np.full(m.NSEC, np.nan)
    r30[lo:hi] = np.log(p_ff[lo:hi] / p_ff[lo - LEG:hi - LEG])
    cand = np.where(r30 > RTH)[0]
    legs = []
    for s in cand:
        if legs and s - legs[-1][1] < LEG:
            if r30[s] > r30[legs[-1][1]]:
                legs[-1][1] = s
        else:
            legs.append([s, s])
    return [(s - LEG, s) for _, s in legs]


def main():
    _, cb = load_klines('BTC')
    rb1 = np.log(cb[1:] / cb[:-1])
    b5 = cb.reshape(-1, 5)
    rb5 = np.log(b5[:, -1][1:] / b5[:, -1][:-1])
    bh = cb.reshape(-1, 60)
    rbh = np.log(bh[:, -1][1:] / bh[:, -1][:-1])
    pffb, rs_b = build_grid_tok('BTC')

    out = {}
    for tok in TOKENS:
        _, ck = load_klines(tok)
        rk1 = np.log(ck[1:] / ck[:-1])
        k5 = ck.reshape(-1, 5)
        rk5 = np.log(k5[:, -1][1:] / k5[:, -1][:-1])
        kh = ck.reshape(-1, 60)
        rkh = np.log(kh[:, -1][1:] / kh[:, -1][:-1])
        p_ff, rs_k = build_grid_tok(tok)

        A = dict(s1=beta(rs_k, rs_b), m1=beta(rk1, rb1), m5=beta(rk5, rb5), h1=beta(rkh, rbh))
        up = rb1 > 0
        dn = rb1 < 0
        B = dict(up_beta=beta(rk1[up], rb1[up])['beta'],
                 down_beta=beta(rk1[dn], rb1[dn])['beta'])
        evu = rb1 > 0.0025
        evd = rb1 < -0.0025
        B['up_event_ratio'] = float(rk1[evu].mean() / rb1[evu].mean())
        B['down_event_ratio'] = float(rk1[evd].mean() / rb1[evd].mean())
        B['up_event_n'] = int(evu.sum())
        # C: 大BTC秒（共同事件集）
        q999 = float(np.quantile(rs_b, 0.999))
        ev = np.where(rs_b > q999)[0]
        ev = ev[(ev >= 20) & (ev + 6 < m.NSEC - 1)]
        K = 6
        per = np.column_stack([rs_k[ev + k] for k in range(K)])
        cum = np.cumsum(per, axis=1)
        in_ep = (ev >= EP0 - m.S0) & (ev < EP1 - m.S0)
        C = dict(q999_1s=q999, n_events=int(len(ev)),
                 same_sec_ratio_all=float(rs_k[ev].mean() / rs_b[ev].mean()),
                 cum_k5_all=float(cum[:, 4].mean() / rs_b[ev].mean()),
                 same_sec_ratio_in=float(rs_k[ev[in_ep]].mean() / rs_b[ev[in_ep]].mean()),
                 same_sec_ratio_out=float(rs_k[ev[~in_ep]].mean() / rs_b[ev[~in_ep]].mean()),
                 cum_k5_in=float(cum[in_ep][:, 4].mean() / rs_b[ev[in_ep]].mean()),
                 cum_k5_out=float(cum[~in_ep][:, 4].mean() / rs_b[ev[~in_ep]].mean()),
                 n_in=int(in_ep.sum()), n_out=int((~in_ep).sum()))
        # D: 滚动30d beta
        win = 43200
        sx = np.concatenate([[0], np.cumsum(rb1)])
        sy = np.concatenate([[0], np.cumsum(rk1)])
        sxy = np.concatenate([[0], np.cumsum(rb1 * rk1)])
        sxx = np.concatenate([[0], np.cumsum(rb1 * rb1)])
        i = np.arange(win, len(rb1))
        mx = (sx[i] - sx[i - win]) / win
        my = (sy[i] - sy[i - win]) / win
        cxy = (sxy[i] - sxy[i - win]) / win - mx * my
        cxx = (sxx[i] - sxx[i - win]) / win - mx * mx
        b30 = cxy / cxx
        tms = (i + 1) * 60000 + 1759515300000
        inep = (tms >= EP0 * 1000) & (tms < EP1 * 1000)
        D = dict(mean=float(b30.mean()), min=float(b30.min()),
                 max=float(b30.max()),
                 min_date=int(tms[int(b30.argmin())]), max_date=int(tms[int(b30.argmax())]),
                 episode_median=float(np.median(b30[inep])),
                 out_median=float(np.median(b30[~inep])))
        # E: 8月21段
        legs = find_legs(pffb)
        rows = []
        for w0, w1 in legs:
            tb = float(np.log(pffb[w1] / pffb[w0 - 1]))
            tk = float(np.log(p_ff[w1] / p_ff[w0 - 1]))
            cbs = cross(pffb, w0, w1, tb)
            cks = cross(p_ff, w0, w1, tk) if tk > 1e-5 else None
            rows.append(dict(peak_utc=__import__('datetime').datetime.fromtimestamp(w1 + m.S0, __import__('datetime').timezone.utc).isoformat(),
                             btc_pct=tb * 100, tok_pct=tk * 100,
                             leg_beta=tk / tb if tb else None,
                             lag50_s=(cks - cbs) if (cks is not None and cbs is not None) else None))
        betas = [r['leg_beta'] for r in rows if r['leg_beta'] is not None]
        E = dict(n_legs=len(rows),
                 leg_beta_median=float(np.median(betas)) if betas else None,
                 leg_beta_min=float(np.min(betas)) if betas else None,
                 leg_beta_max=float(np.max(betas)) if betas else None,
                 big_legs=[r for r in rows if r['btc_pct'] > 2.5],
                 rows=rows)
        out[tok] = dict(A=A, B=B, C=C, D=D, E=E)

    result = dict(date='2026-10-07', tokens=TOKENS, compare=out)
    path = BASE / '2026-10-07-三币跟随对比-结果.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    import datetime as dt
    d = lambda ms: dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).date().isoformat()
    print('A. 多尺度beta (beta/corr/R2):')
    for s in ('s1', 'm1', 'm5', 'h1'):
        print('  %-3s ' % s + '  '.join('%s %.2f/%.2f/%.2f' % (t, out[t]['A'][s]['beta'], out[t]['A'][s]['corr'], out[t]['A'][s]['r2']) for t in TOKENS))
    print('B. 涨跌不对称:')
    for t in TOKENS:
        b = out[t]['B']
        print('  %s upβ %.2f downβ %.2f 事件比 up %.2f down %.2f (n=%d)' % (
            t, b['up_beta'], b['down_beta'], b['up_event_ratio'], b['down_event_ratio'], b['up_event_n']))
    print('C. 大BTC秒同秒响应占比 (k0全 / k0内 / k0外 / k5全 / k5内 / k5外):')
    for t in TOKENS:
        c = out[t]['C']
        print('  %s %.2f / %.2f / %.2f / %.2f / %.2f / %.2f  (n=%d, 内%d/外%d)' % (
            t, c['same_sec_ratio_all'], c['same_sec_ratio_in'], c['same_sec_ratio_out'],
            c['cum_k5_all'], c['cum_k5_in'], c['cum_k5_out'], c['n_events'], c['n_in'], c['n_out']))
    print('D. 滚动30d beta(1m):')
    for t in TOKENS:
        dd = out[t]['D']
        print('  %s 均值%.2f [%.2f(%s)~%.2f(%s)] 8月中位%.2f 段外中位%.2f' % (
            t, dd['mean'], dd['min'], d(dd['min_date']), dd['max'], d(dd['max_date']),
            dd['episode_median'], dd['out_median']))
    print('E. 8月上行段:')
    for t in TOKENS:
        e = out[t]['E']
        print('  %s 段beta中位 %.2f [%.2f, %.2f]' % (t, e['leg_beta_median'], e['leg_beta_min'], e['leg_beta_max']))
        for r in e['big_legs']:
            print('     %s B%+.2f%% %s%+.2f%% beta %.2f lag50 %s' % (
                r['peak_utc'][5:16], r['btc_pct'], t, r['tok_pct'],
                r['leg_beta'] if r['leg_beta'] is not None else float('nan'),
                r['lag50_s']))


if __name__ == '__main__':
    main()
