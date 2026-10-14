"""HYPE 对 BTC 的跟随比例（beta）画像。

问题：HYPE 跟随 BTC，但跟随比例是多少、是否稳定？
数据：全年1分钟/5分钟K线（2025-10-04~2026-10-04）、aggTrades 1秒网格（2026-07-04~10-03）。

输出：
1. 多尺度回归 beta：1s / 1m / 5m / 1h，rH = α + β·rB + ε，报 β、corr、R²、α；
2. 涨跌不对称：rB>0 与 rB<0 分开的 beta，及条件均值比 E[rH|rB>0]/E[rB|rB>0]；
3. 波动分桶：|rB| 十分位内 beta 与均值比（跟随比例是否随冲击变大）；
4. 事件集口径：1m 大上涨/大下跌事件的 E[rH]/E[rB]（冲击时刻的瞬时跟随比例）；
5. 全年滚动30天 beta 与 corr（1m），标注8月中旬episode。

纯描述统计，无推断。
"""
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m

BASE = Path(__file__).resolve().parent


def load_klines(tok):
    p = m.K1M / tok / '1759515300000-1791051300000.json'
    doc = json.loads(p.read_bytes())
    t = np.array([c['open_time_ms'] for c in doc['candles']], dtype=np.int64)
    close = np.array([c['close'] for c in doc['candles']])
    return t, close


def beta(y, x):
    x, y = np.asarray(x, float), np.asarray(y, float)
    b = float(np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1))
    a = float(y.mean() - b * x.mean())
    c = float(np.corrcoef(x, y)[0, 1])
    return dict(beta=b, alpha=a, corr=c, r2=c * c, n=int(len(x)))


def bucket_table(rb, rh, q=10):
    qs = np.quantile(np.abs(rb), np.linspace(0, 1, q + 1))
    rows = []
    for i in range(q):
        lo, hi = qs[i], qs[i + 1]
        sel = (np.abs(rb) >= lo) & (np.abs(rb) <= hi if i == q - 1 else np.abs(rb) < hi)
        x, y = rb[sel], rh[sel]
        if len(x) < 100 or x.mean() == 0:
            continue
        rows.append(dict(abs_rb_bucket=[float(lo), float(hi)],
                         mean_rb_pct=float(x.mean() * 100), mean_rh_pct=float(y.mean() * 100),
                         mean_ratio=float(y.mean() / x.mean()),
                         beta=float(np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1)),
                         n=int(len(x))))
    return rows


def rolling_beta(rb, rh, win):
    n = len(rb)
    sx = np.concatenate([[0], np.cumsum(rb)])
    sy = np.concatenate([[0], np.cumsum(rh)])
    sxy = np.concatenate([[0], np.cumsum(rb * rh)])
    sxx = np.concatenate([[0], np.cumsum(rb * rb)])
    i = np.arange(win, n)
    mx = (sx[i] - sx[i - win]) / win
    my = (sy[i] - sy[i - win]) / win
    cxy = (sxy[i] - sxy[i - win]) / win - mx * my
    cxx = (sxx[i] - sxx[i - win]) / win - mx * mx
    b = cxy / cxx
    vy = ((np.concatenate([[0], np.cumsum(rh * rh)])[i] -
           np.concatenate([[0], np.cumsum(rh * rh)])[i - win]) / win - my * my)
    r = cxy / np.sqrt(cxx * vy)
    return i, b, r


