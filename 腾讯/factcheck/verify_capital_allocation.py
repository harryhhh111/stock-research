from pathlib import Path
import csv,json
base=Path(__file__).resolve().parent
out={}
with (base/'data/capital_allocation.csv').open() as f:
 for r in csv.DictReader(f):
  v={k:float(x) for k,x in r.items() if k not in ('source','period') and x}
  total=v['dividend_cash_rmb_million']+v['buyback_cash_rmb_million']
  out[r['period']]={'cash_return_rmb_million':total,'return_to_fcf_pct':total/v['fcf_rmb_million']*100,
  'cash_dividend_to_profit_pct':v['dividend_cash_rmb_million']/v['parent_profit_rmb_million']*100,
  'remaining_fcf_rmb_million':v['fcf_rmb_million']-total,
  'net_share_reduction_pct':(1-v['closing_shares_million']/v['opening_shares_million'])*100,
  'incentive_offset_pct':v['issued_incentive_shares_million']/v['cancelled_shares_million']*100,
  'average_buyback_hkd':v['buyback_hkd_million']/v['bought_shares_million']}
out['h1_2026_ex_q2_compute_prepaid_return_to_fcf_pct']=63852/(42900+51400)*100
out['current_dividend_yield_pct']=5.3/428.2*100
out['dividend_growth_pct']={'2023':(3.4/2.4-1)*100,'2024':(4.5/3.4-1)*100,'2025':(5.3/4.5-1)*100}
(base/'资本分配计算结果.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
