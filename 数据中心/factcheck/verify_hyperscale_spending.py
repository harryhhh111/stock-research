"""Recompute comparable cash PPE spending; source paths relative to this script."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / 'data/hyperscale_spending_2026-11-05.json'
d = json.loads(INPUT.read_text())
peer = json.loads((INPUT.parent / d['existing_peer_inputs']).resolve().read_text())
oracle = json.loads((INPUT.parent / d['existing_oracle_inputs']).resolve().read_text())
rows = {}
for symbol in ('MSFT', 'AMZN', 'GOOG'):
    x = peer[symbol]
    rows[symbol] = {k: x['annual'][k] + x['current_interim'][k] - x['prior_interim'][k]
                    for k in ('cfo', 'capex')}
m = d['meta']
rows['META'] = {k: m['annual_2025'][k]+m['nine_months_2026'][k]-m['nine_months_2025'][k]
                for k in ('cfo', 'capex', 'finance_lease_principal')}
rows['ORCL'] = {k: oracle['fy26'][k]+oracle['fy27q1'][k]-oracle['fy26q1'][k]
                for k in ('cfo', 'capex')}
for r in rows.values():
    r['fcf_before_finance_lease_principal'] = r['cfo']-r['capex']
    r['capex_to_cfo_pct'] = 100*r['capex']/r['cfo']
totals = {k:sum(r[k] for r in rows.values()) for k in ('cfo','capex','fcf_before_finance_lease_principal')}
totals['capex_to_cfo_pct'] = totals['capex']/totals['cfo']*100
growth = {s:[100*(v/x['prior_comparable']-1) for v in x['range']]
          for s,x in d['annual_guidance_million'].items() if x['prior_comparable'] is not None}
quarters = {s:{'fcf':[a-b for a,b in zip(x['cfo'],x['capex'])],
                'capex_q2_qoq_pct':100*(x['capex'][1]/x['capex'][0]-1),
                'capex_q3_qoq_pct':100*(x['capex'][2]/x['capex'][1]-1)}
            for s,x in d['calendar_quarters_2026'].items()}
out={'date':d['date'],'unit':d['unit'],'ttm':rows,'totals':totals,'guidance_growth_pct':growth,'quarters':quarters}
(BASE/'hyperscale_spending_2026-11-05_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
