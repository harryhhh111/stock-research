from pathlib import Path
import requests,json,concurrent.futures
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent/'data'
urls={
'2026Q3':'https://www.sec.gov/Archives/edgar/data/1236275/000162828026073568/qxo-20260930.htm',
'2025FY':'https://www.sec.gov/Archives/edgar/data/1236275/000162828026012601/qxo-20251231.htm',
'2024FY':'https://www.sec.gov/Archives/edgar/data/1236275/000162828025009626/qxo-20241231.htm',
'2026Q2':'https://www.sec.gov/Archives/edgar/data/1236275/000162828026056919/qxo-20260630.htm',
'2026Q1':'https://www.sec.gov/Archives/edgar/data/1236275/000162828026034130/qxo-20260331.htm',
'2026Q3release':'https://www.sec.gov/Archives/edgar/data/1236275/000162828026073410/qxoq3-26earningsrelease.htm',
'2026proxy':'https://www.sec.gov/Archives/edgar/data/1236275/000110465926033501/tm267778-6_def14a.htm'}
if (P/'sources.json').exists():
 urls=json.loads((P/'sources.json').read_text())
def get(kv):
 k,u=kv
 if (P/(k+'.html')).exists(): return k,'preserved existing raw evidence'
 r=requests.get(u,headers={'User-Agent':'Independent research research@example.com'},timeout=45)
 if r.status_code!=200:return k,r.status_code
 (P/(k+'.html')).write_bytes(r.content)
 s=BeautifulSoup(r.content,'html.parser')
 for n in s(['script','style','ix:header']):n.decompose()
 (P/(k+'.txt')).write_text(s.get_text(' ',strip=True))
 tables=[]
 for i,t in enumerate(s.find_all('table')):
  rows=[' | '.join(tr.stripped_strings) for tr in t.find_all('tr')]
  tables.append(f'TABLE {i}\n'+'\n'.join(rows))
 (P/(k+'-tables.txt')).write_text('\n\n'.join(tables))
 return k,r.status_code,len(r.content)
if __name__=='__main__':
 print(list(concurrent.futures.ThreadPoolExecutor(max_workers=5).map(get,urls.items())))
 (P/'sources.json').write_text(json.dumps(urls,indent=2))
