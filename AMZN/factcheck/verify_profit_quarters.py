"""复算单季盈利现金流与同比/环比，输入保存的公司官方业绩稿。"""
import json,re
from pathlib import Path
from bs4 import BeautifulSoup
B=Path(__file__).resolve().parent
soups={n:BeautifulSoup((B/'data'/f'{n}.html').read_text(),'html.parser') for n in ['2025-q4','2026-q2','2026-q3']}
def row(n,i,label):
 for r in soups[n].find_all('table')[i].find_all('tr'):
  c=[z.get_text(' ',strip=True) for z in r.find_all(['td','th'])]
  if c and c[0]==label:return [float(t.replace(',','').replace('(',''))*(-1 if '(' in t else 1) for t in c[1:] if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?',t)]
labels={'收入':(1,'Total net sales'),'经营利润':(1,'Operating income'),'净利润':(1,'Net income'),'CFO':(0,'Net cash provided by (used in) operating activities'),'购建固定资产现金支出（未扣回款）':(0,'Purchases of property and equipment'),'销售成本':(1,'Cost of sales'),'资产出售及激励款':(0,'Proceeds from property and equipment sales and incentives'),'其他收益/损失净额':(1,'Other income (expense), net')}
d={}
for period,n,i in [('2025Q4','2025-q4',1),('2026Q1','2026-q2',1),('2026Q2','2026-q2',1),('2025Q3','2026-q3',0),('2026Q3','2026-q3',1)]:
 z={}
 for k,(table,label) in labels.items():
  v=row(n,table,label);a=v[i+2]-v[i] if period=='2026Q1' else v[i]
  z[k]=abs(a) if k.startswith('购建') else a
 z['毛利率']=(z['收入']-z['销售成本'])/z['收入']*100
 for k,profit in [('经营利润率','经营利润'),('净利率','净利润')]:z[k]=z[profit]/z['收入']*100
 z['公司口径FCF']=z['CFO']-z['购建固定资产现金支出（未扣回款）']+z['资产出售及激励款']
 d[period]=z
assert abs(sum(d[f'2026Q{q}']['净利润'] for q in [1,2,3])-113587)<1e-8
assert d['2026Q3']['公司口径FCF']==-33456
(B/'profit-quarterly-2026.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('单季合计与Q3 FCF核对通过')
