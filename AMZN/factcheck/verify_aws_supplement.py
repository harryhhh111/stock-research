"""AWS子文档底表复算；输入沿用已核对财报，补充输入保留来源。"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
def read(name):
    return json.loads((BASE / name).read_text())

assets = read('aws-spending-results-2026-11-04.json')
quarters = read('revenue-quarterly-2026.json')
extra = read('data/aws-supplement-inputs-2026-11-04.json')
result = {'annual': {}, 'quarters': {}, 'market': extra['market']}
for year in ('2023', '2024', '2025'):
    row = {**assets[year], **extra['annual'][year]}
    prior = extra['annual']['2022']['revenue'] if year == '2023' else assets[str(int(year)-1)]['revenue']
    row.update(revenue_yoy_pct=(row['revenue']/prior-1)*100,
               group_revenue_share_pct=row['revenue']/row['group_revenue']*100,
               group_op_share_pct=row['op']/row['group_op']*100)
    result['annual'][year] = row
for q in ('2026Q1', '2026Q2', '2026Q3'):
    prev = '2025' + q[4:]
    row = {k: v/1000 for k,v in quarters[q]['segments']['AWS'].items() if k in ('revenue','op')}
    row.update(extra['quarterly_assets'][q] if q != '2026Q3' else {k:assets[q][k] for k in ('additions','depreciation')})
    prior = {k:v/1000 for k,v in quarters[prev]['segments']['AWS'].items() if k in ('revenue','op')}
    prior.update(extra['quarterly_assets'][prev] if q != '2026Q3' else {k:assets[prev][k] for k in ('additions','depreciation')})
    row.update(op_margin_pct=row['op']/row['revenue']*100,
               group_revenue_share_pct=row['revenue']/(quarters[q]['revenue']/1000)*100,
               group_op_share_pct=row['op']/(quarters[q]['op']/1000)*100,
               yoy_pct={k:(row[k]/prior[k]-1)*100 for k in ('revenue','op','additions','depreciation')})
    result['quarters'][q] = row
for metric in ('revenue','op','additions','depreciation'):
    assert abs(sum(result['quarters'][q][metric] for q in result['quarters'])-assets['2026_9m'][metric]) < 1e-8
for index,q in enumerate(result['quarters']):
    previous = result['quarters'][list(result['quarters'])[index-1]] if index else {'revenue':128.725-93.146,'op':45.606-33.141}
    result['quarters'][q]['qoq_pct']={k:(result['quarters'][q][k]/previous[k]-1)*100 for k in ('revenue','op')}
result['ttm'] = {k: assets['2025'][k]-assets['2025_9m'][k]+assets['2026_9m'][k] for k in ('revenue','op','additions','depreciation')}
result['ttm']['op_margin_pct']=result['ttm']['op']/result['ttm']['revenue']*100
result['market_change_pp'] = {'aws_2026_vs_2025':26-29,'aws_2026_vs_2023':26-32,'google_2026_vs_2025':16-13}
result['illustrative_power']={'site_MW':100,'PUE':1.2,'IT_MW':100/1.2,'IT_MW_at_90pct':100/1.2*.9,'IT_MW_at_60pct':100/1.2*.6}
(BASE/'aws-supplement-results-2026-11-04.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('✅ 年度同比、季度同比/环比、三季累计勾稽、TTM及份额变化复算通过')
print(json.dumps({'quarters':result['quarters'],'ttm':result['ttm']},ensure_ascii=False))
