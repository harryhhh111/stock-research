"""回归验证：用 pair_lib 重跑 HYPE/BTC 常驻 pair，与 2026-10-09 归档结果逐项对比。

通过标准：净收益/价格毛/资金费/再平衡成本/回撤 等各项与归档 JSON 误差 <0.1pp。
此脚本证明抽象后的引擎与原版 pair_backtest.py 计算等价；HYPE 旧脚本本身不做改动。
"""
import json
import sys
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent          # 研究流程/pair_lib
sys.path.insert(0, str(BASE.parent))            # 导入 pair_lib 包
import pair_lib as pl

ROOT = BASE.parents[1]
ARCHIVE = ROOT / 'HYPE' / 'factcheck' / '2026-10-09-pair净值回测-结果.json'

TOL = 0.1          # pp
failed = []


def cmp(name, mine, theirs):
    d = abs(mine - theirs)
    ok = d < TOL
    print('%s %-26s 库 %+.3f | 归档 %+.3f | Δ%.4fpp' % (
        'OK  ' if ok else 'FAIL', name, mine, theirs, d))
    if not ok:
        failed.append(name)


def main():
    t_b, c_b = pl.load_crypto_minutes('BTC')
    t_h, c_h = pl.load_crypto_minutes('HYPE')
    t, c_h, c_b = pl.align_pair(t_h, c_h, t_b, c_b)
    assert len(t) == 525600, f'bar 数 {len(t)} != 525600（数据窗口变了？）'
    r_h = np.r_[0.0, np.log(c_h[1:] / c_h[:-1])]
    r_b = np.r_[0.0, np.log(c_b[1:] / c_b[:-1])]
    dk = pl.day_keys(t, 'crypto')

    t_fb, r_fb = pl.crypto_funding_events('BTC')
    t_fh, r_fh = pl.crypto_funding_events('HYPE')
    carry_t = np.r_[t_fb, t_fh]
    carry_r = np.r_[r_fb, -r_fh]

    res = pl.standing_pair(t, r_h, r_b, dk, carry_t, carry_r, fee_side=0.0005)
    ref = json.loads(ARCHIVE.read_bytes())['standing']
    att = res['attribution']

    cmp('价格毛%', att['price'] * 100, ref['price_gross_pct'])
    cmp('资金费贡献%', att['carry'] * 100, ref['funding_contrib_pct'])
    cmp('资金费后%', res['daily_eq'][-1] * 100, ref['after_funding_pct'])
    cmp('再平衡成本%', att['reb_cost'] * 100, ref['rebalance_cost_pct'])
    cmp('净收益%', res['net_eq'][-1] * 100, ref['net_total_pct'])
    cmp('最大回撤(日)%', res['max_dd_daily'] * 100, ref['daily']['max_dd_pct'])
    cmp('最大回撤(分钟)%', res['max_dd_bar'] * 100, ref['minute_max_dd_pct'])
    cmp('日夏普(资金费后)', pl.curve_stats(res['daily_eq'])['sharpe_daily'], ref['daily']['sharpe_daily'])
    cmp('日夏普(净)', pl.curve_stats(res['net_eq'])['sharpe_daily'], ref['net_daily']['sharpe_daily'])
    cmp('上涨日占比(净)', pl.curve_stats(res['net_eq'])['up_day_share'], ref['net_daily']['up_day_share'])

    print()
    if failed:
        print('回归失败 %d 项：%s' % (len(failed), ', '.join(failed)))
        sys.exit(1)
    print('回归通过：pair_lib 与 2026-10-09 归档结果一致（<%0.1fpp）' % TOL)


if __name__ == '__main__':
    main()
