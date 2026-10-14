"""pair策略资金费净收益：把毛边缘扣掉资金费，出净边缘。

数据：数字资产/factcheck 归档的 Binance 资金费全年（2025-10-04~2026-10-04 北京窗，
BTC/HYPE/ETH/SOL，同步与核对见 数字资产/factcheck/runs/funding-*.json）。
毛边缘取自 2026-10-08-pair盈亏归因-HYPE-BTC-结果.json（常驻等名义 +94.2%/年；
事件驱动 BTC 5m<-0.5% 后持有，n=389，15m/1h/4h）。

符号约定：fundingRate>0 = 多头付空头。多HYPE空BTC每事件净资金费 = rate_BTC − rate_HYPE
（每腿单位名义，等名义口径；beta对冲版空β份BTC：β×rate_BTC − rate_HYPE）。

三部分：
1. 各币资金费年度画像（Σrate=单边腿一年资金费合计/名义，正值=多头净付）。
2. 常驻pair：扣全年资金费 → 净边缘（等名义与beta对冲两版）。
3. 事件驱动pair：按时间戳把每个持有窗口内实际发生的资金费逐事件扣除，
   得 15m/1h/4h 扣费后净均值，再叠加三档往返成本。
"""
import datetime as dt
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m


def iso_bj(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone(dt.timedelta(hours=8))).isoformat()

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
FUND = ROOT / '数字资产' / 'factcheck' / 'data' / 'normalized' / 'binance-perp' / 'funding'
ATTR = json.loads((BASE / '2026-10-08-pair盈亏归因-HYPE-BTC-结果.json').read_bytes())
N_DAYS = (1791051300000 - 1759515300000) / 86400000
WINDOW = f'{1759515300000}-{1791051300000}'
HOLD_SET = (3, 12, 48)


def load_funding(tok):
    doc = json.loads((FUND / tok / f'{WINDOW}.json').read_bytes())
    t = np.array([e['funding_time_ms'] for e in doc['events']], dtype=np.int64)
    r = np.array([e['funding_rate'] for e in doc['events']])
    return t, r


def profile(tok):
    t, r = load_funding(tok)
    months = {}
    for tt, rr in zip(t, r):
        key = iso_bj(tt)[:7]
        months.setdefault(key, 0.0)
        months[key] += rr
    return dict(token=tok, n=int(len(r)), sum_rate_pct=float(r.sum() * 100),
                annualized_pct=float(r.sum() / N_DAYS * 365 * 100),
                mean_per_event_pct=float(r.mean() * 100),
                max_pct=float(r.max() * 100), min_pct=float(r.min() * 100),
                pos_share=float((r > 0).mean()),
                monthly_sum_pct={k: round(v * 100, 3) for k, v in sorted(months.items())})


def window_funding(t_b, r_b, t_h, r_h, entries_ms, hold_bars, beta=None):
    """每个事件窗口 [entry, entry+hold*5min) 内的资金费合计（rate_BTC−rate_HYPE，beta版乘β）。"""
    span = hold_bars * 5 * 60000
    out = np.empty(len(entries_ms))
    bmul = 1.0 if beta is None else beta
    for i, e in enumerate(entries_ms):
        lo = np.searchsorted(t_b, e)
        hi = np.searchsorted(t_b, e + span)
        lo2 = np.searchsorted(t_h, e)
        hi2 = np.searchsorted(t_h, e + span)
        out[i] = bmul * r_b[lo:hi].sum() - r_h[lo2:hi2].sum()
    return out


