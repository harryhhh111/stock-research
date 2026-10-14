"""BTC明显上涨后HYPE响应的秒级验证：aggTrades事件研究（1秒分辨率）。

数据：数字资产/factcheck 归档的 Binance USDT本位永续 aggTrades（2026-07-04~2026-10-03 UTC，
BTC 1.04亿条 / HYPE 4,901万条，核对见 数字资产/factcheck/2026-10-06-aggTrades同步-*.json）。

与 1分钟版的关系：1分钟版发现常规冲击同步完成于同一分钟、0.8%组滞后约1分钟。本研究把
分辨率推进到秒，回答"同一分钟内部，HYPE到底比BTC晚几秒"。

口径：以UTC自然秒为网格，每秒取最后一笔成交价（无成交秒前向填充），秒收益=log(p_ff[s]/p_ff[s-1])。
事件分钟=1分钟版同口径（聚合1m收盘收益>阈值，30分钟去簇），窗口=[分钟首秒, 分钟末秒]。

三部分：
G. 事件分钟内"到达时间"（主）：BTC/HYPE 从分钟起点累积到全分钟涨幅的25%/50%/75%所需秒数，
   Δ=τ_H−τ_B，均值与其中位数，块聚类bootstrap（块=24小时=1440分钟）；
H. 大BTC秒后的HYPE秒级脉冲响应（探索）：BTC秒收益>本窗口99.9分位的事件秒，
   之后k=0..15秒HYPE收益的均值与累计，块bootstrap；
I. 1秒互相关（描述性）：corr(rB_s[t], rH_s[t+k])，k∈[-10,+10]，无条件/条件大秒。

主要终点事前登记：theta=+0.25%事件分钟到达50%涨幅的时间差中位数（秒）。其余探索性。
注意：成交明细看不到报价更新，测的是"成交价格响应"而非"盘口报价响应"；HYPE无成交的秒
收益为0（前向填充），crossing时间只在其真实成交的秒上跳变，不受影响。
"""
import json
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
AGG = ROOT / '数字资产' / 'factcheck' / 'data' / 'normalized' / 'binance-perp' / 'aggtrades'
K1M = ROOT / '数字资产' / 'factcheck' / 'data' / 'normalized' / 'binance-perp' / '1m'
S0 = 1783123200                 # 2026-07-04T00:00:00Z（秒）
S1 = 1791072000                 # 2026-10-04T00:00:00Z（不含）
NSEC = S1 - S0                  # 7,948,800 秒
REPS = 20000
RNG = np.random.default_rng(20261006)


def load_trades(tok):
    z = np.load(AGG / tok / '2026-07-04-2026-10-04.npz')
    return z['t_ms'], z['price'], z['qty']


def load_klines(tok):
    p = K1M / tok / '1759515300000-1791051300000.json'
    doc = json.loads(p.read_bytes())
    t = np.array([c['open_time_ms'] for c in doc['candles']], dtype=np.int64)
    close = np.array([c['close'] for c in doc['candles']])
    vol = np.array([c['volume'] for c in doc['candles']])
    return t, close, vol


def build_grid(t_ms, price, qty):
    """每秒最后成交价（前向填充）与每秒成交量；返回price_ff[NSEC], vol[NSEC], n_empty。"""
    sec = t_ms // 1000 - S0
    assert np.all(sec >= 0) and np.all(sec < NSEC) and np.all(np.diff(sec) >= 0)
    bounds = np.flatnonzero(np.r_[True, sec[1:] > sec[:-1]])
    last_idx = np.r_[bounds[1:] - 1, len(sec) - 1]
    p_last = np.full(NSEC, np.nan)
    p_last[sec[last_idx]] = price[last_idx]
    vol = np.zeros(NSEC)
    np.add.at(vol, sec, qty)
    valid = ~np.isnan(p_last)
    idx = np.maximum.accumulate(np.where(valid, np.arange(NSEC), 0))
    p_ff = p_last[idx]
    if np.isnan(p_ff[0]):                       # 首秒前无成交则以首个有效价回填
        first = int(np.argmax(valid))
        p_ff[:first] = p_last[first]
    return p_ff, vol, int((~valid).sum())


