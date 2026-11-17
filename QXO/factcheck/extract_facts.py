from pathlib import Path
from bs4 import BeautifulSoup
import json,re
P=Path(__file__).resolve().parent/'data'
allfacts={}
for f in P.glob('*.html'):
 s=BeautifulSoup(f.read_bytes(),'html.parser');cs={}
 for c in s.find_all(lambda t:t.name and t.name.lower()=='xbrli:context'):
  def txt(n):
   x=c.find(lambda t:t.name and t.name.lower()=='xbrli:'+n);return x.get_text(strip=True) if x else None
  cs[c.get('id')]={'start':txt('startdate'),'end':txt('enddate') or txt('instant'),'dimensions':[(m.get('dimension'),m.get_text(strip=True)) for m in c.find_all(lambda t:t.name and t.name.lower()=='xbrldi:explicitmember')]}
 fs=[]
 for n in s.find_all(lambda t:t.name and t.name.lower()=='ix:nonfraction'):
  tx=n.get_text(strip=True).replace(',','').replace('$','').replace('−','-')
  try:v=float(tx) if tx not in ['—','–','-',''] else 0
  except ValueError:continue
  v=v*10**int(n.get('scale','0'))*(-1 if n.get('sign')=='-' else 1)
  fs.append({'tag':n.get('name'),'value':v,'unit':n.get('unitref'),'decimals':n.get('decimals'),'id':n.get('id'),**cs.get(n.get('contextref'),{})})
 allfacts[f.stem]=fs
(P/'facts.json').write_text(json.dumps(allfacts,ensure_ascii=False,indent=2))
if __name__=='__main__':
 for k,fs in allfacts.items():
  print(k,len(fs))
  if k in ['2025FY','2024FY','2026Q3']:
   tags=sorted(set(x['tag'] for x in fs if not x.get('dimensions') and re.search('Revenue|NetIncome|NetCash|CapitalExpenditure|PaymentsToAcquireProperty|OperatingIncome|CostOf|GrossProfit|StockholdersEquity|CommonStockSharesOutstanding',x['tag'] or '')))
   print(tags)
