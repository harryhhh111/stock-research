"""2026年8月中旬行情案例：BTC上涨→放量→HYPE跟涨的传导窗口（秒级，描述性案例研究）。

数据：aggTrades 1秒网格（复用 leadlag_btc_hype_1s 的装载与网格函数）。
 episode = 2026-08-18T00:00Z .. 2026-08-26T00:00Z（同步日志中两币成交量放大2-4倍的一周）。

输出：
1. 那一周日度OHLC+量表（两币，方向与大小）；
2. BTC上行段（rolling 30分钟收益>+1%，去簇）逐段：BTC/HYPE各自的到达时间τ(25/50/75%)、
   量升时刻τ_V（60秒滚动量首次≥3倍前24小时基线中位）、窗口分解：
   价→量 τ_V−τ_B(25%)、量→价 τ_H(25%)−τ_V、HYPE启动滞后 τ_H(25%)−τ_B(25%)、
   HYPE完成滞后 τ_H(75%)−τ_B(75%)、两币各自段持续时长；
3. 段级错位扫描：HYPE窗口整体平移δ∈[-30,+30]分钟找最大响应，描述性；
4. episode内 vs 外：theta=+0.25%事件分钟Δ(50%)分布对比、大秒脉冲同秒占比对比。

n小（个位数上行段），全部为描述性统计，不做显著性推断。
"""
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m

BASE = Path(__file__).resolve().parent
EP0 = 1787000000          # 约2026-08-18T00:00Z，代码内精确计算
EP1 = 1787700000          # 约2026-08-26T00:00Z
EP0 = int(__import__('datetime').datetime(2026, 8, 18, tzinfo=__import__('datetime').timezone.utc).timestamp())
EP1 = int(__import__('datetime').datetime(2026, 8, 26, tzinfo=__import__('datetime').timezone.utc).timestamp())
LEG = 1800                # 上行段窗口：30分钟
RTH = 0.01                # rolling 30min收益阈值


def cross(p_ff, lo, hi, total):
    cs = np.cumsum(np.log(p_ff[lo:hi + 1] / p_ff[lo - 1]))
    out = []
    for f in (0.25, 0.5, 0.75):
        hit = np.where(cs >= f * total)[0]
        out.append(int(hit[0]) if len(hit) else None)
    return out


def daily_table(t_ms, price, qty, p_ff):
    rows = []
    for d in range(m.S0, m.S1, 86400):
        sel = (t_ms >= d * 1000) & (t_ms < (d + 86400) * 1000)
        if not sel.any():
            continue
        sec0, sec1 = d - m.S0, d - m.S0 + 86400
        if EP0 <= d < EP1 or (d - 86400 >= EP0 and d - 86400 < EP1):
            rows.append(dict(date=__import__('datetime').datetime.fromtimestamp(d, __import__('datetime').timezone.utc).date().isoformat(),
                             in_episode=bool(EP0 <= d < EP1),
                             open=float(price[sel][0]), high=float(price[sel].max()),
                             low=float(price[sel].min()), close=float(price[sel][-1]),
                             volume=float(qty[sel].sum()), n_trades=int(sel.sum())))
    return rows


def find_legs(p_ff):
    """episode内 rolling30min BTC收益阈值以上的簇，取每簇最大点，返回峰值秒下标与窗口。"""
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
    out = []
    for _, s in legs:
        w0, w1 = s - LEG, s
        tot_b = float(np.log(p_ff[w1] / p_ff[w0 - 1]))
        out.append(dict(peak_sec=int(s), window=[int(w0), int(w1)], r30_peak=float(r30[s]),
                        total_b=tot_b))
    return out