def block_boot(rows, block_ids, reps=REPS, stat='mean'):
    """块聚类bootstrap。mean=按块加权平均；median=重抽样整天后取事件池中位数。"""
    uniq = np.unique(block_ids)
    loc = {b: np.where(block_ids == b)[0] for b in uniq}
    draws = RNG.integers(0, len(uniq), size=(reps, len(uniq)))
    if stat == 'mean':
        sums = np.array([rows[loc[b]].sum(axis=0) for b in uniq])
        cnts = np.array([len(loc[b]) for b in uniq], dtype=float)
        out = np.empty((reps, rows.shape[1]))
        for r in range(reps):
            w = np.bincount(draws[r], minlength=len(uniq)).astype(float)
            out[r] = (w @ sums) / (w @ cnts)
        return out
    if stat == 'median':
        out = np.empty((reps, rows.shape[1]))
        for r in range(reps):
            sel = np.concatenate([loc[b] for b in uniq[draws[r]]])
            out[r] = np.median(rows[sel], axis=0)
        return out
    raise ValueError(stat)


def ci(boot, center):
    center = np.atleast_1d(np.asarray(center, dtype=float))
    if boot.ndim == 1:
        lo, hi = np.percentile(boot, [2.5, 97.5])
        return dict(estimate=[float(x) for x in center], ci95_lo=[float(lo)],
                    ci95_hi=[float(hi)], boot_std=[float(boot.std())])
    lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
    return dict(estimate=[float(x) for x in center], ci95_lo=[float(x) for x in lo],
                ci95_hi=[float(x) for x in hi], boot_std=[float(x) for x in boot.std(axis=0)])


def cross_times(p_ff, base, total):
    """分钟窗口[base, base+60)内，累积收益首达f*total的秒偏移（f=25%/50%/75%）；达不到记NaN。"""
    cs = np.cumsum(np.log(p_ff[base:base + 60] / p_ff[base - 1]))
    out = []
    for f in (0.25, 0.5, 0.75):
        hit = np.where(cs >= f * total)[0]
        out.append(float(hit[0]) if len(hit) else np.nan)
    return out


