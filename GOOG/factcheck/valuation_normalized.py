"""经营利润代理估值，税率和优先股股息均为研究假设，不是调整后GAAP净利润。"""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
x=json.loads((P/'2026-10-29-计算结果.json').read_text())
price=290.50;shares=12294;tax=.20;pref=19000*.0625
profit=x['ttm']['op']*(1-tax)-pref
eps=profit/shares
r={'date':'2026-10-29','price_snapshot':'2026-10-28 19:59 EDT GOOG StockAnalysis','price':price,'shares_million':shares,'assumed_tax':tax,'assumed_annual_preferred_dividend_million':pref,'ttm_op':x['ttm']['op'],'operating_earnings_proxy_million':profit,'proxy_eps':eps,'proxy_pe':price/eps,'excluded':'net interest and other non-operating items; full conversion dilution not modeled','multiple_sensitivity':{str(m):eps*m for m in [20,25,30]},'growth_sensitivity':{str(g):price/(eps*(1+g)) for g in [.2,.3]}}
(P/'2026-10-29-经营利润估值.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False,indent=2))
