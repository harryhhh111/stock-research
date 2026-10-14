"""Recalculate ROE and company-defined FCF yield; run from any directory."""
from pathlib import Path
import csv, json
root=Path(__file__).resolve().parent
with (root/'data/roe_fcf_inputs.csv').open() as f:
    v={r['metric']:float(r['value']) for r in csv.DictReader(f)}
out={}
for year in (2023,2024,2025):
    avg=(v[f'parent_equity_{year-1}']+v[f'parent_equity_{year}'])/2
    out[str(year)]={'average_parent_equity_million':avg,
        'roe_pct':v[f'parent_profit_{year}']/avg*100,
        'adjusted_roe_reference_pct':v[f'adjusted_profit_{year}']/avg*100}
cap=v['market_cap_hkd']*v['hkd_cny']
ttm=v['fcf_fy2025']-v['fcf_q1_2025']-v['fcf_q2_2025']+v['fcf_q1_2026']+v['fcf_q2_2026']
prepaid=v['fcf_q2_ex_prepaid']-v['fcf_q2_2026']
out['fcf']={'market_cap_rmb_million':cap,'ttm_rmb_million':ttm,
 'ttm_yield_pct':ttm/cap*100,'ttm_ex_q2_prepaid_rmb_million':ttm+prepaid,
 'ttm_ex_q2_prepaid_yield_pct':(ttm+prepaid)/cap*100,
 'fy2025_at_current_cap_yield_pct':v['fcf_fy2025']/cap*100}
(root/'ROE与FCF计算结果.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
