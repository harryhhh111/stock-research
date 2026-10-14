"""策略检验：BTC上涨时 空BTC+多SOL 的pair效果。

用户策略：BTC 明显上涨时，做空 BTC、做多 SOL（吃 SOL 的放大跟随）。
关键问题：进场在事件bar收盘（信号可观察时点），SOL 已在同一根bar内完成跟随
（beta≈1.23、99%命中、秒级同步），pair 的后续盈亏取决于进场后的漂移。

本脚本度量（全年1m/5m数据，与事件研究同口径）：
- 事件：BTC 5m>+0.5%（451次）与 1m>+0.25%（2062次），30分钟去簇；
- 进场：事件bar收盘；持有15/30/60分钟；
- P&L（log近似，单位=单腿名义）：
  V1 等名义: rSOL_fwd − rBTC_fwd
  V2 beta对冲(1.23): 1.23·rSOL_fwd − rBTC_fwd
- 报均值/中位/胜率/块聚类bootstrap CI，与无条件基线对比；
- 年度背景：BTC/SOL/SOL-BTC全年累计（趋势是pair要对抗的头寸风险）；
- 成本基准：Binance taker 0.05%/腿 → 单次往返约0.10%（单腿名义计），未含滑点与资金费。
纯描述，非完整回测（无订单簿冲击、无资金费、无保证金细节）。
"""
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m

BASE = Path(__file__).resolve().parent
REPS = 20000
RNG = np.random.default_rng(20261008)
BETA_SOL = 1.23


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


def pair_stats(rb, rs, theta, interval_min, hold_bars_list):
    n = len(rb)
    raw = np.where(rb > theta)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 30])]
    H = max(hold_bars_list)
    valid = keep[(keep >= 1) & (keep <= n - 2 - H)]
    blk_per_day = 1440 // interval_min
    base_idx = np.arange(1, n - H)
    out = {}
    for h in hold_bars_list:
        fS = np.array([rs[v + 1:v + 1 + h].sum() for v in valid])
        fB = np.array([rb[v + 1:v + 1 + h].sum() for v in valid])
        p1 = fS - fB
        p2 = BETA_SOL * fS - fB
        bS = np.array([rs[b + 1:b + 1 + h].sum() for b in base_idx])
        bB = np.array([rb[b + 1:b + 1 + h].sum() for b in base_idx])
        q1, q2 = bS - bB, BETA_SOL * bS - bB
        M = np.column_stack([p1, p2])
        boots = block_boot(M, valid // blk_per_day)
        out[f'hold_{h}bar_{h * interval_min}min'] = dict(
            events=int(len(valid)),
            v1_equal_notional=ci(boots[:, 0], p1.mean()),
            v1_median=float(np.median(p1)), v1_win=float((p1 > 0).mean()),
            v1_base=float(q1.mean()),
            v2_beta_hedged=ci(boots[:, 1], p2.mean()),
            v2_median=float(np.median(p2)), v2_win=float((p2 > 0).mean()),
            v2_base=float(q2.mean()))
    return out


def main():
    cb, cs = load_k('BTC'), load_k('SOL')
    rb1 = np.log(cb[1:] / cb[:-1])
    rs1 = np.log(cs[1:] / cs[:-1])
    b5 = cb.reshape(-1, 5)
    s5 = cs.reshape(-1, 5)
    rb5 = np.log(b5[:, -1][1:] / b5[:, -1][:-1])
    rs5 = np.log(s5[:, -1][1:] / s5[:, -1][:-1])

    year = dict(btc_log_ret=float(np.log(cb[-1] / cb[0])),
                sol_log_ret=float(np.log(cs[-1] / cs[0])),
                sol_minus_btc=float(np.log(cs[-1] / cs[0]) - np.log(cb[-1] / cb[0])))

    res = dict(date='2026-10-08', strategy='BTC上涨时 空BTC+多SOL', year_background=year,
               trigger_5m_05pct=pair_stats(rb5, rs5, 0.005, 5, (3, 6, 12)),
               trigger_1m_025pct=pair_stats(rb1, rs1, 0.0025, 1, (15, 30, 60)))
    out = BASE / '2026-10-08-pair策略空BTC多SOL-结果.json'
    out.write_text(json.dumps(res, ensure_ascii=False, indent=2) + '\n')
    print('全年背景: BTC %+.1f%%  SOL %+.1f%%  SOL-BTC %+.1f%%（这个pair要对抗的年度趋势）' % (
        year['btc_log_ret'] * 100, year['sol_log_ret'] * 100, year['sol_minus_btc'] * 100))
    for name, block in (('5m>+0.5%', res['trigger_5m_05pct']), ('1m>+0.25%', res['trigger_1m_025pct'])):
        for hk, d in block.items():
            v1, v2 = d['v1_equal_notional'], d['v2_beta_hedged']
            print('%s %s: n=%d' % (name, hk, d['events']))
            print('  V1等名义: 均值%+.4f%% [%+.4f,%+.4f] 中位%+.4f%% 胜率%.0f%% (基线%+.4f%%)' % (
                v1['estimate'][0] * 100, v1['ci95_lo'][0] * 100, v1['ci95_hi'][0] * 100,
                d['v1_median'] * 100, d['v1_win'] * 100, d['v1_base'] * 100))
            print('  V2 beta对冲: 均值%+.4f%% [%+.4f,%+.4f] 中位%+.4f%% 胜率%.0f%% (基线%+.4f%%)' % (
                v2['estimate'][0] * 100, v2['ci95_lo'][0] * 100, v2['ci95_hi'][0] * 100,
                d['v2_median'] * 100, d['v2_win'] * 100, d['v2_base'] * 100))


if __name__ == '__main__':
    main()
