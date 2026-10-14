"""BTC明显上涨后HYPE的分钟级响应：事件研究。

数据：数字资产/factcheck 归档的 Binance USDT本位永续5分钟K线（BTC、HYPE各105,120根，
时间完全对齐，核对见 数字资产/factcheck/2026-10-04-一年5分钟K线核对.json）。

三部分：
A. 单根大阳线冲击（5分钟收益>阈值），看HYPE之后逐根与累计响应，是否显著高于无条件基线；
B. 涨势启动事件（滚动1小时收益穿越阈值且此前3小时未达），看HYPE跟随时间；
C. 大波动条件下的互相关（10-2线性扫描的全年、条件化版本）。

推断：A用288根(≈24小时)事件块聚类bootstrap（事件成簇、波动率状态持续）；
B事件天然间隔>=24小时，直接对事件重采样。基线在全部样本上计算，其抽样误差远小于
条件均值，bootstrap只对条件部分变动（报告注明）。主要终点事前设定：theta=0.5%冲击后
15/30/60分钟累计响应；其余为敏感性或探索性。
"""
import hashlib
import json
import math
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
DATA = ROOT / '数字资产' / 'factcheck' / 'data' / 'normalized' / 'binance-perp' / '5m'
H_MAX = 12          # 主要向前看60分钟
BLOCK = 288         # 聚类bootstrap块长（288根5分钟≈24小时）
REPS = 20000
RNG = np.random.default_rng(20261005)

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

def boot_events(rows, reps=REPS):
    draws = RNG.integers(0, len(rows), size=(reps, len(rows)))
    return rows[draws].mean(axis=1)

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

