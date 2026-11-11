"""复核第8节现金流与股数，来源：保存的官方Q3业绩稿；单位百万美元。"""
from pathlib import Path
from bs4 import BeautifulSoup
import re,json
b=Path(__file__).resolve().parent
s=BeautifulSoup((b/'data/2026-q3.html').read_text(),'html.parser')
def row(label):
 for r in s.find_all('table')[0].find_all('tr'):
  c=[x.get_text(' ',strip=True) for x in r.find_all('td')]
  if c and c[0]==label:return [float(x.replace(',','').replace('(',''))*(-1 if '(' in x else 1) for x in c[1:] if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?',x)]
cfo=row('Net cash provided by (used in) operating activities');cap=row('Purchases of property and equipment');pro=row('Proceeds from property and equipment sales and incentives');inv=row('Acquisitions, net of cash acquired, non-marketable investments, and other, net')
r={}
for name,i in [('2025Q3',0),('2026Q3',1),('2025_9m',2),('2026_9m',3)]:
 r[name]={'net_capex':-cap[i]-pro[i],'company_fcf':cfo[i]+cap[i]+pro[i],'after_acquisition_investment':cfo[i]+cap[i]+pro[i]+inv[i]}
assert r['2026_9m']['after_acquisition_investment']==-122100
r['dilution_ytd_pct']=(10811/10731-1)*100
r['aws_asset_additions_share_pct']=147236/196910*100
r['asset_addition_reconciliation']=37795+10335+147236+1544
assert r['asset_addition_reconciliation']==196910
(b/'capital-results-2026-11-04.json').write_text(json.dumps(r,indent=2)+'\n')
print('资本分配复算通过')
