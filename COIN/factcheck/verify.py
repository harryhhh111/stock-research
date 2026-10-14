"""复算研究报告指标。仅使用标准库；输入为带来源的人工转录值。"""
import json
from pathlib import Path

base = Path(__file__).resolve().parent
d = json.loads((base / "data/financial_inputs.json").read_text())
ttm = {k: d['annual_2025'][k] - d['h1_2025'][k] + d['h1_2026'][k]
       for k in d['annual_2025']}
q = d['q2_2026']
assert abs(sum(v for k, v in q.items() if k != 'revenue') - q['revenue']) < .001
for key in ['shares_2025', 'shares_h1_2026']:
    s = d[key]
    assert abs(s['start'] + s['acquisition'] + s['awards'] - s['repurchase'] - s['withheld'] - s['end']) < .001
cap = d['price'] * d['shares_h1_2026']['end']
b = d['balance']
net_cash = b['cash'] - b['long_debt'] - b['short_borrow']
out = {
    'status': '✅ 收入组成与股数变动核对通过',
    'ttm_million_usd': ttm,
    'market_cap_proxy_million_usd': cap,
    'net_cash_proxy_million_usd': net_cash,
    'ev_proxy_million_usd': cap - net_cash,
    'ps': cap / ttm['revenue'],
    'ev_adjusted_ebitda': (cap-net_cash)/ttm['ebitda'],
    'cfo_yield': ttm['cfo']/cap,
    'cfo_minus_sbc_proxy_yield': (ttm['cfo']-ttm['sbc'])/cap,
    'h1_revenue_yoy': d['h1_2026']['revenue']/d['h1_2025']['revenue']-1,
    'q2_revenue_mix': {k:v/q['revenue'] for k,v in q.items() if k!='revenue'},
    'h1_share_change': d['shares_h1_2026']['end']/d['shares_h1_2026']['start']-1,
    'valuation_scenarios': [
        {'assumed_normal_net_income_million':n,'assumed_pe':pe,'value_million':n*pe,'price_proxy':n*pe/d['shares_h1_2026']['end']}
        for n,pe in [(1000,20),(2000,25),(3000,30)]
    ]
}
(base/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
