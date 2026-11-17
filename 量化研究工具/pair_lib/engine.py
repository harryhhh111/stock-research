"""pair 回测引擎：常驻等名义多空。

standing_pair(t_ms, r_a, r_b, day_key, carry_t, carry_r, fee_side, carry_map='minute'):
  每 bar 线性 spread = r_a − r_b（每腿单位名义，非复利）；
  carry 事件（资金费差额/借券费）映射到 bar（与 HYPE 旧脚本同公式）：
    carry_map='minute'（默认，分钟 bar 归档口径）：事件分钟 − 首bar分钟 − 1；
    carry_map='clock'（日线等非分钟 bar）：searchsorted 落到时间不晚于事件的最后一根 bar——
    日线数据若误用 'minute'，全部 carry 会被堆到最后一根 bar（全年总数不变、年内时点全错）；
  按 day_key 分日聚合出日度净值；再平衡成本 = fee_side × Σ_d(|r_a,d|+|r_b,d|)（每日回等名义）。

返回 dict：
  daily_eq / bar_eq / net_eq（成本后）, day_returns, attribution{price,carry,reb_cost},
  max_dd_daily, max_dd_bar, day_of_leg_a/b（每日各腿对数收益，供成本与基准计算）
"""
import numpy as np


def standing_pair(t_ms, r_a, r_b, day_key, carry_t=None, carry_r=None, fee_side=5e-4,
                  carry_map='minute'):
    n = len(r_a)
    pnl = (np.asarray(r_a, dtype=float) - np.asarray(r_b, dtype=float)).copy()
    if carry_t is not None and len(carry_t):
        if carry_map == 'clock':
            # 任意 bar 粒度通用：事件落到时间不晚于它的最后一根 bar（日线必须走这个）
            idxs = np.searchsorted(t_ms, carry_t, side='right') - 1
        else:
            # 分钟 bar 的归档口径（HYPE 回归基准）：分钟差 −1
            t0 = int(t_ms[0])
            idxs = np.asarray(carry_t, dtype=np.int64) // 60000 - t0 // 60000 - 1
        for idx, r in zip(idxs, carry_r):
            pnl[min(max(int(idx), 0), n - 1)] += r
    edges = np.flatnonzero(np.r_[True, day_key[1:] != day_key[:-1], True])
    starts, stops = edges[:-1], edges[1:]
    day_pnl = np.add.reduceat(pnl, starts)
    d_a = np.add.reduceat(r_a, starts)
    d_b = np.add.reduceat(r_b, starts)
    daily = np.cumsum(day_pnl)
    reb_cost = float(fee_side * (np.abs(d_a) + np.abs(d_b)).sum())
    bar_eq = np.cumsum(pnl)
    carry_sum = float(np.asarray(carry_r).sum()) if carry_r is not None else 0.0
    return dict(
        daily_eq=daily, bar_eq=bar_eq, net_eq=daily - reb_cost,
        day_returns=day_pnl, day_of_leg_a=d_a, day_of_leg_b=d_b,
        attribution=dict(price=float((r_a - r_b).sum()), carry=carry_sum, reb_cost=reb_cost),
        max_dd_daily=float((daily - np.maximum.accumulate(daily)).min()),
        max_dd_bar=float((bar_eq - np.maximum.accumulate(bar_eq)).min()),
        n_days=int(len(starts)))


def standing_pair_dollar(t_ms, r_a, r_b, day_key, tau, fee_side=2e-4,
                         borrow_ann=0.0, fund_daily=None):
    """真实美元口径的阈值再平衡 pair。

    与 standing_pair（对数线性、隐含每日回等名义）不同：腿名义随价格漂移，
    仅当偏离比例 |V_L−V_S|/均值 > tau 时拉回等名义（目标=两腿均值）。
    tau=0 即每日再平衡。成本=fee_side×|V_L−V_S|（只补偏离量，非全仓重开）；
    借券费按短腿当前名义×日历间隔计提；fund_daily 为按单位名义的每日资金费净流入
    （多腿收−空腿付），按当日两腿均值名义近似计提。

    r_a/r_b 为对数 bar 收益，内部按日桶转简单收益。返回 dict(equity, n_rebalance,
    cost_total, borrow_total)——equity 为复利美元净值（初始 1.0）。
    """
    edges = np.flatnonzero(np.r_[True, day_key[1:] != day_key[:-1], True])
    starts = edges[:-1]
    ra_d = np.add.reduceat(r_a, starts)                 # 日对数收益
    rb_d = np.add.reduceat(r_b, starts)
    sa = np.exp(ra_d) - 1.0                             # 转简单收益
    sb = np.exp(rb_d) - 1.0
    last_bar = edges[1:] - 1
    gaps = np.empty(len(starts))
    gaps[0] = 1.0
    gaps[1:] = (t_ms[last_bar[1:]] - t_ms[last_bar[:-1]]) / 86_400_000.0

    V_L = V_S = 1.0
    E = 1.0
    n = 0
    cost_total = 0.0
    borrow_total = 0.0
    equity = np.empty(len(starts) + 1)
    equity[0] = 1.0
    for i in range(len(starts)):
        # 当日盈亏按当前名义计提并滚入权益与腿名义
        pnl_l = V_L * sa[i]
        pnl_s = V_S * sb[i]
        V_L += pnl_l
        V_S += pnl_s
        E += pnl_l - pnl_s
        mid = 0.5 * (V_L + V_S)
        if fund_daily is not None:
            E += fund_daily[i] * mid
        if borrow_ann > 0:
            br = borrow_ann * gaps[i] / 365.0 * V_S
            E -= br
            borrow_total += br
        if abs(V_L - V_S) / mid > tau:
            # 拉回等名义只改变腿的分布，不改变权益（除佣金）
            cost = fee_side * abs(V_L - V_S)
            E -= cost
            cost_total += cost
            V_L = V_S = mid
            n += 1
        equity[i + 1] = E
    return dict(equity=equity, n_rebalance=int(n),
                cost_total=float(cost_total), borrow_total=float(borrow_total))
