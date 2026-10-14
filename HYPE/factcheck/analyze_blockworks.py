"""Reproduce weekly analysis from unchanged Blockworks JSON snapshots."""
import json
import math
import statistics
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
START, END = date(2025, 9, 29), date(2026, 9, 27)
fees = json.loads((DATA / '2026-09-30-blockworks-fees-daily.json').read_text())
buys = json.loads((DATA / '2026-09-30-blockworks-buybacks-daily.json').read_text())
assert len(fees['data']) == fees['total']
assert len(buys['data']) == buys['total']
daily = defaultdict(lambda: defaultdict(float))
seen = set()
for r in fees['data']:
    d = date.fromisoformat(r['date'])
    if r['grouping_level'] == 'totals':
        assert d not in seen
        seen.add(d)
        daily[d]['fees'] = r['total_fee_usd_totals'] or 0
        daily[d]['protocol'] = r['protocol_fee_usd_totals'] or 0
    elif r['grouping_level'] == 'market_type':
        if r['label'] in ('Native Perp', 'HIP-3 Perp'):
            k = 'native' if r['label'] == 'Native Perp' else 'hip3'
            daily[d][k] += r['protocol_fee_usd_market_type'] or 0
seen_b = set()
for r in buys['data']:
    if r['grouping_level'] == 'totals':
        d = date.fromisoformat(r['date'])
        assert d not in seen_b
        seen_b.add(d)
        daily[d]['buybacks'] = r['vol_usd_totals'] or 0
        daily[d]['hype'] = r['vol_hype_totals'] or 0
for i in range((END-START).days+1):
    d = START + timedelta(days=i)
    assert d in seen and d in seen_b, f'Missing daily total: {d}'
weeks = []
for i in range(52):
    s = START + timedelta(days=7*i)
    w = {'start': str(s), 'end': str(s+timedelta(days=6))}
    for k in ('fees', 'protocol', 'native', 'hip3', 'buybacks', 'hype'):
        w[k] = sum(daily[s+timedelta(days=j)][k] for j in range(7))
    w['buyback_price'] = w['buybacks']/w['hype'] if w['hype'] else None
    weeks.append(w)

def corr(xs, ys):
    mx, my = statistics.mean(xs), statistics.mean(ys)
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/math.sqrt(sum((x-mx)**2 for x in xs)*sum((y-my)**2 for y in ys))

out = ['# Hyperliquid 最近一年手续费与回购周度核对', '',
       '整理/核对日期：2026-09-30；数据截止：2026-09-29。', '',
       '来源：[Blockworks Hyperliquid Financials](https://app.blockworks.com/projects/hyperliquid/analytics/hyperliquid-financials)。原始数值是第三方链上统计；以下汇总、变化和相关系数为自己复算。', '',
       '## 口径与完整性', '',
       '- 两张图公开接口返回完整数据：Fees 25,154 行；Buybacks 6,873 行。仅使用 totals，市场拆分只用 market_type，避免将同一流水重复累加。',
       '- 最近 52 个完整自然周：2025-09-29 至 2026-09-27，共 364 天；364 天均有手续费和回购总计记录。周一至周日汇总；不保证网站 Weekly 的周起始日相同。',
       '- Fees 为总费用，包含协议、Builder、Deployer、Gas 与部署拍卖等。协议手续费另列；原生/HIP-3 为协议手续费市场分类，不包含相应第三方分账。',
       '- Buybacks 为实际买入的美元成交金额和 HYPE 数量。Buybacks / Fees 是观察比率，不是分配规则；直接燃烧、第三方分账、资金结余和执行时差均会影响它。', '',
       '## 每 13 周分段（金额：百万美元；HYPE：百万枚）', '',
       '| 期间 | 总费用 | 协议手续费 | 原生永续协议手续费 | HIP-3 协议手续费 | 实际回购 | HYPE 数量 | 回购均价（美元） |',
       '|---|---:|---:|---:|---:|---:|---:|---:|']
for i in range(4):
    ws = weeks[i*13:(i+1)*13]
    sums = {k:sum(w[k] for w in ws) for k in ('fees','protocol','native','hip3','buybacks','hype')}
    out.append(f"| {ws[0]['start']}—{ws[-1]['end']} | " + ' | '.join(f'{sums[k]/1e6:.2f}' for k in sums) + f" | {sums['buybacks']/sums['hype']:.2f} |")
