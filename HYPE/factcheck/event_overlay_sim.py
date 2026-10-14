"""事件规避 overlay 模拟：常驻pair在"日历可知利空"窗口空仓的效果。

用户设想：正常 1:1 空BTC多HYPE；确定性重大利空前 1-2 个月空仓；利空出尽后回场。
用今年唯一的事件簇（2025-11-28 创世周年解锁 cliff，官方 2024-11-28 公告、可提前知道）
做示意模拟。再入场用两个客观上可执行的规则：
  R1 固定时点：事件后 33 天（2026-02-01）
  R2 趋势确认：HYPE/BTC 日收盘重新站上其 30 日均线（信号每日可算，无事后信息）
对比基准（全程持有）与两种 overlay 的净收益、最大回撤、空仓期错过的暴跌反弹 alpha。
"""
import datetime as dt
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
FUND = ROOT / '数字资产' / 'factcheck' / 'data' / 'normalized' / 'binance-perp' / 'funding'
WINDOW = '1759515300000-1791051300000'
N_MIN, N_DAY = 525600, 365
COST_RT = 0.0015                       # 一次进出双边 ≈0.15%


def load_funding(tok):
    doc = json.loads((FUND / tok / f'{WINDOW}.json').read_bytes())
    return (np.array([e['funding_time_ms'] for e in doc['events']], dtype=np.int64),
            np.array([e['funding_rate'] for e in doc['events']]))


def main():
    t1m, cb = m.load_klines('BTC')[0], m.load_klines('BTC')[1]
    ch = m.load_klines('HYPE')[1]
    r_h = np.r_[0.0, np.log(ch[1:] / ch[:-1])]
    r_b = np.r_[0.0, np.log(cb[1:] / cb[:-1])]
    pmin = (r_h - r_b).copy()                                  # 每分钟pnl：资金费必须先加在分钟层
    t_fb, r_fb = load_funding('BTC')
    t_fh, r_fh = load_funding('HYPE')
    for t, r in zip(t_fb, r_fb):
        pmin[min(max(t // 60000 - t1m[0] // 60000 - 1, 0), N_MIN - 1)] += r
    for t, r in zip(t_fh, r_fh):
        pmin[min(max(t // 60000 - t1m[0] // 60000 - 1, 0), N_MIN - 1)] -= r
    curve = np.cumsum(pmin)
    curve = curve - (0.010 / N_MIN) * np.arange(N_MIN)        # 再平衡成本线性扣
    d = curve.reshape(N_DAY, 1440)[:, -1]                     # 日末净值
    days = [dt.datetime.fromtimestamp(t1m[i * 1440] / 1000, dt.timezone(dt.timedelta(hours=8))) for i in range(N_DAY)]
    d0 = days[0]

    def day_idx(y, mo, dd):
        return int((dt.datetime(y, mo, dd, tzinfo=dt.timezone(dt.timedelta(hours=8))) - d0).total_seconds() // 86400)

    event_i = day_idx(2025, 11, 28)                            # 解锁 cliff
    exit_i = max(day_idx(2025, 11, 28) - 60, 0)                # 提前60天,截断到窗口起点
    ratio = (ch / cb).reshape(N_DAY, 1440)[:, -1]
    ma30 = np.convolve(ratio, np.ones(30) / 30, mode='valid')  # 下标 i 对应 days[i+29]
    r2 = None
    for j in range(event_i + 1, N_DAY):
        k = j - 29
        if k >= 0 and ratio[j] > ma30[k]:
            r2 = j
            break
    r1 = day_idx(2026, 2, 1)
    print('事件日=%s 空仓起点=%s | R1回场=%s R2(站上30MA)回场=%s' % (
        days[event_i].date(), days[exit_i].date(), days[r1].date(), days[r2].date() if r2 else None))

    def simulate(reenter_i):
        keep = np.ones(N_DAY)
        keep[exit_i:reenter_i] = 0.0
        eq = np.cumsum(np.diff(np.r_[0.0, d]) * keep)
        # 空仓期免资金费? 不——资金费已含在curve,空仓即不付不收,上面逐日pnl乘0自然处理
        n_switch = 2 if exit_i > 0 else 1                        # 起点即空仓只算一次回场成本
        eq = eq - COST_RT * n_switch
        dd = (eq - np.maximum.accumulate(eq)).min()
        return eq, dd, keep

    base_dd = (d - np.maximum.accumulate(d)).min()
    print('基准(全程持有): 净%+0.1f%% 最大回撤(日)%0.1f%%' % (d[-1] * 100, base_dd * 100))
    res = {}
    for name, ri in (('R1固定33天', r1), ('R2站上30MA', r2)):
        eq, dd, keep = simulate(ri)
        flat_days = int((keep == 0).sum())
        missed = [i for i in range(N_DAY) if keep[i] == 0]
        # 空仓期错过的 BTC 5m<-0.5% 暴跌事件数(近似: 用日收益<-1.5%且发生在空仓段的粗略计数不够准,
        # 这里用已归档的事件分钟段: 空仓段内 BTC日跌>3% 的天数作为代理)
        crash_proxy = sum(1 for i in missed if r_b.reshape(N_DAY, 1440).sum(1)[i] < -0.03)
        print('%s: 净%+0.1f%% 最大回撤(日)%0.1f%% 空仓%d天(占%.0f%%) 空仓段BTC日跌>3%%天数=%d' % (
            name, eq[-1] * 100, dd * 100, flat_days, flat_days / N_DAY * 100, crash_proxy))
        res[name] = dict(net_pct=float(eq[-1] * 100), max_dd_pct=float(dd * 100), flat_days=flat_days)
    res['base'] = dict(net_pct=float(d[-1] * 100), max_dd_pct=float(base_dd * 100))
    (BASE / '2026-10-10-事件规避overlay模拟-结果.json').write_text(
        json.dumps(res, ensure_ascii=False, indent=2) + '\n')
    print('已写出 2026-10-10-事件规避overlay模拟-结果.json')


if __name__ == '__main__':
    main()
