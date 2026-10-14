"""BTC明显上涨后HYPE响应的1分钟分解：事件研究（1分钟分辨率版）。

数据：数字资产/factcheck 归档的 Binance USDT本位永续1分钟K线（BTC、HYPE各525,600根，
时间完全对齐，核对见 数字资产/factcheck/2026-10-05-一年1分钟K线核对.json）。

与 5分钟版（leadlag_btc_hype.py）的关系：事件定义完全对齐——把1分钟聚合成5分钟后用
同样的阈值与去簇规则（5分钟收益>theta，30分钟去簇），因此事件集与5分钟研究一致；
新增的是把事件后15分钟拆成15个1分钟桶、以及事件5分钟bar内部的5根1分钟拆解，
回答"第二根K线的+0.067%到底发生在第几分钟"、"0.8%组+0.224%漂移集中在哪些分钟"。

口径约定（与5分钟版一致）：rb5[i]=log(close5[i+1]/close5[i])，事件=该收益>theta，
即"事件窗口"=从5m bar i收盘到bar i+1收盘，对应1m收益下标 5i+4 .. 5i+8；
事件后第k分钟 = rh1[5i+8+k]。

三部分：
D. 5分钟事件后HYPE响应的1分钟拆解（主，theta=0.5%为主终点、0.8%为探索）；
E. 1分钟级别BTC急涨事件（1分钟收益>全年99.5分位）后HYPE的分钟级响应（探索）；
F. 1分钟收益互相关（无条件与条件于大1分钟波动），看分钟级谁先动（描述性）。

推断：事件块聚类bootstrap（块=288根5分钟≈24小时；1分钟 spike 事件块=1440根1分钟）；
基线在全部样本上计算（其抽样误差远小于条件均值，bootstrap只对条件部分变动，报告注明）。
主要终点事前设定：theta=0.5%事件后第1–5分钟逐分钟diff vs 基线、累计+5分钟diff；
theta=0.8%事件后第1–15分钟。其余为敏感性或探索性。
"""
import hashlib
import json
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
DATA = ROOT / '数字资产' / 'factcheck' / 'data' / 'normalized' / 'binance-perp' / '1m'
H_MAX = 12            # 与5分钟版对齐：事件需留12根5分钟（60分钟）向前
POST_MIN = 15         # 事件后拆成15个1分钟桶
BLOCK5M = 288         # 5分钟事件的聚类块长（288根5分钟≈24小时）
BLOCK1M = 1440        # 1分钟spike事件的聚类块长（24小时）
REPS = 20000
RNG = np.random.default_rng(202610051)


def load(token):
    p = DATA / token / '1759515300000-1791051300000.json'
    raw = p.read_bytes()
    doc = json.loads(raw)
    candles = doc['candles']
    t = np.array([c['open_time_ms'] for c in candles], dtype=np.int64)
    closes = np.array([c['close'] for c in candles])
    return t, closes, hashlib.sha256(raw).hexdigest()


def block_boot_cluster(rows, block_ids, reps=REPS):
    """rows: (n_events, n_metrics)，block_ids: 每个事件所属块。返回统计量bootstrap分布。"""
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
        return dict(estimate=[float(x) for x in center], ci95_lo=[float(lo)],
                    ci95_hi=[float(hi)], boot_std=[float(boot.std())])
    lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
    return dict(estimate=[float(x) for x in center], ci95_lo=[float(x) for x in lo],
                ci95_hi=[float(x) for x in hi], boot_std=[float(x) for x in boot.std(axis=0)])