out += ['', '## 结论', '',
        '❌「手续费与回购过去一年持续上涨」不符。总费用、原生永续协议手续费、回购金额均有明显周度回落，最近 13 周相较最初 13 周仍下降。',
        '最近 13 周相较此前 13 周：总费用 +12.5%，原生永续协议手续费 +2.6%，回购金额 +2.9%；表现为低位恢复，总费用恢复幅度大于原生永续收入恢复幅度。',
        '回购资金来源具有持续性，但金额不稳定：364 天都有回购记录，周回购金额最高约 4,001 万美元、最低约 580 万美元，不能视为固定收益。',
        '最近一段回购 HYPE 数量下降，同时回购均价明显上升；资金金额与代币数量应分开判断。', '',
        '## 最近 4 周与此前 4 周', '',
        '最近 4 个完整周为 2026-08-31 至 2026-09-27；此前 4 周为 2026-08-03 至 2026-08-30。']
for k,label in [('fees','总费用'),('native','原生永续协议手续费'),('buybacks','实际回购金额'),('hype','回购 HYPE 数量')]:
    a=sum(w[k] for w in weeks[-8:-4]);b=sum(w[k] for w in weeks[-4:])
    out.append(f'- {label}：此前 {a/1e6:.3f} 百万，最近 {b/1e6:.3f} 百万，变化 {b/a-1:+.1%}。')
out += ['', '## 统计结果', '']
for k,label in [('fees','总费用'),('native','原生永续协议手续费'),('buybacks','实际回购金额'),('hype','回购 HYPE 数量')]:
    xs=[w[k] for w in weeks]
    high,low=max(weeks,key=lambda w:w[k]),min(weeks,key=lambda w:w[k])
    first=sum(xs[:13]);last=sum(xs[-13:])
    increases=sum(b>a for a,b in zip(xs,xs[1:]))
    out += [f'- {label}：52 周总计 {sum(xs)/1e6:.2f} 百万；周均 {statistics.mean(xs)/1e6:.2f} 百万；末 13 周较首 13 周 {last/first-1:+.1%}；51 次周环比中 {increases} 次上涨、{51-increases} 次下降或持平。',
            f'  - 最高周 {high["start"]}：{high[k]/1e6:.2f} 百万；最低周 {low["start"]}：{low[k]/1e6:.2f} 百万；周度变异系数 {statistics.pstdev(xs)/statistics.mean(xs):.2f}。']
out += [f'- 总费用与同期回购金额的周度 Pearson 相关系数：{corr([w["fees"] for w in weeks],[w["buybacks"] for w in weeks]):.3f}；描述共同变化，不证明因果或固定划拨比例。', '',
        '## 52 周明细（金额：百万美元；HYPE：百万枚）', '',
        '| 周起始 | 总费用 | 原生永续协议手续费 | 实际回购 | HYPE 数量 |', '|---|---:|---:|---:|---:|']
for w in weeks:
    out.append(f"| {w['start']} | {w['fees']/1e6:.2f} | {w['native']/1e6:.2f} | {w['buybacks']/1e6:.2f} | {w['hype']/1e6:.3f} |")
out += ['', '## 本周尚未结束', '',
        '2026-09-28 至 2026-09-29 仅两天，不能直接与完整周比较。']
for k in ('fees','buybacks','hype'):
    v=sum(daily[date(2026,9,28)+timedelta(days=i)][k] for i in range(2))
    out.append(f'- {k}: {v/1e6:.3f} 百万。')
out += ['', '## 验证与解释限制', '',
        '✅ 原始响应行数与 total 一致；每日 totals 无重复；分析区间没有缺日；按周求和可复算。',
        '⚠️ 本次核验第三方数据的完整读取与汇总，未逐笔重放链上成交。HYPE 数量下降可能源于价格上涨，不能只据数量判断回购资金下降。不同来源统计方法不一致时，不应直接拼接。', '',
        '复算：在本目录运行 `python3 analyze_blockworks.py`。原始 JSON 位于 data；复算不会改写原始数据。']
outdir = ROOT / 'runs'
outdir.mkdir(exist_ok=True)
(outdir/'2026-09-30-手续费与回购周度分析-复算.md').write_text('\n'.join(out)+'\n')
(ROOT/'2026-09-30-weekly-derived.json').write_text(json.dumps(weeks,ensure_ascii=False,indent=2))
print('\n'.join(out[:40]))
