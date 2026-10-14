"""相对强弱（RS）研究：ETH/SOL/HYPE 对 BTC 的"自己的部分"。

框架：r_X = β_X·r_BTC + ε_X（1分钟OLS分解）。研究对象是 ε（超出beta的部分）与
ln(X/BTC) 比值序列本身——不是方向（方向被β解释），是相对幅度与比值动态。

五层（全部全年1分钟K线，四币同口径）：
1. 分解事实：各币 ε 方差占比、日频 ε 波动；
2. 事件后RS漂移：BTC 5m>+0.5% / <-0.5% 事件后，各币 ε 在 +1h/+4h/+24h/+3d 的累计
   （初始1.23倍的pop会不会在日线上回吐或加强），块聚类bootstrap；
3. alt间结构：三币 ε 的截面相关（1m与日频）、谁先动（±1日lead-lag）；
4. 比值可预测性：日频 Δln(X/BTC) 自相关、偏离30日均线后的半衰期（AR1）；
5. 状态条件：BTC在30日均线上/下、实现波动率四分位下，日ε均值对比。

纯描述统计。残差用静态β（全年OLS，1分钟）。
"""
import json
from pathlib import Path

import numpy as np

import leadlag_btc_hype_1s as m

BASE = Path(__file__).resolve().parent
TOKENS = ['ETH', 'SOL', 'HYPE']
REPS = 20000
RNG = np.random.default_rng(20261008)


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


