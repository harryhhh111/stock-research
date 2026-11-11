"""从已保存的官方业绩稿复算；运行 python AMZN/factcheck/verify.py。金额为百万美元。"""
import json
import re
from functools import lru_cache
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent

@lru_cache(None)
def rows(name, index):
    soup = BeautifulSoup((BASE / 'data' / f'{name}.html').read_text(), 'html.parser')
    out = []
    for row in soup.find_all('table')[index].find_all('tr'):
        cells = [c.get_text(' ', strip=True) for c in row.find_all(['td', 'th'])]
        if not cells:
            continue
        nums = []
        for cell in cells[1:]:
            if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?', cell):
                nums.append(float(cell.replace(',', '').replace('(', '')) * (-1 if '(' in cell else 1))
        out.append((cells[0], nums))
    return out

def get(name, index, label):
    aliases = {'Net income':'Net income (loss)', 'Diluted earnings per share':'Diluted earnings (loss) per share', 'Income before income taxes':'Income (loss) before income taxes', 'Provision for income taxes':'Benefit (provision) for income taxes'}
    return next(v for k, v in rows(name, index) if k in [label, aliases.get(label)])

labels = {
    'revenue': (1, 'Total net sales'), 'cost_sales': (1, 'Cost of sales'),
    'op': (1, 'Operating income'), 'ni': (1, 'Net income'),
    'interest': (1, 'Interest expense'), 'other_income': (1, 'Other income (expense), net'),
    'pretax': (1, 'Income before income taxes'), 'tax': (1, 'Provision for income taxes'),
    'eps': (1, 'Diluted earnings per share'),
    'cfo': (0, 'Net cash provided by (used in) operating activities'),
    'capex': (0, 'Purchases of property and equipment'),
    'asset_proceeds': (0, 'Proceeds from property and equipment sales and incentives'),
    'sbc': (0, 'Stock-based compensation'),
}
periods = {}
for period, name, col in [('2022','2023-q4',-2),('2023','2024-q4',-2),
                          ('2024','2025-q4',-2),('2025','2025-q4',-1),
                          ('2025H1','2026-q2',2),('2026H1','2026-q2',3)]:
    d = {k: get(name, idx, label)[col] for k, (idx, label) in labels.items()}
    d['capex'] = abs(d['capex'])
    d['fcf_gross'] = d['cfo'] - d['capex']
    d['fcf_company'] = d['fcf_gross'] + d['asset_proceeds']
    d['net_capex'] = d['capex'] - d['asset_proceeds']
    d['gross_margin_pct'] = (d['revenue']-d['cost_sales'])/d['revenue']*100
    d['op_margin_pct'] = d['op']/d['revenue']*100
    d['net_margin_pct'] = d['ni']/d['revenue']*100
    d['capex_revenue_pct'] = d['capex']/d['revenue']*100
    periods[period] = d
for year in ['2023','2024','2025']:
    d=periods[year]; prev=periods[str(int(year)-1)]
    d['revenue_yoy_pct']=(d['revenue']/prev['revenue']-1)*100
    d['op_yoy_pct']=(d['op']/prev['op']-1)*100
    d['roe_pct']=d['ni']/({'2023':(146043+201875)/2,'2024':(201875+285970)/2,'2025':(285970+411065)/2}[year])*100
    d['roic_proxy_pct']=d['op']*(1-abs(d['tax'])/d['pretax'])/({'2023':None,'2024':((201875+66808+12109-86780)+(285970+57640+10602-101202))/2,'2025':((285970+57640+10602-101202)+(411065+68396+12286-123029))/2}[year] or 1)*100 if year!='2023' else None

ttm = {k:periods['2025'][k]+periods['2026H1'][k]-periods['2025H1'][k]
       for k in ['revenue','op','ni','cfo','capex','net_capex','fcf_gross','fcf_company','sbc','other_income','pretax','tax']}
price, shares, debt, cash_sec, finance_lease = 254.60, 10783, 132224, 122988, 13451
marketcap=price*shares
ev=marketcap+debt+finance_lease-cash_sec
taxrate=abs(ttm['tax'])/ttm['pretax']
normalized=ttm['ni']-ttm['other_income']*(1-taxrate)
valuation={'price':price,'price_date':'2026-10-28 close US','shares_date':'2026-06-30',
 'marketcap':marketcap,'ev_finance_leases_only':ev,'pe_fy2025':marketcap/periods['2025']['ni'],
 'pe_ttm':marketcap/ttm['ni'],'pe_ex_other_income_sensitivity':marketcap/normalized,
 'normalized_ni_sensitivity':normalized,'ev_op_ttm':ev/ttm['op'],
 'fcf_yield_gross_pct':ttm['fcf_gross']/marketcap*100,
 'fcf_yield_company_pct':ttm['fcf_company']/marketcap*100,'pb':marketcap/551620}
segments={}
for year,name,col in [('2022','2023-q4',-2),('2023','2024-q4',-2),('2024','2025-q4',-2),('2025','2025-q4',-1),('2025H1','2026-q2',2),('2026H1','2026-q2',3)]:
    sales=[v[col] for k,v in rows(name,3) if k=='Net sales'][:3]
    ops=[v[col] for k,v in rows(name,3) if k in ['Operating income','Operating income (loss)','Operating loss']][:3]
    assert sum(sales)==periods[year]['revenue']
    assert sum(ops)==periods[year]['op']
    segments[year]={n:{'sales':s,'op':o,'mix_pct':s/periods[year]['revenue']*100,'margin_pct':o/s*100,'profit_share_pct':o/periods[year]['op']*100} for n,s,o in zip(['North America','International','AWS'],sales,ops)}
for year in ['2023','2024','2025','2026H1']:
    prev=str(int(year)-1) if year.isdigit() else '2025H1'
    for name,d in segments[year].items():d['yoy_pct']=(d['sales']/segments[prev][name]['sales']-1)*100
assert periods['2025']['fcf_company']==11194
assert ttm['fcf_company']==-7604
result={'units':'USD million, except price and EPS','periods':periods,'segments':segments,'ttm_20260630':ttm,'valuation':valuation}
products=json.loads((BASE/'data'/'product-inputs.json').read_text())
result['products']={}
for i, period in enumerate(products['columns']):
    total=periods[period]['revenue']
    assert sum(v[i] for v in products['products'].values())==total
    result['products'][period]={name:{'revenue':v[i], 'mix_pct':v[i]/total*100,
        'yoy_pct':(v[i]/v[4 if i==5 else i-1]-1)*100 if i in [1,2,3,5] else None}
        for name,v in products['products'].items()}
result['valuation_scenarios']={
 'required_fcf_year5':marketcap*1.1**5/25,
 'equity_pv_by_year5_fcf':{str(f):f*25/1.1**5 for f in [100000,150000,200000]},
 'required_fcf_by_exit_multiple':{str(v):marketcap*1.1**5/v for v in [20,25,30]},
 'required_fcf_by_discount':{str(r):marketcap*(1+r)**5/25 for r in [.08,.10,.12]}}
(BASE/'results-2026-10-30.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