def part_a(rb, rh, theta):
    """单根冲击：rb/rh为收盘对收盘5分钟log收益（长度n-1），事件=rb[i]>theta。"""
    n = len(rb)
    raw = np.where(rb > theta)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 6])]          # 30分钟去簇，取首个
    valid = keep[keep <= n - 2 - H_MAX]
    base_valid = np.arange(0, n - H_MAX)
    # 指标：同根HYPE；逐根HYPE k=1..12；累计HYPE h=1..12；累计BTC h=1..12
    def cum(ret, idx, h):
        return np.array([ret[i + 1:i + 1 + h].sum() for i in idx])
    same = rh[valid]
    per_bar = np.column_stack([rh[valid + k] for k in range(1, H_MAX + 1)])
    cum_h = np.column_stack([cum(rh, valid, h) for h in range(1, H_MAX + 1)])
    cum_b = np.column_stack([cum(rb, valid, h) for h in range(1, H_MAX + 1)])
    base_cum_h = np.column_stack([cum(rh, base_valid, h) for h in range(1, H_MAX + 1)])
    # HYPE“也明显上涨”：未来h根内单根收益曾>0.5%；绝对命中作波动率机械效应对照
    hit = np.column_stack([(np.maximum.reduce([rh[valid + k] for k in range(1, h + 1)]) > 0.005)
                           for h in (3, 6, 12)])
    hit_abs = np.column_stack([(np.maximum.reduce([np.abs(rh[valid + k]) for k in range(1, h + 1)]) > 0.005)
                               for h in (3, 6, 12)])
    hit_base = np.column_stack([(np.maximum.reduce([rh[base_valid + k] for k in range(1, h + 1)]) > 0.005)
                                for h in (3, 6, 12)])
    hit_abs_base = np.column_stack([(np.maximum.reduce([np.abs(rh[base_valid + k]) for k in range(1, h + 1)]) > 0.005)
                                    for h in (3, 6, 12)])
    metrics = np.column_stack([same, per_bar, cum_h, hit.astype(float), hit_abs.astype(float)])
    boots = block_boot_cluster(metrics, valid // BLOCK)
    base_center = np.concatenate([[rh[base_valid].mean()], [rh[base_valid].mean()] * H_MAX,
                                  base_cum_h.mean(axis=0), hit_base.mean(axis=0),
                                  hit_abs_base.mean(axis=0)])
    center = metrics.mean(axis=0)
    p_end, c_end = 1 + H_MAX, 1 + 2 * H_MAX          # same|per_bar|cum_h|hit|hit_abs 列边界
    a_end = c_end + 3
    delta = boots - base_center
    beta5 = float(np.cov(rb, rh, ddof=1)[0, 1] / np.var(rb, ddof=1))
    excess = (cum_h.mean(axis=0) - base_cum_h.mean(axis=0)) - beta5 * cum_b.mean(axis=0)
    return dict(
        theta=theta, raw_events=int(len(raw)), events=int(len(valid)),
        same_bar_hype_mean=float(same.mean()),
        same_bar_base_mean=float(rh[base_valid].mean()),
        per_bar=dict(h5_min=[k * 5 for k in range(1, H_MAX + 1)],
                     event_mean=ci(boots[:, 1:p_end], center[1:p_end]),
                     diff_vs_base=ci(delta[:, 1:p_end], center[1:p_end] - base_center[1:p_end])),
        cum=dict(h_min=[h * 5 for h in range(1, H_MAX + 1)],
                 event_mean=ci(boots[:, p_end:c_end], center[p_end:c_end]),
                 base_mean=[float(x) for x in base_cum_h.mean(axis=0)],
                 diff_vs_base=ci(delta[:, p_end:c_end], center[p_end:c_end] - base_center[p_end:c_end])),
        cum_btc_event_mean=[float(x) for x in cum_b.mean(axis=0)],
        excess_over_beta5=[float(x) for x in excess], beta5=beta5,
        hit_prob=dict(horizon_min=[15, 30, 60],
                      event=ci(boots[:, c_end:a_end], center[c_end:a_end]),
                      base=[float(x) for x in hit_base.mean(axis=0)],
                      diff=ci(delta[:, c_end:a_end], center[c_end:a_end] - base_center[c_end:a_end])),
        hit_prob_abs=dict(horizon_min=[15, 30, 60],
                          event=ci(boots[:, a_end:], center[a_end:]),
                          base=[float(x) for x in hit_abs_base.mean(axis=0)],
                          diff=ci(delta[:, a_end:], center[a_end:] - base_center[a_end:])),
    )

def part_a_down(rb, rh, theta):
    """对称性：大跌事件后HYPE的响应（带符号），并与上涨事件同口径对照。"""
    n = len(rb)
    raw = np.where(rb < -theta)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 6])]
    valid = keep[keep <= n - 2 - H_MAX]
    base_valid = np.arange(0, n - H_MAX)
    def cum(ret, idx, h):
        return np.array([ret[i + 1:i + 1 + h].sum() for i in idx])
    same = rh[valid]
    per_bar = np.column_stack([rh[valid + k] for k in range(1, H_MAX + 1)])
    cum_h = np.column_stack([cum(rh, valid, h) for h in range(1, H_MAX + 1)])
    cum_b = np.column_stack([cum(rb, valid, h) for h in range(1, H_MAX + 1)])
    base_cum_h = np.column_stack([cum(rh, base_valid, h) for h in range(1, H_MAX + 1)])
    base_per = rh[base_valid]
    # 方向命中：未来h根内出现 < -0.5% 的单根；绝对命中：|单根| > 0.5%（检验波动率机械效应）
    hit_dn = np.column_stack([(np.minimum.reduce([rh[valid + k] for k in range(1, h + 1)]) < -0.005)
                              for h in (3, 6, 12)])
    hit_abs = np.column_stack([(np.maximum.reduce([np.abs(rh[valid + k]) for k in range(1, h + 1)]) > 0.005)
                               for h in (3, 6, 12)])
    hit_abs_base = np.column_stack([(np.maximum.reduce([np.abs(rh[base_valid + k]) for k in range(1, h + 1)]) > 0.005)
                                    for h in (3, 6, 12)])
    metrics = np.column_stack([same, per_bar, cum_h, hit_dn.astype(float), hit_abs.astype(float)])
    boots = block_boot_cluster(metrics, valid // BLOCK)
    center = metrics.mean(axis=0)
    base_center = np.concatenate([[base_per.mean()], [base_per.mean()] * H_MAX,
                                  base_cum_h.mean(axis=0), [0, 0, 0], hit_abs_base.mean(axis=0)])
    delta = boots - base_center
    p_end, c_end = 1 + H_MAX, 1 + 2 * H_MAX
    a_end = c_end + 3
    beta5 = float(np.cov(rb, rh, ddof=1)[0, 1] / np.var(rb, ddof=1))
    excess = (cum_h.mean(axis=0) - base_cum_h.mean(axis=0)) - beta5 * cum_b.mean(axis=0)
    return dict(theta=-theta, events=int(len(valid)), same_bar_hype_mean=float(same.mean()),
                per_bar=dict(h5_min=[k * 5 for k in range(1, H_MAX + 1)],
                             diff_vs_base=ci(delta[:, 1:p_end], center[1:p_end] - base_center[1:p_end])),
                cum=dict(h_min=[h * 5 for h in range(1, H_MAX + 1)],
                         event_mean=ci(boots[:, p_end:c_end], center[p_end:c_end]),
                         diff_vs_base=ci(delta[:, p_end:c_end], center[p_end:c_end] - base_center[p_end:c_end])),
                cum_btc_event_mean=[float(x) for x in cum_b.mean(axis=0)],
                excess_over_beta5=[float(x) for x in excess], beta5=beta5,
                hit_prob_down=dict(horizon_min=[15, 30, 60], event=ci(boots[:, c_end:a_end], center[c_end:a_end])),
                hit_prob_abs=dict(horizon_min=[15, 30, 60], event=ci(boots[:, a_end:], center[a_end:]),
                                  base=[float(x) for x in hit_abs_base.mean(axis=0)],
                                  diff=ci(delta[:, a_end:], center[a_end:] - base_center[a_end:])))

def wilson(k, n, z=1.959964):
    """Wilson score interval for a binomial proportion (bootstrap分布在n小时退化)。"""
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    half = z / d * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [float(center - half), float(center + half)]

def part_b(bc, hc, th=0.02, cool=288):
    """涨势启动：滚动1小时BTC收益在c处>=th，前36根均<th，距上一事件>=cool根。"""
    e = np.log(bc[12:] / bc[:-12])                    # e[j] 对应收盘下标 j+12
    e_idx = np.arange(12, len(bc))
    ok = e >= th
    fresh = np.ones(len(e), dtype=bool)
    for k in range(1, 37):
        fresh[k:] &= ~ok[:-k] if k <= 36 else True
    cand = np.where(ok & fresh)[0]
    events = []
    for j in cand:
        if not events or j - events[-1] >= cool:
            events.append(int(j))
    events = np.array(events)
    fwd_need = 24
    events = events[events + 12 + fwd_need < len(hc)]  # 需完整向前24根+1小时窗
    eh = np.log(hc[12:] / hc[:-12])                    # HYPE滚动1小时收益，下标j对应收盘j+12
    from numpy.lib.stride_tricks import sliding_window_view
    any_win = sliding_window_view(eh, 13).max(axis=1) >= th   # any_win[j]=eh[j..j+12]是否有>=th
    def fwd_cum(px, c, h):
        return np.log(px[c + h] / px[c])
    cum_h = np.column_stack([fwd_cum(hc, events + 12, h) for h in (3, 6, 12, 24)])
    cum_b = np.column_stack([fwd_cum(bc, events + 12, h) for h in (3, 6, 12, 24)])
    end = events + 12                                 # 事件收盘下标
    reach60 = eh[end] >= th                            # +60分钟时点的1小时滚动收益>=th
    reach120 = any_win[end]                            # +60至+120分钟内1小时滚动收益曾>=th
    # 首次到达时间（根，5分钟/根），未达记None
    first = []
    for k, c in enumerate(end):
        hit_idx = np.where(eh[c:c + 13] >= th)[0]
        first.append(int(hit_idx[0]) + 12 if len(hit_idx) else None)
    # 基线：全部有效收盘下标（与事件同定义、同窗口）
    allc = np.arange(12, len(bc) - 12 - fwd_need)
    base60 = float((eh[allc] >= th).mean())
    base120 = float(any_win[allc].mean())
    boots = boot_events(np.column_stack([cum_h, reach60.astype(float), reach120.astype(float)]))
    center = np.column_stack([cum_h, reach60, reach120]).astype(float).mean(axis=0)
    beta1h = 1.2597                                   # 全年1小时收益beta，见配对研究报告
    return dict(th=th, events=int(len(events)),
                event_close_idx=[int(x) for x in end],
                cum=dict(horizon_min=[15, 30, 60, 120],
                         hype_event_mean=ci(boots[:, :4], center[:4]),
                         btc_event_mean=[float(x) for x in cum_b.mean(axis=0)],
                         excess_over_beta1h=[float(x) for x in
                                             cum_h.mean(axis=0) - beta1h * cum_b.mean(axis=0)]),
                reach=dict(reach60_min_prob=ci(boots[:, 4], center[4]), base60=base60,
                           reach60_wilson95=wilson(int(reach60.sum()), int(len(reach60))),
                           reach120_min_prob=ci(boots[:, 5], center[5]), base120=base120,
                           reach120_wilson95=wilson(int(reach120.sum()), int(len(reach120)))),
                time_to_reach_bars=[f for f in first if f is not None],
                unreached=int(sum(f is None for f in first)))

def part_c(rb, rh, theta):
    """条件互相关：事件根rb[i]与未来第k根rh[i+k]的Pearson相关，对照无条件。"""
    n = len(rb)
    raw = np.where(np.abs(rb) > theta)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 6])]
    valid = keep[keep <= n - 2 - H_MAX]
    ks = range(0, H_MAX + 1)
    def corr_set(idx):
        out = []
        for k in ks:
            x, y = rb[idx], rh[idx + k]
            out.append(float(np.corrcoef(x, y)[0, 1]))
        return out
    all_idx = np.arange(0, n - H_MAX)
    return dict(theta=theta, events=int(len(valid)),
                conditioned_k0_to_12=corr_set(valid), uncond_k0_to_12=corr_set(all_idx))

