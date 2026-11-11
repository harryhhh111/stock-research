"""同业最近四季TTM；冻结输入、期间和现金PP&E口径均保留。"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
inputs = json.loads((ROOT / 'data/peers_ttm_2026-11-04_inputs.json').read_text())
oracle = json.loads((ROOT / 'data/fy2027q1_inputs.json').read_text())
cols = ('revenue', 'op', 'common_net', 'cfo', 'capex', 'eps')
results = {}
for symbol in ('ORCL', 'MSFT', 'AMZN', 'GOOG'):
    item = inputs[symbol]
    if symbol == 'ORCL':
        mapping = {'op':'operating_income', 'common_net':'common_income'}
        a, c, p = (oracle[x] for x in ('fy26','fy27q1','fy26q1'))
        ttm = {k:a[mapping.get(k,k)]+c[mapping.get(k,k)]-p[mapping.get(k,k)] for k in cols}
    else:
        a,c,p = (item[x] for x in ('annual','current_interim','prior_interim'))
        ttm = {k:a[k]+c[k]-p[k] for k in cols}
    assert (date.fromisoformat(item['end'])-date.fromisoformat(item['start'])).days in (364,365)
    prior = item['prior_ttm_revenue_inputs']
    prior_revenue = prior['annual'] + prior['current_interim'] - prior['prior_interim']
    ttm.update({
        'prior_ttm_revenue':prior_revenue,
        'revenue_growth_pct':(ttm['revenue']/prior_revenue-1)*100,
        'op_margin_pct':ttm['op']/ttm['revenue']*100,
        'common_net_margin_pct':ttm['common_net']/ttm['revenue']*100,
        'fcf_uniform':ttm['cfo']-ttm['capex'],
        'capex_cfo_pct':ttm['capex']/ttm['cfo']*100,
        'capex_revenue_pct':ttm['capex']/ttm['revenue']*100,
        'pe_eps_splice_approx':item['price']/ttm['eps'],
        'period_start':item['start'], 'period_end':item['end'],
    })
    if symbol == 'AMZN':
        ttm['fcf_company'] = ttm['fcf_uniform'] + item['ttm_asset_proceeds']
        assert ttm['fcf_company'] == -42357
    results[symbol] = ttm
assert results['ORCL']['fcf_uniform'] == -28720
assert results['AMZN']['cfo'] == 168300
assert results['AMZN']['capex'] == 215192
assert results['GOOG']['fcf_uniform'] == 19747
assert results['GOOG']['common_net'] == 235310
ends = [date.fromisoformat(x['period_end']) for x in results.values()]
assert (max(ends)-min(ends)).days == 30
# 四季直接加总交叉核验Amazon，避免仅信任年度滚动公式。
q = json.loads((ROOT.parents[1] / 'AMZN/factcheck/profit-quarterly-2026.json').read_text())
mapping = {'revenue':'收入','op':'经营利润','common_net':'净利润','cfo':'CFO','capex':'购建固定资产现金支出（未扣回款）'}
for key, label in mapping.items():
    actual = sum(q[quarter][label] for quarter in ('2025Q4','2026Q1','2026Q2','2026Q3'))
    assert actual == results['AMZN'][key], (key,actual,results['AMZN'][key])
output = ROOT / 'peers_ttm_2026-11-04_results.json'
output.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
