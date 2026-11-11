"""Q3 AWS经营利润变化桥；算术分解不是经营原因的独立归因。"""
from pathlib import Path
import json

base = Path(__file__).resolve().parent
data = json.loads((base/'aws-spending-results-2026-11-04.json').read_text())
a, b = data['2025Q3'], data['2026Q3']
delta = b['op'] - a['op']
scale = (b['revenue']-a['revenue'])*a['op']/a['revenue']
margin = b['revenue']*(b['op']/b['revenue']-a['op']/a['revenue'])
cost_a, cost_b = a['revenue']-a['op'], b['revenue']-b['op']
result = {
    'checked':'2026-11-04', 'units':'B美元；比例为%',
    'source':'2026Q3 10-Q Note 8及MD&A，链接见AWS.md F3',
    'periods':['2025Q3','2026Q3'],
    'operating_costs':[cost_a,cost_b],
    'operating_cost_yoy_pct':(cost_b/cost_a-1)*100,
    'profit_increase':delta,
    'revenue_scale_at_old_margin':scale,
    'margin_change_at_current_revenue':margin,
    'scale_share_pct':scale/delta*100,
    'margin_share_pct':margin/delta*100,
    'incremental_operating_margin_pct':delta/(b['revenue']-a['revenue'])*100,
    'cost_excluding_DA':[cost_a-a['depreciation'],cost_b-b['depreciation']],
    'cost_excluding_DA_yoy_pct':((cost_b-b['depreciation'])/(cost_a-a['depreciation'])-1)*100,
    'caveat':'先按上年利润率估收入规模效应，再按本期收入估利润率效应；分解次序影响归属，不等同AI、芯片或降本的因果贡献。剔折旧成本也不是现金成本。'
}
assert abs(scale+margin-delta)<1e-10
(base/'aws-growth-bridge-2026-11-04.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