def event_matrix(rb1, rh1, last):
    """事件窗口末根1m收益下标last（数组，=5i+8），返回(列名, 事件指标矩阵)。"""
    names, arrs = [], []

    def add(name, a):
        names.append(name)
        arrs.append(np.asarray(a, dtype=float))

    add('hype_event_bar5', rh1[last] + rh1[last - 1] + rh1[last - 2] +
        rh1[last - 3] + rh1[last - 4])                       # 事件5m窗口HYPE收益（=rh5[i]）
    add('btc_event_bar5', rb1[last] + rb1[last - 1] + rb1[last - 2] +
        rb1[last - 3] + rb1[last - 4])
    for j in range(5):                                        # 事件窗口内第1..5分钟
        add(f'hype_intra_m{j + 1}', rh1[last - 4 + j])
    for j in range(5):
        add(f'btc_intra_m{j + 1}', rb1[last - 4 + j])
    for k in range(1, POST_MIN + 1):                          # 事件后第1..15分钟
        add(f'hype_post_m{k}', rh1[last + k])
    for k in range(1, POST_MIN + 1):
        add(f'btc_post_m{k}', rb1[last + k])
    for h in (5, 10, 15, 30, 60):                             # 事件后累计（1m口径）
        add(f'hype_cum_m{h}', np.array([rh1[l + 1:l + 1 + h].sum() for l in last]))
        add(f'btc_cum_m{h}', np.array([rb1[l + 1:l + 1 + h].sum() for l in last]))
    win15 = np.column_stack([rh1[last + k] for k in range(1, POST_MIN + 1)])
    add('hype_hit_up15', (win15.max(axis=1) > 0.005).astype(float))
    add('hype_hit_abs15', (np.abs(win15).max(axis=1) > 0.005).astype(float))
    return names, np.column_stack(arrs)


def baselines(rb1, rh1, fwd=60):
    """全部有效1m起点（留fwd分钟向前）的各指标基线均值，键名与event_matrix一致。

    起点b表示"事件窗口末根收益下标为b"的伪事件：窗口内第j分钟=rh1[b-4+j]，
    事件后第k分钟=rh1[b+k]，累计h=rh1[b+1..b+h]之和。对全体起点取均值。
    """
    n = len(rh1)
    nb = n - fwd - 1                                          # 起点0..nb-1
    out = {'hype_event_bar5': 5 * float(rh1[:nb].mean()),     # 5×单根均值（滑窗均值=5倍均值）
           'btc_event_bar5': 5 * float(rb1[:nb].mean())}
    for j in range(5):
        out[f'hype_intra_m{j + 1}'] = float(rh1[j:j + nb].mean())
        out[f'btc_intra_m{j + 1}'] = float(rb1[j:j + nb].mean())
    for k in range(1, POST_MIN + 1):
        out[f'hype_post_m{k}'] = float(rh1[k:k + nb].mean())
        out[f'btc_post_m{k}'] = float(rb1[k:k + nb].mean())
    crh = np.concatenate([[0.0], np.cumsum(rh1)])
    crb = np.concatenate([[0.0], np.cumsum(rb1)])
    for h in (5, 10, 15, 30, 60):
        out[f'hype_cum_m{h}'] = float((crh[1 + h:1 + h + nb] - crh[1:1 + nb]).mean())
        out[f'btc_cum_m{h}'] = float((crb[1 + h:1 + h + nb] - crb[1:1 + nb]).mean())
    from numpy.lib.stride_tricks import sliding_window_view
    w = sliding_window_view(rh1[1:1 + POST_MIN + nb - 1], POST_MIN)   # 窗口b=rh1[b+1..b+15]
    out['hype_hit_up15'] = float((w.max(axis=1) > 0.005).mean())
    out['hype_hit_abs15'] = float((np.abs(w).max(axis=1) > 0.005).mean())
    return out


