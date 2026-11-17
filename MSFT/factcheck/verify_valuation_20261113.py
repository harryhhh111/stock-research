import json
from pathlib import Path
p=Path(__file__).resolve().parent
d=json.loads((p/'data/valuation_2026-11-13.json').read_text());m=d['price']*d['shares'];f=d['price']*(1+d['required_return'])**d['holding_years']
r={'market_cap_B_USD':m,'pe_eps':d['price']/d['eps'],'pe_net':m/d['net_income'],'pe_openai_adjusted':d['price']/d['openai_adjusted_eps'],'fcf_yield_pct':d['fcf']/m*100,'p_fcf':m/d['fcf'],'five_year_price_required_ex_dividends':f,'scenarios':[{'terminal_pe':v,'eps_required':f/v,'eps_cagr_pct':((f/v/d['openai_adjusted_eps'])**(1/d['holding_years'])-1)*100} for v in d['terminal_pe']],'fcf_required_at_yield':{str(y):m*y for y in [.03,.04]}}
(p/'valuation_2026-11-13_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