def part_g(rb1, pff_b, pff_h, theta):
    """事件分钟内到达时间差。rb1: 1m收盘对收盘收益（全窗口数组，事件按窗口过滤）。"""
    raw = np.where(rb1 > theta)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 30])]
    m = keep + 1                                            # 事件bar下标
    ms = m * 60000 + 1759515300000
    w = (ms >= S0 * 1000) & (ms + 60000 <= S1 * 1000)
    m, ms = m[w], ms[w]
    base = (ms // 1000 - S0).astype(np.int64)               # 分钟首秒网格下标
    tot_b = np.log(pff_b[base + 59] / pff_b[base - 1])
    tot_h = np.log(pff_h[base + 59] / pff_h[base - 1])
    ok = (tot_b > theta * 0.8) & (tot_h > 1e-5)             # HYPE全分钟涨幅需为正
    base, tot_b, tot_h = base[ok], tot_b[ok], tot_h[ok]
    n_skip_hype = int((~ok).sum())
    tau_b = np.array([cross_times(pff_b, b, tb) for b, tb in zip(base, tot_b)])
    tau_h = np.array([cross_times(pff_h, b, th) for b, th in zip(base, tot_h)])
    delta = tau_h - tau_b                                   # (n, 3)，正值=HYPE滞后
    valid = ~np.isnan(delta).any(axis=1)
    delta, base = delta[valid], base[valid]
    blk = base // 60 // 1440                                # 24小时块
    return dict(
        theta=theta, raw_events=int(len(raw)), events=int(len(delta)),
        skipped_nonpositive_hype=n_skip_hype, skipped_no_cross=int((~valid).sum()),
        delta_sec=dict(
            fraction=[0.25, 0.5, 0.75],
            mean=ci(block_boot(delta, blk, stat='mean'), delta.mean(axis=0)),
            median=ci(block_boot(delta, blk, stat='median'), np.median(delta, axis=0)),
            q25=[float(x) for x in np.percentile(delta, 25, axis=0)],
            q75=[float(x) for x in np.percentile(delta, 75, axis=0)],
            frac_hype_lags=[float((delta[:, j] > 0).mean()) for j in range(3)],
            frac_sync=[float((delta[:, j] == 0).mean()) for j in range(3)],
            frac_hype_leads=[float((delta[:, j] < 0).mean()) for j in range(3)]),
        total_b_mean=float(tot_b.mean()), total_h_mean=float(tot_h.mean()))


def part_h(rs_b, rs_h):
    """大BTC秒（rB>99.9分位）后HYPE秒级脉冲响应（探索）。"""
    q = float(np.quantile(rs_b, 0.999))
    ev = np.where(rs_b > q)[0]
    ev = ev[(ev >= 20) & (ev + 16 < NSEC - 1)]
    K = 16
    per = np.column_stack([rs_h[ev + k] for k in range(K)])
    cum = np.cumsum(per, axis=1)
    base_mean = float(rs_h.mean())
    boot = block_boot(np.column_stack([per, cum]), ev // 86400)
    return dict(q999_1s=q, n_events=int(len(ev)),
                mean_btc_event=float(rs_b[ev].mean()),
                per_sec=dict(k=[int(k) for k in range(K)],
                             hype_event=ci(boot[:, :K], per.mean(axis=0)),
                             hype_diff=ci(boot[:, :K] - base_mean, per.mean(axis=0) - base_mean),
                             base=base_mean),
                cum=dict(k=[int(k) for k in range(K)],
                         hype_event=ci(boot[:, K:], cum.mean(axis=0)),
                         hype_diff=ci(boot[:, K:] - base_mean * np.arange(1, K + 1),
                                      cum.mean(axis=0) - base_mean * np.arange(1, K + 1))))


def part_i(rs_b, rs_h):
    """1秒互相关（描述性）。k>0=HYPE在BTC后k秒。"""
    lags = list(range(-10, 11))

    def corr_set(idx):
        out = []
        for k in lags:
            if k >= 0:
                x, y = rs_b[idx], rs_h[idx + k]
            else:
                x, y = rs_b[idx - k], rs_h[idx]
            out.append(float(np.corrcoef(x, y)[0, 1]))
        return out

    all_idx = np.arange(20, NSEC - 1 - 20)
    q = float(np.quantile(rs_b, 0.999))
    big = all_idx[np.abs(rs_b[all_idx]) > q]
    up = all_idx[rs_b[all_idx] > q]
    return dict(lags_sec=lags, uncond=corr_set(all_idx), cond_abs=corr_set(big),
                cond_up=corr_set(up), n_cond_abs=int(len(big)), n_cond_up=int(len(up)))


def grid_check(pff, vol, t1, c1, v1, n_empty):
    """1秒网格聚合回1分钟，与归档K线比对（量与收盘）。"""
    sel = (t1 >= S0 * 1000) & (t1 < S1 * 1000)
    kt, kc, kv = t1[sel], c1[sel], v1[sel]
    base = (kt // 1000 - S0).astype(np.int64)
    gv = vol[base[:, None] + np.arange(60)].sum(axis=1)
    rel = np.abs(gv - kv) / np.maximum(kv, 1e-12)
    return dict(n_minutes=int(len(kt)), empty_seconds=int(n_empty),
                volume_max_rel_diff=float(rel.max()),
                volume_mean_rel_diff=float(rel.mean()),
                close_max_abs_diff=float(np.abs(pff[base + 59] - kc).max()))


def main():
    tb1, cb1, vb1 = load_klines('BTC')
    th1, ch1, vh1 = load_klines('HYPE')
    t_b, p_b, q_b = load_trades('BTC')
    t_h, p_h, q_h = load_trades('HYPE')
    pffb, volb, emptyb = build_grid(t_b, p_b, q_b)
    pffh, volh, emptyh = build_grid(t_h, p_h, q_h)
    rs_b = np.empty(NSEC)
    rs_h = np.empty(NSEC)
    rs_b[0] = rs_h[0] = 0.0
    rs_b[1:] = np.log(pffb[1:] / pffb[:-1])
    rs_h[1:] = np.log(pffh[1:] / pffh[:-1])
    result = dict(date='2026-10-06',
                  data_window_utc='2026-07-04T00:00:00Z..2026-10-04T00:00:00Z(不含)',
                  interval='1s（aggTrades每秒末价网格）',
                  grid_check=dict(
                      BTC=grid_check(pffb, volb, tb1, cb1, vb1, emptyb),
                      HYPE=grid_check(pffh, volh, th1, ch1, vh1, emptyh)),
                  pre_registered_primary='theta=+0.25%事件分钟：HYPE与BTC到达全分钟涨幅50%的时间差中位数（秒）',
                  part_G=[part_g(rb1, pffb, pffh, t) for t in (0.0025, 0.005)
                          for rb1 in [np.log(cb1[1:] / cb1[:-1])]],
                  part_H=part_h(rs_b, rs_h),
                  part_I=part_i(rs_b, rs_h))
    out = BASE / '2026-10-06-BTC大涨后HYPE响应-秒级-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    g = result['part_G'][0]
    print('网格校验 BTC:', result['grid_check']['BTC'])
    print('网格校验 HYPE:', result['grid_check']['HYPE'])
    print('G theta=0.25%%: events=%d/%d, 全分钟涨幅 B=%+.3f%% H=%+.3f%%' %
          (g['events'], g['raw_events'], g['total_b_mean'] * 100, g['total_h_mean'] * 100))
    for j, f in enumerate((0.25, 0.5, 0.75)):
        m = g['delta_sec']['mean']
        md = g['delta_sec']['median']
        print('  Δ(f=%.2f): mean %+.2fs [%+.2f,%+.2f]  median %+.2fs [%+.2f,%+.2f]  滞后%.0f%% 同步%.0f%% 领先%.0f%%' %
              (f, m['estimate'][j], m['ci95_lo'][j], m['ci95_hi'][j],
               md['estimate'][j], md['ci95_lo'][j], md['ci95_hi'][j],
               g['delta_sec']['frac_hype_lags'][j] * 100,
               g['delta_sec']['frac_sync'][j] * 100,
               g['delta_sec']['frac_hype_leads'][j] * 100))
    g5 = result['part_G'][1]
    print('G theta=0.5%%: events=%d, Δ(0.5) median %+.2fs mean %+.2fs' %
          (g5['events'], g5['delta_sec']['median']['estimate'][1], g5['delta_sec']['mean']['estimate'][1]))
    h = result['part_H']
    print('H 1s脉冲: q99.9=%+.4f%%, n=%d, 事件秒BTC均值%+.3f%%' % (h['q999_1s'] * 100, h['n_events'], h['mean_btc_event'] * 100))
    print('  HYPE k=0..5均值%%:', [round(x * 100, 4) for x in h['per_sec']['hype_event']['estimate'][:6]],
          '累计k=0..5%%:', [round(x * 100, 4) for x in h['cum']['hype_event']['estimate'][:6]])
    i = result['part_I']
    print('I 1s互相关 k=-3..+3: uncond', [round(x, 3) for x in i['uncond'][7:14]],
          '|cond_abs', [round(x, 3) for x in i['cond_abs'][7:14]])


if __name__ == '__main__':
    main()