def main():
    tb, bc, h_btc = load('BTC')
    th_, hc, h_hype = load('HYPE')
    assert np.array_equal(tb, th_) and np.all(np.diff(tb) == 300000)
    rb = np.log(bc[1:] / bc[:-1])
    rh = np.log(hc[1:] / hc[:-1])
    result = dict(date='2026-10-05',
                  data_cutoff_ms=int(tb[-1] + 300000),
                  interval='5m', source='binance-perp USDT永续',
                  n_bars=int(len(bc)), n_returns=int(len(rb)),
                  sha256=dict(BTC=h_btc, HYPE=h_hype),
                  pre_registered_primary='theta=+0.5%冲击后15/30/60分钟HYPE累计响应 vs 无条件基线',
                  part_A=[part_a(rb, rh, t) for t in (0.004, 0.005, 0.008)],
                  part_A_down=part_a_down(rb, rh, 0.005),
                  part_B=[part_b(bc, hc, t) for t in (0.02, 0.03)],
                  part_C=part_c(rb, rh, 0.005))
    out = BASE / '2026-10-05-BTC大涨后HYPE响应-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    a5 = result['part_A'][1]
    print('A theta=0.5%%: events=%d/%d, same-bar HYPE mean=%+.4f%%' %
          (a5['events'], a5['raw_events'], a5['same_bar_hype_mean'] * 100))
    print('  cum event %% / diff %% (15/30/60min):')
    for i, m in zip((2, 5, 11), (15, 30, 60)):
        e = a5['cum']['event_mean']; d = a5['cum']['diff_vs_base']
        print('    %3dmin  %+.4f [%+.4f,%+.4f]   diff %+.4f [%+.4f,%+.4f]' %
              (m, e['estimate'][i] * 100, e['ci95_lo'][i] * 100, e['ci95_hi'][i] * 100,
               d['estimate'][i] * 100, d['ci95_lo'][i] * 100, d['ci95_hi'][i] * 100))
    print('  hit up (15/30/60):', [round(x, 4) for x in a5['hit_prob']['event']['estimate']],
          'base:', [round(x, 4) for x in a5['hit_prob']['base']])
    print('  hit abs (15/30/60):', [round(x, 4) for x in a5['hit_prob_abs']['event']['estimate']],
          'base:', [round(x, 4) for x in a5['hit_prob_abs']['base']])
    print('  per-bar diff %% k=1..6:', [round(x * 100, 4) for x in a5['per_bar']['diff_vs_base']['estimate'][:6]])
    d = result['part_A_down']
    print('A down theta=0.5%%: events=%d, same-bar HYPE mean=%+.4f%%' % (d['events'], d['same_bar_hype_mean'] * 100))
    print('  down cum event%% (15/30/60):', [round(x * 100, 3) for x in
          (np.array(d['cum']['event_mean']['estimate'])[[2, 5, 11]]).tolist()],
          'diff:', [round(x * 100, 3) for x in
          (np.array(d['cum']['diff_vs_base']['estimate'])[[2, 5, 11]]).tolist()])
    print('  down hit%% (15/30/60):', [round(x, 4) for x in d['hit_prob_down']['event']['estimate']],
          'abs:', [round(x, 4) for x in d['hit_prob_abs']['event']['estimate']],
          'abs base:', [round(x, 4) for x in d['hit_prob_abs']['base']])
    print('  down per-bar diff%% k=1..6:', [round(x * 100, 4) for x in d['per_bar']['diff_vs_base']['estimate'][:6]])
    for pb in result['part_B']:
        r = pb['reach']
        print('B th=%.0f%%: events=%d, reach60 %d/%d Wilson%s (base %.4f), reach120 %d/%d Wilson%s (base %.4f)' %
              (pb['th'] * 100, pb['events'],
               round(r['reach60_min_prob']['estimate'][0] * pb['events']), pb['events'],
               r['reach60_wilson95'], r['base60'],
               round(r['reach120_min_prob']['estimate'][0] * pb['events']), pb['events'],
               r['reach120_wilson95'], r['base120']))
    c = result['part_C']
    print('C cond corr k0..6:', [round(x, 3) for x in c['conditioned_k0_to_12'][:7]])
    print('C uncond corr k0..6:', [round(x, 3) for x in c['uncond_k0_to_12'][:7]])

if __name__ == '__main__':
    main()