def main():
    t_b, p_b, q_b = m.load_trades('BTC')
    t_h, p_h, q_h = m.load_trades('HYPE')
    pffb, volb, _ = m.build_grid(t_b, p_b, q_b)
    pffh, volh, _ = m.build_grid(t_h, p_h, q_h)
    tbl_b = daily_table(t_b, p_b, q_b, pffb)
    tbl_h = daily_table(t_h, p_h, q_h, pffh)
    legs = find_legs(pffb)
    # 60秒滚动量（全窗口一次cumsum）
    cvol = np.concatenate([[0.0], np.cumsum(volb)])
    trail60 = np.full(m.NSEC, np.nan)
    trail60[59:] = cvol[60:] - cvol[:m.NSEC - 59]     # trail60[s]=vol(s-59..s]
    detail = []
    for L in legs:
        w0, w1 = L['window']
        tot_h = float(np.log(pffh[w1] / pffh[w0 - 1]))
        tb = cross(pffb, w0, w1, L['total_b'])
        th = cross(pffh, w0, w1, tot_h)
        base_lo = max(w0 - 86400, 60)
        baseline = float(np.median(trail60[base_lo:w0 - 1][~np.isnan(trail60[base_lo:w0 - 1])]))
        vt = trail60[w0:w1 + 1]
        hit = np.where(vt >= 3 * baseline)[0]
        tau_v = int(hit[0]) if len(hit) and baseline > 0 else None
        # 错位扫描：HYPE在[BTC窗+δ]上的收益，δ∈[-1800,1800]步30s
        scans = []
        for dlt in range(-1800, 1801, 30):
            a, b2 = w0 + dlt, w1 + dlt
            if a - 1 < 0 or b2 >= m.NSEC:
                scans.append((dlt, np.nan))
                continue
            scans.append((dlt, float(np.log(pffh[b2] / pffh[a - 1]))))
        best = max(scans, key=lambda x: -np.inf if np.isnan(x[1]) else x[1])
        detail.append(dict(
            peak_utc=__import__('datetime').datetime.fromtimestamp(L['peak_sec'] + m.S0, __import__('datetime').timezone.utc).isoformat(),
            r30_peak_pct=L['r30_peak'] * 100,
            btc_30min_pct=L['total_b'] * 100, hype_30min_pct=tot_h * 100,
            hype_beta_leg=tot_h / L['total_b'] if L['total_b'] else None,
            tau_b_25_50_75=tb, tau_h_25_50_75=th,
            window_hype_start_lag_s=(th[0] - tb[0]) if None not in (th[0], tb[0]) else None,
            window_hype_mid_lag_s=(th[1] - tb[1]) if None not in (th[1], tb[1]) else None,
            window_hype_done_lag_s=(th[2] - tb[2]) if None not in (th[2], tb[2]) else None,
            btc_leg_duration_s=(tb[2] - tb[0]) if None not in (tb[2], tb[0]) else None,
            hype_leg_duration_s=(th[2] - th[0]) if None not in (th[2], th[0]) else None,
            volume_baseline_60s=baseline,
            volume_peak_multiple=float(trail60[w0:w1 + 1].max() / baseline) if baseline > 0 else None,
            tau_volume_from_window_start_s=tau_v,
            price_to_volume_lag_s=(tau_v - tb[0]) if (tau_v is not None and tb[0] is not None) else None,
            volume_to_hype_lag_s=(th[0] - tau_v) if (tau_v is not None and th[0] is not None) else None,
            best_shift_s=best[0], best_shift_hype_pct=best[1] * 100))
    # episode 内 vs 外：事件分钟Δ(50%)
    tb1, cb1, _ = m.load_klines('BTC')
    rb1 = np.log(cb1[1:] / cb1[:-1])
    raw = np.where(rb1 > 0.0025)[0]
    keep = raw[np.concatenate([[True], np.diff(raw) >= 30])]
    mm = keep + 1
    ms = mm * 60000 + 1759515300000
    w2 = (ms >= m.S0 * 1000) & (ms + 60000 <= m.S1 * 1000)
    mm, ms = mm[w2], ms[w2]
    base = (ms // 1000 - m.S0).astype(np.int64)
    tot_b = np.log(pffb[base + 59] / pffb[base - 1])
    tot_h = np.log(pffh[base + 59] / pffh[base - 1])
    ok = (tot_b > 0.002) & (tot_h > 1e-5)
    base2, tb_, th_ = base[ok], tot_b[ok], tot_h[ok]
    d50 = []
    for b, t_b_, t_h_ in zip(base2, tb_, th_):
        cb = cross(pffb, b, b + 59, t_b_)
        ch = cross(pffh, b, b + 59, t_h_)
        if cb[1] is not None and ch[1] is not None:
            d50.append((b, ch[1] - cb[1]))
    in_ep = [(b, d) for b, d in d50 if EP0 - m.S0 <= b < EP1 - m.S0]
    out_ep = [(b, d) for b, d in d50 if not (EP0 - m.S0 <= b < EP1 - m.S0)]
    comp = dict(n_in=len(in_ep), n_out=len(out_ep),
                median_in=float(np.median([d for _, d in in_ep])) if in_ep else None,
                median_out=float(np.median([d for _, d in out_ep])) if out_ep else None,
                mean_in=float(np.mean([d for _, d in in_ep])) if in_ep else None,
                mean_out=float(np.mean([d for _, d in out_ep])) if out_ep else None,
                q75_in=float(np.percentile([d for _, d in in_ep], 75)) if in_ep else None,
                q75_out=float(np.percentile([d for _, d in out_ep], 75)) if out_ep else None)
    # 大秒脉冲：episode 内 vs 外的同秒占比
    rs_b = np.empty(m.NSEC); rs_h = np.empty(m.NSEC)
    rs_b[0] = rs_h[0] = 0.0
    rs_b[1:] = np.log(pffb[1:] / pffb[:-1])
    rs_h[1:] = np.log(pffh[1:] / pffh[:-1])
    q999 = float(np.quantile(rs_b, 0.999))
    ev = np.where(rs_b > q999)[0]
    ev = ev[(ev >= 20) & (ev + 5 < m.NSEC - 1)]
    k0_in = [rs_h[e] for e in ev if EP0 - m.S0 <= e < EP1 - m.S0]
    k0_out = [rs_h[e] for e in ev if not (EP0 - m.S0 <= e < EP1 - m.S0)]
    b_in = [rs_b[e] for e in ev if EP0 - m.S0 <= e < EP1 - m.S0]
    b_out = [rs_b[e] for e in ev if not (EP0 - m.S0 <= e < EP1 - m.S0)]
    comp['impulse'] = dict(
        n_in=len(k0_in), n_out=len(k0_out),
        same_sec_hype_mean_in=float(np.mean(k0_in)) if k0_in else None,
        same_sec_hype_mean_out=float(np.mean(k0_out)) if k0_out else None,
        same_sec_btc_mean_in=float(np.mean(b_in)) if b_in else None,
        same_sec_btc_mean_out=float(np.mean(b_out)) if b_out else None)
    # 段级汇总（仅统计三段滞后都存在的段）
    sane = [d for d in detail if d['window_hype_start_lag_s'] is not None
            and d['window_hype_mid_lag_s'] is not None and d['window_hype_done_lag_s'] is not None]
    def med(key):
        vals = [d[key] for d in sane if d[key] is not None]
        return float(np.median(vals)) if vals else None
    leg_summary = dict(n_sane=len(sane),
                       median_start_lag_s=med('window_hype_start_lag_s'),
                       median_mid_lag_s=med('window_hype_mid_lag_s'),
                       median_done_lag_s=med('window_hype_done_lag_s'),
                       median_btc_duration_s=med('btc_leg_duration_s'),
                       median_hype_duration_s=med('hype_leg_duration_s'),
                       median_beta=med('hype_beta_leg'),
                       beta_min=float(np.min([d['hype_beta_leg'] for d in sane])) if sane else None,
                       beta_max=float(np.max([d['hype_beta_leg'] for d in sane])) if sane else None)
    result = dict(date='2026-10-07', episode_utc=['2026-08-18T00:00:00Z', '2026-08-26T00:00:00Z'],
                  leg_window_min=LEG // 60, leg_threshold_pct=RTH * 100,
                  daily_BTC=tbl_b, daily_HYPE=tbl_h, legs=detail, leg_summary=leg_summary,
                  event_minute_comparison=comp)
    out = BASE / '2026-10-07-8月中旬行情传导窗口-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    ep_b = [r for r in tbl_b if r['in_episode']]
    print('episode BTC日表:')
    for r in ep_b:
        print('  %s O%.0f H%.0f L%.0f C%.0f 量%.0fK 笔数%.2fM' %
              (r['date'], r['open'], r['high'], r['low'], r['close'], r['volume'] / 1000, r['n_trades'] / 1e6))
    ep_h = [r for r in tbl_h if r['in_episode']]
    print('episode HYPE日表:')
    for r in ep_h:
        print('  %s O%.1f H%.1f L%.1f C%.1f 量%.1fM 笔数%.2fM' %
              (r['date'], r['open'], r['high'], r['low'], r['close'], r['volume'] / 1e6, r['n_trades'] / 1e6))
    print('上行段 %d 个:' % len(detail))
    for d in detail:
        print('  %s r30峰%+.2f%% B%+.2f%%/H%+.2f%%(beta %.2f) | HYPE滞后 启动%+ds 中点%+ds 完成%+ds | B段长%ss H段长%ss | 量基线%.2fBTC/s 峰%.1fx τV在窗内%+ds 价→量%+ds 量→HYPE%+ds | 最佳平移%+ds→HYPE%+.2f%%' % (
            d['peak_utc'][5:16], d['r30_peak_pct'], d['btc_30min_pct'], d['hype_30min_pct'],
            d['hype_beta_leg'] or float('nan'),
            d['window_hype_start_lag_s'] if d['window_hype_start_lag_s'] is not None else -999,
            d['window_hype_mid_lag_s'] if d['window_hype_mid_lag_s'] is not None else -999,
            d['window_hype_done_lag_s'] if d['window_hype_done_lag_s'] is not None else -999,
            d['btc_leg_duration_s'] if d['btc_leg_duration_s'] is not None else -999,
            d['hype_leg_duration_s'] if d['hype_leg_duration_s'] is not None else -999,
            d['volume_baseline_60s'], d['volume_peak_multiple'] or float('nan'),
            d['tau_volume_from_window_start_s'] if d['tau_volume_from_window_start_s'] is not None else -999,
            d['price_to_volume_lag_s'] if d['price_to_volume_lag_s'] is not None else -999,
            d['volume_to_hype_lag_s'] if d['volume_to_hype_lag_s'] is not None else -999,
            d['best_shift_s'], d['best_shift_hype_pct']))
    print('事件分钟Δ(50%%): episode内 n=%d 中位%+.1fs 均值%+.1fs q75=%+.1fs | episode外 n=%d 中位%+.1fs 均值%+.1fs q75=%+.1fs' % (
        comp['n_in'], comp['median_in'], comp['mean_in'], comp['q75_in'],
        comp['n_out'], comp['median_out'], comp['mean_out'], comp['q75_out']))
    im = comp['impulse']
    print('大秒同秒响应: episode内 n=%d HYPE%+.4f%%/BTC%+.4f%% = %.0f%% | episode外 n=%d HYPE%+.4f%%/BTC%+.4f%% = %.0f%%' % (
        im['n_in'], im['same_sec_hype_mean_in'] * 100, im['same_sec_btc_mean_in'] * 100,
        im['same_sec_hype_mean_in'] / im['same_sec_btc_mean_in'] * 100,
        im['n_out'], im['same_sec_hype_mean_out'] * 100, im['same_sec_btc_mean_out'] * 100,
        im['same_sec_hype_mean_out'] / im['same_sec_btc_mean_out'] * 100))


if __name__ == '__main__':
    main()
