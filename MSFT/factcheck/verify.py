import json
from pathlib import Path
p=Path(__file__).resolve().parent
d=json.loads((p/'data/inputs.json').read_text())
a=d['annual']; results={}
for y,v in a.items():
 v['fcf']=v['cfo']-v['capex']
 v['roe']=v['net']/((a.get(str(int(y)-1),{'equity':206.223})['equity']+v['equity'])/2)*100
 for k in ['gross','op','net','fcf']:v[k+'_margin']=v[k]/v['revenue']*100
for group in ['old_segments','products']:
 for i,y in enumerate(a): assert abs(sum(v[i] for v in d[group].values())-a[y]['revenue'])<0.001
assert abs(sum(v[1] for v in d['q_products'].values())-d['q1_2027']['revenue'])<0.001
results['annual']=a
results['ttm']={k:a['2026'][k]-d['q1_2026'][k]+d['q1_2027'][k] for k in ['revenue','gross','op','net','cfo','capex']}
t=results['ttm'];t['fcf']=t['cfo']-t['capex'];t['eps']=17.95-3.72+4.92;t['adjusted_eps_openai']=17.28-4.13+4.89
m=d['price']*d['shares'];results['valuation']={'market_cap':m,'ev_ex_leases':m+d['debt']-d['cash_securities'],'ev_finance_leases':m+d['debt']+d['finance_lease']-d['cash_securities'],'pe':d['price']/t['eps'],'pe_openai_adjusted':d['price']/t['adjusted_eps_openai'],'fcf_yield':t['fcf']/m*100,'pb':m/d['equity_latest']}
(p/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps(results,ensure_ascii=False,indent=2))