def main():
    cb = load_k('BTC')
    rb = np.log(cb[1:] / cb[:-1])                    # 1m收益，全年
    b5 = cb.reshape(-1, 5)
    rb5 = np.log(b5[:, -1][1:] / b5[:, -1][:-1])
    eps = {}
    betas = {}
    daily_eps = {}
    daily_rs = {}
    closes = {}
    for tok in TOKENS:
        ck = load_k(tok)
        closes[tok] = ck
        rk = np.log(ck[1:] / ck[:-1])
        betas[tok] = float(np.cov(rb, rk, ddof=1)[0, 1] / np.var(rb, ddof=1))
        e = rk - betas[tok] * rb
        eps[tok] = e
        ne = len(e) // 1440 * 1440
        daily_eps[tok] = e[:ne].reshape(-1, 1440).sum(axis=1)
        ratio = np.log(ck / cb)
        daily_rs[tok] = ratio[::1440][:ne // 1440]
    ndays = len(daily_eps['ETH'])
    days_axis = np.arange(ndays)

    # ---- 1. 分解事实
    layer1 = {}
    for tok in TOKENS:
        var_share = 1 - np.var(eps[tok]) / np.var(np.log(load_k(tok)[1:] / load_k(tok)[:-1]))
        layer1[tok] = dict(beta=betas[tok], btc_var_share=float(var_share),
                           eps_daily_vol=float(daily_eps[tok].std()),
                           rs_year_ret=float(daily_rs[tok][-1] - daily_rs[tok][0]))
    rs_corr = {f'{a}_{b}': float(np.corrcoef(np.diff(daily_rs[a]), np.diff(daily_rs[b]))[0, 1])
               for i, a in enumerate(TOKENS) for b in TOKENS[i + 1:]}

    # ---- 2. 事件后RS漂移（5m事件，看+1h/+4h/+24h/+3d 的 ε 累计）
    HORIZONS = dict(h1=12, h4=48, h24=288, d3=864)
    layer2 = {}
    for side, cond in (('up', rb5 > 0.005), ('down', rb5 < -0.005)):
        raw = np.where(cond)[0]
        keep = raw[np.concatenate([[True], np.diff(raw) >= 6])]
        valid = keep[keep <= len(rb5) - 2 - 900]
        per_tok = {}
        for tok in TOKENS:
            k5 = closes[tok].reshape(-1, 5)                  # 与rb5严格同口径对齐
            rk5 = np.log(k5[:, -1][1:] / k5[:, -1][:-1])
            e5 = rk5 - betas[tok] * rb5                       # 5分钟ε
            cols = []
            for h in HORIZONS.values():
                cols.append(np.array([e5[v + 1:v + 1 + h].sum() for v in valid]))
            M = np.column_stack(cols)
            boots = block_boot(M, valid // 288)
            per_tok[tok] = ci(boots, M.mean(axis=0))
        layer2[side] = dict(events=int(len(valid)), horizons=list(HORIZONS), eps_fwd=per_tok)

    # ---- 3. alt间结构
    layer3 = dict(corr_1m={}, corr_daily={}, leadlag_daily={})
    for i, a in enumerate(TOKENS):
        for b in TOKENS[i + 1:]:
            layer3['corr_1m'][f'{a}_{b}'] = float(np.corrcoef(eps[a], eps[b])[0, 1])
            layer3['corr_daily'][f'{a}_{b}'] = float(np.corrcoef(daily_eps[a], daily_eps[b])[0, 1])
            dpa, dpb = daily_eps[a], daily_eps[b]
            ll = [float(np.corrcoef(np.roll(dpa, k), dpb)[0, 1]) for k in (-1, 0, 1)]
            layer3['leadlag_daily'][f'{a}_{b}'] = dict(lead_b=ll[0], same=ll[1], lag_b=ll[2])

    # ---- 4. 比值可预测性
    layer4 = {}
    for tok in TOKENS:
        drs = np.diff(daily_rs[tok])                 # 日RS变化
        ac = [float(np.corrcoef(drs[k:], drs[:-k])[0, 1]) for k in (1, 2, 3, 5)]
        dev = daily_rs[tok] - np.convolve(daily_rs[tok], np.ones(30) / 30, mode='same')
        dev = dev[30:-30]
        rho = float(np.corrcoef(dev[1:], dev[:-1])[0, 1])
        halflife = float(-np.log(2) / np.log(abs(rho))) if abs(rho) < 1 else None
        layer4[tok] = dict(daily_rs_change_autocorr_lag1_2_3_5=ac,
                           dev_ar1_rho=rho, dev_halflife_days=halflife)

    # ---- 5. 状态条件
    px = cb[: (ndays) * 1440].reshape(-1, 1440)[:, -1]
    sma30 = np.convolve(px, np.ones(30) / 30, mode='same')
    rv = np.convolve(np.abs(rb), np.ones(1440), mode='valid')[::1440][:ndays]
    layer5 = {}
    for tok in TOKENS:
        de = daily_eps[tok]
        state_trend = dict(above_sma=float(de[px > sma30].mean()), below_sma=float(de[px <= sma30].mean()))
        qs = np.quantile(rv, [0.25, 0.5, 0.75])
        qv = [float(de[rv <= qs[0]].mean()), float(de[(rv > qs[0]) & (rv <= qs[1])].mean()),
              float(de[(rv > qs[1]) & (rv <= qs[2])].mean()), float(de[rv > qs[2]].mean())]
        layer5[tok] = dict(trend_state=state_trend, vol_quartile_eps_mean=qv)

    result = dict(date='2026-10-08', frame='r_X = beta·r_BTC + eps; 研究eps与ln(X/BTC)',
                  n_days=int(ndays), layer1=layer1, rs_corr=rs_corr,
                  layer2=layer2, layer3=layer3, layer4=layer4, layer5=layer5)
    out = BASE / '2026-10-08-相对强弱研究-结果.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')

    print('1. 分解: ' + ' | '.join('%s β%.2f BTC解释%.0f%% 日ε波动%.2f%% RS年变动%+.1f%%' % (
        t, layer1[t]['beta'], layer1[t]['btc_var_share'] * 100,
        layer1[t]['eps_daily_vol'] * 100, layer1[t]['rs_year_ret'] * 100) for t in TOKENS))
    print('   日RS变动相关: ' + ', '.join('%s %.2f' % (k, v) for k, v in rs_corr.items()))
    for side in ('up', 'down'):
        print('2. BTC%s事件(n=%d)后 ε 累计(%%):' % (side, layer2[side]['events']))
        for tok in TOKENS:
            e = layer2[side]['eps_fwd'][tok]
            print('   %s ' % tok + '  '.join('%s %+.3f[%+.3f,%+.3f]' % (h, e['estimate'][j] * 100, e['ci95_lo'][j] * 100, e['ci95_hi'][j] * 100)
                  for j, h in enumerate(layer2[side]['horizons'])))
    print('3. ε相关 1m: ' + ', '.join('%s %.2f' % (k, v) for k, v in layer3['corr_1m'].items())
          + ' | 日频: ' + ', '.join('%s %.2f' % (k, v) for k, v in layer3['corr_daily'].items()))
    print('   日lead-lag (lead_b=前一日a与当日b):')
    for k, v in layer3['leadlag_daily'].items():
        print('     %s %+0.2f / %0.2f / %+0.2f' % (k, v['lead_b'], v['same'], v['lag_b']))
    for tok in TOKENS:
        l4 = layer4[tok]
        print('4. %s 日RS变化自相关 %s  AR1(偏离30MA) ρ=%.2f 半衰期 %.1f天' % (
            tok, [round(x, 2) for x in l4['daily_rs_change_autocorr_lag1_2_3_5']],
            l4['dev_ar1_rho'], l4['dev_halflife_days'] or -1))
    for tok in TOKENS:
        l5 = layer5[tok]
        print('5. %s ε日均: 均线上%+.3f%%/均线下%+.3f%% | RV四分位 %s' % (
            tok, l5['trend_state']['above_sma'] * 100, l5['trend_state']['below_sma'] * 100,
            ['%+.3f' % (x * 100) for x in l5['vol_quartile_eps_mean']]))


if __name__ == '__main__':
    main()
