"""从官方业绩稿生成2026逐季可比营收底表，输出JSON；不联网。"""
import json,re
from pathlib import Path
from bs4 import BeautifulSoup
B=Path(__file__).resolve().parent
soups={n:BeautifulSoup((B/'data'/f'{n}.html').read_text(),'html.parser') for n in ['2026-q2','2026-q3']}
def rows(n,i):
 out=[]
 for r in soups[n].find_all('table')[i].find_all('tr'):
  c=[t.get_text(' ',strip=True) for t in r.find_all(['td','th'])]
  if c:out.append((c[0],[float(t.replace(',','').replace('(',''))*(-1 if '(' in t else 1) for t in c[1:] if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?',t)]))
 return out
def get(n,i,label):return next(v for k,v in rows(n,i) if k==label)
result={}
for y in [2025,2026]:
 for q in [1,2,3]:
  n='2026-q3' if q==3 else '2026-q2';idx=0 if y==2025 else 1
  d={}
  for key,label in [('revenue','Total net sales'),('op','Operating income'),('ni','Net income')]:
   a=get(n,1,label);d[key]=a[idx+2]-a[idx] if q==1 else a[idx]
  sales=[v for k,v in rows(n,3) if k=='Net sales'][:3]
  ops=[v for k,v in rows(n,3) if k in ['Operating income','Operating income (loss)']][:3]
  d['segments']={name:{'revenue':v[idx+2]-v[idx] if q==1 else v[idx], 'op':o[idx+2]-o[idx] if q==1 else o[idx]} for name,v,o in zip(['北美','国际','AWS'],sales,ops)}
  assert sum(v['revenue'] for v in d['segments'].values())==d['revenue']
  d['products']={}
  labels={'线上商店':'Online stores (1)','实体店':'Physical stores (2)','第三方卖家服务':'Third-party seller services (3)','广告':'Advertising services (4)','订阅':'Subscription services (5)','AWS':'AWS','其他':'Other (6)'}
  for cn,label in labels.items():
   hits=[v for i in range(len(soups[n].find_all('table'))) for k,v in rows(n,i) if k==label and len(v)>=6]
   a=hits[0];col=5 if q==3 and y==2026 else 1 if q==3 else (4 if q==1 else 5) if y==2026 else (0 if q==1 else 1)
   d['products'][cn]=a[col]
  assert sum(d['products'].values())==d['revenue'],(y,q,d['products'])
  result[f'{y}Q{q}']=d
for q in [1,2,3]:
 a,b=result[f'2025Q{q}'],result[f'2026Q{q}']
 b['yoy_pct']=(b['revenue']/a['revenue']-1)*100
 for k,v in b['segments'].items():v.update(mix_pct=v['revenue']/b['revenue']*100,yoy_pct=(v['revenue']/a['segments'][k]['revenue']-1)*100)
(B/'revenue-quarterly-2026.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('季度分部与产品收入加总全部通过')
