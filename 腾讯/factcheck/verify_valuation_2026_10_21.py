import json
from pathlib import Path
base=Path(__file__).resolve().parent
d=json.loads((base/'data/valuation_2026-10-21.json').read_text())
cap_hkd=d['price_hkd']*d['shares_million_rounded']
cap=cap_hkd*d['hkd_cny']
profit=d['profit_fy2025']-d['profit_h1_2025']+d['profit_h1_2026']
adj=d['adj_profit_fy2025']-d['adj_profit_h1_2025']+d['adj_profit_h1_2026']
fcf=d['fcf_fy2025']-d['fcf_h1_2025']+d['fcf_h1_2026']
r=dict(cap_hkd_million=cap_hkd,cap_cny_million=cap,ttm_profit=profit,ttm_adjusted_profit=adj,ttm_fcf=fcf,pe=cap/profit,adjusted_pe=cap/adj,pb=cap/d['parent_equity_h1_2026'],fcf_yield=fcf/cap*100,fy2025_fcf_yield=d['fcf_fy2025']/cap*100,fcf_ex_prepaid_yield=(fcf+d['compute_prepaid'])/cap*100,dividend_yield=d['dividend_hkd']/d['price_hkd']*100,fcf_yield_if_200bn=200000/cap*100)
(base/'估值计算结果-2026-10-21.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
print(json.dumps(r,ensure_ascii=False,indent=2))