def main():
    # 1) 各币画像
    profs = {tok: profile(tok) for tok in ('BTC', 'HYPE', 'ETH', 'SOL')}
    print('== 各币资金费画像（全年，单边腿名义）==')
    for tok, p in profs.items():
        print('  %s: n=%d Σ=%.2f%% 年化%.2f%% 单次均%.4f%% 正占比%.0f%% [max %.3f%% min %.3f%%]' % (
            tok, p['n'], p['sum_rate_pct'], p['annualized_pct'], p['mean_per_event_pct'],
            p['pos_share'] * 100, p['max_pct'], p['min_pct']))

    # 2) 常驻pair净边缘（contrib=pair净收资金费=Σrate_BTC−Σrate_HYPE，正=收、负=付）
    gross = ATTR['standing']['total_pct']                   # +94.2%
    beta = ATTR['event_driven']['beta']                     # 1.2205
    contrib_eq = profs['BTC']['sum_rate_pct'] - profs['HYPE']['sum_rate_pct']
    contrib_bh = beta * profs['BTC']['sum_rate_pct'] - profs['HYPE']['sum_rate_pct']
    standing = dict(
        gross_pct=gross, beta=beta,
        funding_contrib_equal_pct=contrib_eq, funding_contrib_beta_pct=contrib_bh,
        net_equal_pct=gross + contrib_eq, net_beta_pct=gross + contrib_bh,
        note='contrib=Σrate_BTC−Σrate_HYPE（等名义）或 β×Σrate_BTC−Σrate_HYPE（beta对冲）；'
             '正=pair净收资金费，负=净付。HYPE全年Σ(5.76%)>BTC(3.34%)，多HYPE腿是净付方')
    print('== 常驻pair ==')
    print('  毛 %+.2f%%/年；资金费贡献 等名义 %+.2f%%（净 %+0.1f%%） | beta对冲 %+.2f%%（净 %+0.1f%%）' % (
        gross, contrib_eq, standing['net_equal_pct'], contrib_bh, standing['net_beta_pct']))

    # 3) 事件驱动pair：逐事件窗口扣资金费
    t1m, cb = m.load_klines('BTC')[0], m.load_klines('BTC')[1]
    ch = m.load_klines('HYPE')[1]
    b5 = cb.reshape(-1, 5)
    rb5 = np.log(b5[:, -1][1:] / b5[:, -1][:-1])
    raw = np.where(rb5 < -0.005)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 6])]
    valid = keep[keep <= len(rb5) - 2 - 200]
    entries_ms = t1m[(valid + 1) * 5]                       # 事件bar次一根的开盘时刻=进场时刻
    t_fb, r_fb = load_funding('BTC')
    t_fh, r_fh = load_funding('HYPE')
    n_events = int(len(valid))
    assert n_events == ATTR['event_driven']['events'], (n_events, ATTR['event_driven']['events'])
    ev = {}
    print('== 事件驱动pair（n=%d，窗口内实际资金费）==' % n_events)
    for hold in HOLD_SET:
        gross_eq = ATTR['event_driven']['by_horizon'][str(hold)]['equal_mean'] * 100
        gross_bh = ATTR['event_driven']['by_horizon'][str(hold)]['beta_mean'] * 100
        f_eq = window_funding(t_fb, r_fb, t_fh, r_fh, entries_ms, hold) * 100
        f_bh = window_funding(t_fb, r_fb, t_fh, r_fh, entries_ms, hold, beta=beta) * 100
        key = f'{hold * 5}min'
        ev[key] = dict(
            gross_equal_pct=gross_eq, gross_beta_pct=gross_bh,
            funding_mean_equal_pct=float(f_eq.mean()),
            funding_mean_beta_pct=float(f_bh.mean()),
            funding_med_equal_pct=float(np.median(f_eq)),
            funding_p90_abs_equal_pct=float(np.percentile(np.abs(f_eq), 90)),
            net_equal_pct=gross_eq + f_eq.mean(),
            net_beta_pct=gross_bh + f_bh.mean())
        print('  %s: 毛 等%.3f%%/β%.3f%% +资金费贡献 等%+.4f%%/β%+.4f%% = 净 等%+.3f%%/β%+.3f%%' % (
            key, gross_eq, gross_bh, f_eq.mean(), f_bh.mean(),
            ev[key]['net_equal_pct'], ev[key]['net_beta_pct']))
    # 扣费后再扣三档往返成本（4h beta版）
    h4 = ev['240min']
    for c in (0.1, 0.2, 0.3):
        k = f'rt_{c:.1f}pct'
        net_after_cost = h4['net_beta_pct'] - c
        ev.setdefault('cost_scenarios', {})[k] = dict(
            net_per_event_pct=net_after_cost,
            naive_annual_pct=net_after_cost * n_events)
    print('  4h beta版扣费+成本：' + ' | '.join(
        '%s %+.3f%%/事件 →年化%+0.0f%%' % (k, v['net_per_event_pct'], v['naive_annual_pct'])
        for k, v in ev['cost_scenarios'].items()))

    result = dict(date='2026-10-09', window='2025-10-04~2026-10-04 北京',
                  funding_source='数字资产/factcheck/data/normalized/binance-perp/funding/',
                  profiles=profs, standing=standing, event_driven=ev, n_events=n_events)
    out = BASE / '2026-10-09-pair资金费净收益-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('已写出', out.name)


if __name__ == '__main__':
    main()