def main():
    _, cb = load_klines('BTC')
    _, ch = load_klines('HYPE')
    rb1 = np.log(cb[1:] / cb[:-1])
    rh1 = np.log(ch[1:] / ch[:-1])
    b5 = cb.reshape(-1, 5)
    h5 = ch.reshape(-1, 5)
    rb5 = np.log(b5[:, -1][1:] / b5[:, -1][:-1])
    rh5 = np.log(h5[:, -1][1:] / h5[:, -1][:-1])
    bh = cb.reshape(-1, 60)
    hh = ch.reshape(-1, 60)
    rbh = np.log(bh[:, -1][1:] / bh[:, -1][:-1])
    rhh = np.log(hh[:, -1][1:] / hh[:, -1][:-1])
    t_b, p_b, q_b = m.load_trades('BTC')
    t_h, p_h, q_h = m.load_trades('HYPE')
    pffb, _, _ = m.build_grid(t_b, p_b, q_b)
    pffh, _, _ = m.build_grid(t_h, p_h, q_h)
    rs_b = np.empty(m.NSEC)
    rs_h = np.empty(m.NSEC)
    rs_b[0] = rs_h[0] = 0.0
    rs_b[1:] = np.log(pffb[1:] / pffb[:-1])
    rs_h[1:] = np.log(pffh[1:] / pffh[:-1])

    scales = dict(s1=beta(rs_h, rs_b), m1=beta(rh1, rb1), m5=beta(rh5, rb5), h1=beta(rhh, rbh))

    updn = dict(
        up=beta(rh1[rb1 > 0], rb1[rb1 > 0]),
        down=beta(rh1[rb1 < 0], rb1[rb1 < 0]),
        up_mean_ratio=float(rh1[rb1 > 0].mean() / rb1[rb1 > 0].mean()),
        down_mean_ratio=float(rh1[rb1 < 0].mean() / rb1[rb1 < 0].mean()))

    buckets = bucket_table(rb1, rh1)

    ev_up = rb1 > 0.0025
    ev_dn = rb1 < -0.0025
    events = dict(
        up_n=int(ev_up.sum()), up_mean_b=float(rb1[ev_up].mean() * 100),
        up_mean_h=float(rh1[ev_up].mean() * 100),
        up_ratio=float(rh1[ev_up].mean() / rb1[ev_up].mean()),
        dn_n=int(ev_dn.sum()), dn_mean_b=float(rb1[ev_dn].mean() * 100),
        dn_mean_h=float(rh1[ev_dn].mean() * 100),
        dn_ratio=float(rh1[ev_dn].mean() / rb1[ev_dn].mean()))

    win = 43200                     # 30天（1分钟）
    ti, b30, r30 = rolling_beta(rb1, rh1, win)
    _, cb_t = load_klines('BTC')
    tt = np.arange(len(cb))[1:]
    tms = tt[ti] * 60000 + 1759515300000
    EP0, EP1 = 1787011200000, 1787702400000
    in_ep = (tms >= EP0) & (tms < EP1)
    roll = dict(window_days=30,
                beta_min=float(b30.min()), beta_min_date=int(tms[int(b30.argmin())]),
                beta_max=float(b30.max()), beta_max_date=int(tms[int(b30.argmax())]),
                beta_last=float(b30[-1]),
                beta_mean=float(b30.mean()),
                beta_episode_median=float(np.median(b30[in_ep])) if in_ep.any() else None,
                beta_out_episode_median=float(np.median(b30[~in_ep])),
                corr_episode_median=float(np.median(r30[in_ep])) if in_ep.any() else None,
                corr_out_episode_median=float(np.median(r30[~in_ep])))

    result = dict(date='2026-10-07', question='HYPE对BTC的跟随比例',
                  scales=scales, updown=updn, abs_buckets=buckets,
                  event_ratio=events, rolling30d=roll)
    out = BASE / '2026-10-07-HYPE对BTC跟随比例-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('多尺度beta:', {k: (round(v['beta'], 3), round(v['corr'], 3), round(v['r2'], 3))
                          for k, v in scales.items()})
    print('涨跌不对称: up beta %.3f (均值比 %.3f) | down beta %.3f (均值比 %.3f)' %
          (updn['up']['beta'], updn['up_mean_ratio'], updn['down']['beta'], updn['down_mean_ratio']))
    print('事件集 1m>0.25%%: n=%d B均%+.3f%% H均%+.3f%% 比 %.2f | 1m<-0.25%%: n=%d B均%+.3f%% H均%+.3f%% 比 %.2f' % (
        events['up_n'], events['up_mean_b'], events['up_mean_h'], events['up_ratio'],
        events['dn_n'], events['dn_mean_b'], events['dn_mean_h'], events['dn_ratio']))
    print('|rB|分桶（1m十分位）:')
    for r in buckets:
        print('  |rB|%5.3f%%~%5.3f%%  n=%6d  均值比 %.2f  beta %.2f' %
              (r['abs_rb_bucket'][0] * 100, r['abs_rb_bucket'][1] * 100, r['n'],
               r['mean_ratio'], r['beta']))
    import datetime as dt
    d = lambda ms: dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).date().isoformat()
    print('滚动30d beta(1m): 均值 %.2f 最小 %.2f(%s) 最大 %.2f(%s) 末值 %.2f | 8月段中位 %.2f（段外中位 %.2f）' % (
        roll['beta_mean'], roll['beta_min'], d(roll['beta_min_date']),
        roll['beta_max'], d(roll['beta_max_date']), roll['beta_last'],
        roll['beta_episode_median'], roll['beta_out_episode_median']))
    print('滚动30d corr: 8月段中位 %.2f 段外中位 %.2f' % (roll['corr_episode_median'], roll['corr_out_episode_median']))


if __name__ == '__main__':
    main()
