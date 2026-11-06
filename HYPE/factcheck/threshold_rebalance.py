"""HYPE/BTC 阈值再平衡补测：真实美元口径下 tau 0/2/5/10% 对比（回答"当初为什么没跑"）。

背景：2026-10-09 归档的常驻 pair（净 +90.8%）用的是对数线性口径（隐含每日回等名义），
当时未做阈值再平衡，原因：再平衡成本仅 ~1%/年，相对 +90.8% 不显著；加密市场 7×24
可随时限价补偏离量。本脚本在补全的 standing_pair_dollar 上补测，验证该省略是否无代价。

口径：crypto 1m 线 → 日桶简单收益；资金费按单位名义日净流入（+BTC −HYPE）×当日名义均值；
佣金 5bp/边（taker）；tau=0 即每日再平衡。
"""
import json
import sys
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parents[1] / '研究流程'))
import pair_lib as pl
from pair_lib import ANN_CRYPTO, metrics

TAUS = (0.0, 0.02, 0.05, 0.10)
FEE_SIDE = 5e-4


def main():
    t_b, c_b = pl.load_crypto_minutes('BTC')
    t_h, c_h = pl.load_crypto_minutes('HYPE')
    t, c_h, c_b = pl.align_pair(t_h, c_h, t_b, c_b)
    r_h = np.r_[0.0, np.log(c_h[1:] / c_h[:-1])]
    r_b = np.r_[0.0, np.log(c_b[1:] / c_b[:-1])]
    dk = pl.day_keys(t, 'crypto')
    n_days = int(dk[-1]) + 1

    # 资金费日净流入（+BTC收 −HYPE付），按日桶聚合
    fund = np.zeros(n_days)
    for tok, sign in (('BTC', 1.0), ('HYPE', -1.0)):
        ft, fr = pl.crypto_funding_events(tok)
        day = (ft - t[0]) // 86_400_000
        for d, r in zip(day, fr):
            if 0 <= d < n_days:
                fund[int(d)] += sign * r

    print('HYPE/BTC 多HYPE空BTC 美元口径 阈值对比（资金费已含，佣金5bp/边）')
    rows = []
    for tau in TAUS:
        res = pl.standing_pair_dollar(t, r_h, r_b, dk, tau, fee_side=FEE_SIDE, fund_daily=fund)
        m = metrics(res['equity'], ANN_CRYPTO)
        rows.append(dict(tau=tau, net_pct=round(float((res['equity'][-1] - 1) * 100), 2),
                         max_dd_pct=round(m['max_dd_pct'], 2), sharpe=round(m['sharpe'], 2),
                         n_rebalance=res['n_rebalance'],
                         cost_pct=round(res['cost_total'] * 100, 2),
                         funding_note='资金费按单位名义日净流入×当日名义均值近似'))
        print('tau=%3.0f%%: 净 %+7.1f%% | 回撤 %6.1f%% | SR %.2f | 再平衡 %3d 次 | 佣金 %.2f%%' % (
            tau * 100, (res['equity'][-1] - 1) * 100, m['max_dd_pct'], m['sharpe'],
            res['n_rebalance'], res['cost_total'] * 100))

    out = BASE / '2026-10-21-阈值再平衡-结果.json'
    out.write_text(json.dumps(dict(
        date='2026-10-21', pair='HYPE/BTC', direction='long HYPE / short BTC',
        granularity='1m→日桶', fee_side=FEE_SIDE,
        reference='对数线性口径(2026-10-09归档): 净+90.8% 回撤-61.1%',
        rows=rows), ensure_ascii=False, indent=2) + '\n')
    print('已写出', out.name)


if __name__ == '__main__':
    main()