def mod_matched_base(rh1, t, last):
    """日内分钟匹配基线（敏感性）：rh1[j]实现于bar j+1，用mod[j+1]对齐。

    对事件后第k分钟，取该事件对应分钟内全年同分钟的HYPE收益均值，再对事件平均。
    """
    mod = (t // 60000) % 1440
    cnt = np.bincount(mod[1:], minlength=1440).astype(float)
    s = np.bincount(mod[1:], weights=rh1, minlength=1440)
    modmean = s / cnt
    return {f'hype_post_m{k}': float(modmean[mod[last + k + 1]].mean())
            for k in range(1, POST_MIN + 1)}


def part_d(rb5, rb1, rh1, t, theta):
    """5分钟事件的1分钟拆解。事件选择与5分钟版完全一致（含向前60分钟有效性约束）。"""
    n = len(rb5)
    raw = np.where(rb5 > theta)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 6])]   # 30分钟去簇，取首个
    valid = keep[keep <= n - 2 - H_MAX]
    last = valid * 5 + 8                                       # 事件窗口末根1m收益下标
    names, M = event_matrix(rb1, rh1, last)
    base = baselines(rb1, rh1)
    bvec = np.array([base[nm] for nm in names])
    boots = block_boot_cluster(M, valid // BLOCK5M)
    center = M.mean(axis=0)
    delta = boots - bvec
    modb = mod_matched_base(rh1, t, last)
    idx = {nm: i for i, nm in enumerate(names)}

    def pick(prefix, keys):
        return [idx[f'{prefix}{k}'] for k in keys]

    post_keys = list(range(1, POST_MIN + 1))
    intra_keys = list(range(1, 6))
    cum_keys = [5, 10, 15, 30, 60]
    out = dict(
        theta=theta, raw_events=int(len(raw)), events=int(len(valid)),
        event_bar_hype_mean=float(center[idx['hype_event_bar5']]),
        event_bar_btc_mean=float(center[idx['btc_event_bar5']]),
        intra_hype=dict(pos_min=intra_keys,
                        event_mean=ci(boots[:, pick('hype_intra_m', intra_keys)],
                                      center[pick('hype_intra_m', intra_keys)]),
                        base_mean=[base[f'hype_intra_m{k}'] for k in intra_keys],
                        diff=ci(delta[:, pick('hype_intra_m', intra_keys)],
                                center[pick('hype_intra_m', intra_keys)] -
                                bvec[pick('hype_intra_m', intra_keys)])),
        intra_btc=dict(pos_min=intra_keys,
                       event_mean=[float(center[i]) for i in pick('btc_intra_m', intra_keys)],
                       base_mean=[base[f'btc_intra_m{k}'] for k in intra_keys]),
        post_hype=dict(k_min=post_keys,
                       event_mean=ci(boots[:, pick('hype_post_m', post_keys)],
                                     center[pick('hype_post_m', post_keys)]),
                       base_mean=[base[f'hype_post_m{k}'] for k in post_keys],
                       diff=ci(delta[:, pick('hype_post_m', post_keys)],
                               center[pick('hype_post_m', post_keys)] -
                               bvec[pick('hype_post_m', post_keys)]),
                       mod_matched_base=[modb[f'hype_post_m{k}'] for k in post_keys]),
        post_btc=dict(k_min=post_keys,
                      event_mean=[float(center[i]) for i in pick('btc_post_m', post_keys)],
                      base_mean=[base[f'btc_post_m{k}'] for k in post_keys]),
        cum=dict(h_min=cum_keys,
                 hype_event=ci(boots[:, pick('hype_cum_m', cum_keys)],
                               center[pick('hype_cum_m', cum_keys)]),
                 hype_base=[base[f'hype_cum_m{h}'] for h in cum_keys],
                 hype_diff=ci(delta[:, pick('hype_cum_m', cum_keys)],
                              center[pick('hype_cum_m', cum_keys)] -
                              bvec[pick('hype_cum_m', cum_keys)]),
                 btc_event=[float(center[i]) for i in pick('btc_cum_m', cum_keys)]),
        hit15=dict(up_event=ci(boots[:, idx['hype_hit_up15']], center[idx['hype_hit_up15']]),
                   up_base=base['hype_hit_up15'],
                   up_diff=ci(delta[:, idx['hype_hit_up15']], center[idx['hype_hit_up15']] - bvec[idx['hype_hit_up15']]),
                   abs_event=ci(boots[:, idx['hype_hit_abs15']], center[idx['hype_hit_abs15']]),
                   abs_base=base['hype_hit_abs15'],
                   abs_diff=ci(delta[:, idx['hype_hit_abs15']], center[idx['hype_hit_abs15']] - bvec[idx['hype_hit_abs15']])),
    )
    out['beta1m'] = float(np.cov(rb1, rh1, ddof=1)[0, 1] / np.var(rb1, ddof=1))
    out['excess_over_beta1m'] = [float(d - out['beta1m'] * b) for d, b in
                                 zip(out['cum']['hype_diff']['estimate'], out['cum']['btc_event'])]
    return out


def part_e(rb1, rh1, t, ev5_05):
    """1分钟急涨事件（探索）：1分钟收益>全年99.5分位，30分钟去簇。"""
    q = float(np.quantile(rb1, 0.995))
    raw = np.where(rb1 > q)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 30])]
    valid = keep[keep <= len(rb1) - 1 - POST_MIN]
    names, arrs = [], []

    def add(name, a):
        names.append(name)
        arrs.append(np.asarray(a, dtype=float))

    add('hype_same_m1', rh1[valid])
    add('btc_same_m1', rb1[valid])
    for k in range(1, POST_MIN + 1):
        add(f'hype_post_m{k}', rh1[valid + k])
    for h in (5, 10, 15):
        add(f'hype_cum_m{h}', np.array([rh1[v + 1:v + 1 + h].sum() for v in valid]))
        add(f'btc_cum_m{h}', np.array([rb1[v + 1:v + 1 + h].sum() for v in valid]))
    win15 = np.column_stack([rh1[valid + k] for k in range(1, POST_MIN + 1)])
    add('hype_hit_up15', (win15.max(axis=1) > 0.005).astype(float))
    M = np.column_stack(arrs)
    n = len(rb1)
    nb = n - POST_MIN - 1
    base = {'hype_same_m1': float(rh1[:nb].mean()), 'btc_same_m1': float(rb1[:nb].mean())}
    for k in range(1, POST_MIN + 1):
        base[f'hype_post_m{k}'] = float(rh1[k:k + nb].mean())
    crh = np.concatenate([[0.0], np.cumsum(rh1)])
    crb = np.concatenate([[0.0], np.cumsum(rb1)])
    for h in (5, 10, 15):
        base[f'hype_cum_m{h}'] = float((crh[1 + h:1 + h + nb] - crh[1:1 + nb]).mean())
        base[f'btc_cum_m{h}'] = float((crb[1 + h:1 + h + nb] - crb[1:1 + nb]).mean())
    from numpy.lib.stride_tricks import sliding_window_view
    w = sliding_window_view(rh1[1:1 + POST_MIN + nb - 1], POST_MIN)
    base['hype_hit_up15'] = float((w.max(axis=1) > 0.005).mean())
    bvec = np.array([base[nm] for nm in names])
    boots = block_boot_cluster(M, valid // BLOCK1M)
    center = M.mean(axis=0)
    delta = boots - bvec
    idx = {nm: i for i, nm in enumerate(names)}
    post_keys = list(range(1, POST_MIN + 1))
    cum_keys = [5, 10, 15]
    # 与theta=0.5%的5m事件集的重叠：spike的1m收益落在事件窗口或其后5分钟内
    ev_lo = ev5_05 * 5 + 4
    ev_hi = ev5_05 * 5 + 13
    pos = np.searchsorted(ev_lo, valid, side='right') - 1
    in_ev = np.zeros(len(valid), dtype=bool)
    ok = pos >= 0
    in_ev[ok] = valid[ok] <= ev_hi[pos[ok]]
    return dict(threshold_1m=q, raw_events=int(len(raw)), events=int(len(valid)),
                overlap_with_5m_05_events=float(in_ev.mean()),
                same_minute=dict(hype_event=ci(boots[:, idx['hype_same_m1']], center[idx['hype_same_m1']]),
                                 hype_base=base['hype_same_m1'],
                                 btc_event_mean=float(center[idx['btc_same_m1']])),
                post_hype=dict(k_min=post_keys,
                               event_mean=ci(boots[:, [idx[f'hype_post_m{k}'] for k in post_keys]],
                                             center[[idx[f'hype_post_m{k}'] for k in post_keys]]),
                               base_mean=[base[f'hype_post_m{k}'] for k in post_keys],
                               diff=ci(delta[:, [idx[f'hype_post_m{k}'] for k in post_keys]],
                                       center[[idx[f'hype_post_m{k}'] for k in post_keys]] -
                                       bvec[[idx[f'hype_post_m{k}'] for k in post_keys]])),
                cum=dict(h_min=cum_keys,
                         hype_event=ci(boots[:, [idx[f'hype_cum_m{h}'] for h in cum_keys]],
                                       center[[idx[f'hype_cum_m{h}'] for h in cum_keys]]),
                         hype_base=[base[f'hype_cum_m{h}'] for h in cum_keys],
                         hype_diff=ci(delta[:, [idx[f'hype_cum_m{h}'] for h in cum_keys]],
                                      center[[idx[f'hype_cum_m{h}'] for h in cum_keys]] -
                                      bvec[[idx[f'hype_cum_m{h}'] for h in cum_keys]]),
                         btc_event=[float(center[idx[f'btc_cum_m{h}']]) for h in cum_keys]),
                hit15=dict(up_event=ci(boots[:, idx['hype_hit_up15']], center[idx['hype_hit_up15']]),
                           up_base=base['hype_hit_up15']))


def part_f(rb1, rh1):
    """1分钟互相关：corr(rb1[t], rh1[t+k])，k>0表示HYPE在BTC之后k分钟。描述性，无推断。"""
    q = float(np.quantile(rb1, 0.995))
    lags = list(range(-5, 6))

    def corr_set(idx):
        out = []
        for k in lags:
            if k >= 0:
                x, y = rb1[idx], rh1[idx + k]
            else:
                x, y = rb1[idx - k], rh1[idx]
            out.append(float(np.corrcoef(x, y)[0, 1]))
        return out

    n = len(rb1)
    all_idx = np.arange(5, n - 5)                             # 留±5分钟边界
    big_idx = all_idx[np.abs(rb1[all_idx]) > q]
    up_idx = all_idx[rb1[all_idx] > q]
    return dict(q995_1m=q, lags_min=lags,
                uncond=corr_set(all_idx), cond_abs=corr_set(big_idx), cond_up=corr_set(up_idx),
                n_cond_abs=int(len(big_idx)), n_cond_up=int(len(up_idx)))


def main():
    tb, bc, h_btc = load('BTC')
    th_, hc, h_hype = load('HYPE')
    assert np.array_equal(tb, th_) and np.all(np.diff(tb) == 60000)
    assert len(bc) % 5 == 0
    t5 = tb[::5]
    assert np.all(np.diff(t5) == 300000)
    b5, h5 = bc[4::5], hc[4::5]
    rb5, rh5 = np.log(b5[1:] / b5[:-1]), np.log(h5[1:] / h5[:-1])
    rb1, rh1 = np.log(bc[1:] / bc[:-1]), np.log(hc[1:] / hc[:-1])
    ev_raw = np.where(rb5 > 0.005)[0]
    ev5_05 = ev_raw[np.concatenate([[True], np.diff(ev_raw) >= 6])]
    ev5_05 = ev5_05[ev5_05 <= len(rb5) - 2 - H_MAX]
    result = dict(date='2026-10-05',
                  data_cutoff_ms=int(tb[-1] + 60000),
                  interval='1m（事件用聚合5m定义，与5分钟版对齐）',
                  source='binance-perp USDT永续',
                  n_bars_1m=int(len(bc)), n_bars_5m_agg=int(len(b5)),
                  sha256=dict(BTC=h_btc, HYPE=h_hype),
                  baseline_1m=dict(hype_mean=float(rh1.mean()), btc_mean=float(rb1.mean())),
                  pre_registered_primary=['theta=+0.5%事件后第1–5分钟逐分钟HYPE diff vs 基线、累计+5分钟diff',
                                          'theta=+0.8%事件后第1–15分钟逐分钟与累计diff vs 基线'],
                  part_D=[part_d(rb5, rb1, rh1, tb, t) for t in (0.004, 0.005, 0.008)],
                  part_E=part_e(rb1, rh1, tb, ev5_05),
                  part_F=part_f(rb1, rh1))
    out = BASE / '2026-10-05-BTC大涨后HYPE响应-1分钟-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    d5 = result['part_D'][1]
    print('D theta=0.5%%: events=%d/%d, 事件窗口HYPE均值=%+.4f%% (5m版同口径+0.845%%)' %
          (d5['events'], d5['raw_events'], d5['event_bar_hype_mean'] * 100))
    print('  事件窗口内HYPE逐分钟%% (基线%%) 与BTC逐分钟%%:')
    for j in range(5):
        e = d5['intra_hype']['event_mean']['estimate'][j] * 100
        b = d5['intra_hype']['base_mean'][j] * 100
        d = d5['intra_hype']['diff']['estimate'][j] * 100
        lo, hi = d5['intra_hype']['diff']['ci95_lo'][j] * 100, d5['intra_hype']['diff']['ci95_hi'][j] * 100
        bb = d5['intra_btc']['event_mean'][j] * 100
        print('    窗内第%d分钟  HYPE %+8.4f (%+8.5f)  diff %+8.4f [%+8.4f,%+8.4f]   BTC %+8.4f' %
              (j + 1, e, b, d, lo, hi, bb))
    print('  事件后HYPE逐分钟diff%% (前10分钟):')
    for k in range(10):
        d = d5['post_hype']['diff']['estimate'][k] * 100
        lo, hi = d5['post_hype']['diff']['ci95_lo'][k] * 100, d5['post_hype']['diff']['ci95_hi'][k] * 100
        print('    +%2dmin  %+.4f [%+.4f,%+.4f]' % (k + 1, d, lo, hi))
    print('  cum diff%% (+5/10/15/30/60):', [round(x * 100, 4) for x in d5['cum']['hype_diff']['estimate']],
          '超beta1m:', [round(x * 100, 4) for x in d5['excess_over_beta1m']])
    d8 = result['part_D'][2]
    print('D theta=0.8%%: events=%d, cum diff%% (+5/10/15):' % d8['events'],
          [round(x * 100, 4) for x in d8['cum']['hype_diff']['estimate'][:3]])
    print('  0.8%%组后15分钟逐分钟diff%%:', [round(x * 100, 4) for x in d8['post_hype']['diff']['estimate']])
    e = result['part_E']
    print('E 1m spike: q99.5=%+.4f%%, events=%d, 与5m事件重叠=%.1f%%' %
          (e['threshold_1m'] * 100, e['events'], e['overlap_with_5m_05_events'] * 100))
    print('  同分钟HYPE %+.4f%% (基线%+.5f%%), cum+5/15 diff%%:' %
          (e['same_minute']['hype_event']['estimate'][0] * 100, e['same_minute']['hype_base'] * 100),
          [round(x * 100, 4) for x in e['cum']['hype_diff']['estimate']])
    f = result['part_F']
    print('F 1m互相关 lags -3..+3: uncond', [round(x, 3) for x in f['uncond'][2:9]],
          '|cond_abs', [round(x, 3) for x in f['cond_abs'][2:9]])


if __name__ == '__main__':
    main()
