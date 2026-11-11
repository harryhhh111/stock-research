"""复算2026Q3财报事件，输入官方保存HTML；金额百万美元。"""
import json,re
from pathlib import Path
from bs4 import BeautifulSoup
b=Path(__file__).resolve().parent
s=BeautifulSoup((b/'data/2026-q3.html').read_text(),'html.parser')
def row(i,label):
 for r in s.find_all('table')[i].find_all('tr'):
  c=[t.get_text(' ',strip=True) for t in r.find_all(['td','th'])]
  if c and c[0]==label:return [float(t.replace(',','').replace('(',''))*(-1 if '(' in t else 1) for t in c[1:] if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?',t)]
cfo=row(0,'Net cash provided by (used in) operating activities');cap=row(0,'Purchases of property and equipment');pro=row(0,'Proceeds from property and equipment sales and incentives')
r={'source':'https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Third-Quarter-Results/default.aspx','event_date_US':'2026-10-29','checked_date_Asia_Shanghai':'2026-10-30','units':'USD million', 'q3_cfo':cfo[1],'q3_cash_capex':abs(cap[1]),'q3_fcf_company':cfo[1]+cap[1]+pro[1],'ttm_cfo':cfo[-1],'ttm_cash_capex':abs(cap[-1]),'ttm_fcf_company':cfo[-1]+cap[-1]+pro[-1],'ttm_fcf_gross':cfo[-1]+cap[-1], 'regular_session_return_pct':(243.79/254.60-1)*100,'combined_return_at_reported_229_57_pct':(229.57/254.60-1)*100,'nasdaq_regular_return_pct':-1.4,'source_time_warning':'229.57 is media after-hours snapshot, not final/latest quote; no verified 15% observation.'}
assert r['ttm_fcf_company']==-42357
(b/'q3-event-results-2026-10-30.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(r,ensure_ascii=False))
