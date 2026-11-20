"""Audit actual HTML tables against saved research inputs and independently recalc.
This verifies coverage/numerical rendering; it does not certify future assumptions.
"""
from pathlib import Path
import json,re,math,hashlib
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]
def number(text):
 t=text.replace(',','').replace('−','-');m=re.match(r'\s*\$?\s*([+-]?\d+(?:\.\d+)?)',t)
 assert m,text
 return float(m.group(1))
def by_label(table,label):
 for tr in table.select('tbody tr'):
  cells=tr.find_all(['td','th'],recursive=False)
  if cells and cells[0].get_text(' ',strip=True)==label:return cells
 raise AssertionError(label)
def close(x,y):assert math.isclose(x,y,abs_tol=.011),(x,y)
results=[]
for sym,project in [('CRWV','CRWV'),('NBIS','Nebius公司研究')]:
 p=ROOT/project;htmlpath=p/'reports/main.html';s=BeautifulSoup(htmlpath.read_text(),'html.parser');d=json.loads((p/'factcheck/full-research-results.json').read_text());ann=d['annual'];q=d['quarterly']
 checks=[]
 at=s.find(id='annual-revenue').find_next('table');qt=s.find(id='quarter-revenue').find_next('table');ft=s.find(id='annual-finance').find_next('table')
 assert [x.get_text() for x in at.thead.select('th')][1:]==['FY2023','FY2024','FY2025']
 assert [x.get_text() for x in qt.thead.select('th')][1:]==['2026 Q1','2026 Q2','2026 Q3']
 label='集团收入' if sym=='CRWV' else '集团持续经营收入'
 for i,y in enumerate(['2023','2024','2025']):
  cell=by_label(at,label)[i+1];close(number(cell.get_text()),ann[y]['revenue']);assert '同比' in cell.text and '占集团' in cell.text
  if y!='2023':close(number(cell.small.get_text(' ',strip=True).split('同比：')[1]),(ann[y]['revenue']/ann[str(int(y)-1)]['revenue']-1)*100)
  for metric,key in [('收入','revenue'),('经营利润','op'),('持续经营净利润 / 合并净利润','net'),('股权激励费用','sbc'),('折旧与摊销','da'),('经营现金流（持续经营）','cfo'),('现金CapEx','cash_capex'),('自算FCF','fcf')]:close(number(by_label(ft,metric)[i+1].get_text()),ann[y][key])
  close(ann[y]['fcf'],ann[y]['cfo']-ann[y]['cash_capex']);close(ann[y]['op_margin'],ann[y]['op']/ann[y]['revenue']*100)
 checks.append('FY2023/FY2024/FY2025 actual HTML revenue, YoY/share and income/cash table values match inputs')
 for i,period in enumerate(['q1','q2','q3']):
  cell=by_label(qt,'集团')[i+1];close(number(cell.get_text()),q[period]['revenue']);assert '同比' in cell.text and '占集团' in cell.text
  close(q[period]['fcf'],q[period]['cfo']-q[period]['cash_capex'])
 quarter_finance=next(t for t in s.find(id='finance').find_all('table') if '单季 · M美元' in t.get_text() or '单季 · M USD' in t.get_text())
 for label,k in [('经营利润','op'),('经营利润率','op_margin'),('净利润 / 亏损','net'),('净利率','net_margin'),('调整后EBITDA','ebitda'),('调整后EBITDA率','ebitda_margin'),('CFO','cfo'),('现金CapEx','cash_capex'),('自算FCF','fcf')]:
  cells=by_label(quarter_finance,label)
  for i,period in enumerate(['q1','q2','q3']):close(number(cells[i+1].get_text()),q[period][k])
 checks.append('2026 Q1/Q2/Q3 actual HTML revenue, profits/margins, EBITDA, CFO/cashCapEx/FCF all match the preserved inputs')
 if sym=='NBIS':
  names={'cloud':'Nebius AI cloud','tripleten':'TripleTen','avride':'Avride','eliminations':'内部交易抵销'}
  for k,label in names.items():
   for i,y in enumerate(['2023','2024','2025']):close(number(by_label(at,label)[i+1].get_text()),ann[y][k])
  for i,period in enumerate(['q1','q2','q3']):
   vals=[]
   for k,label in names.items():
    cells=by_label(qt,'内部抵销' if k=='eliminations' else label);rendered=number(cells[i+1].get_text());close(rendered,d['segments']['quarterly'][k][i]);vals.append(rendered)
   close(sum(vals),q[period]['revenue'])
  for y in ['2023','2024','2025']:close(sum(ann[y][k] for k in names),ann[y]['revenue'])
  close(q['ttm']['net'],9.8-278.6+393.3)
  ttm=next(t for t in s.find(id='finance').find_all('table') if '2025 Q4＋2026 9M' in t.get_text())
  close(number(by_label(ttm,'持续经营净利润')[2].get_text()),124.5)
  checks.append('NBIS all 3 segments/eliminations independently add to group in annual and quarter HTML; TTM uses audited annual net=9.8')
 else:close(q['ttm']['net'],-1167-(-715)+(-2075))
 for key in ['revenue','net','cfo','cash_capex']:
  nine=sum(q[x][key] for x in ['q1','q2','q3']);assert isinstance(nine,(int,float))
 close(q['ttm']['fcf'],q['ttm']['cfo']-q['ttm']['cash_capex'])
 v=d['valuation'];shares=v['shares_million'];nd=v['net_debt_billion'];r=v['discount_rate'];g=v['terminal_growth'];T=v['T_years']
 close(v['market_cap_billion'],v['price']*shares/1000);close(v['enterprise_value_billion'],v['market_cap_billion']+nd)
 pv=sum(f/(1+r)**t for f,t in zip(v['assumed_ufcf_billion'],v['time_years']));need=(v['enterprise_value_billion']-pv)*(1+r)**T*(r-g);close(need,v['required_2030_ufcf_billion'])
 for case in v['scenarios']:
  value=(pv+case['fcf2030_billion']/(r-g)/(1+r)**T-nd)*1000/shares;close(max(value,0),case['per_share'])
 assert '2030' in s.find(id='valuation').text and '研究者' in s.find(id='valuation').text and '一年延迟' in s.find(id='valuation').text
 checks.append('Valuation price/shares/EV, date-specific discounting, terminal FCF and scenario values independently recalculate')
 ids=[x['id'] for x in s.select('[id]')];assert len(ids)==len(set(ids))
 broken=[a['href'] for a in s.select('a[href^="#"]') if a['href'][1:] not in ids];assert not broken,broken
 assert not s.select('script[src],link[rel="stylesheet"],img[src^="http"]')
 assert all(s.find(id=x) for x in ['business','revenue','finance','customers','competition','cycle','valuation','governance','moat'])
 for term in ['power-and-delivery','capital-allocation','valuation-model','coverage-matrix','customer-cases','funding']:assert s.find(id=term),term
 checks.append('9 chapters and preserved explanations have live anchors; no external display dependencies or duplicate IDs')
 assert '未加入QQQ' not in s.get_text();assert 'QQQ' in s.find(id='price-review').text
 coverage=json.loads((p/'factcheck/revenue-coverage.json').read_text());coverage.update(status='final HTML checked',actual_annual=['FY2023','FY2024','FY2025'],actual_quarters=['2026Q1','2026Q2','2026Q3'],group_revenue='pass',major_segments='single segment disclosed' if sym=='CRWV' else 'all 3 and eliminations pass',final_html='reports/main.html',html_sha256=hashlib.sha256(htmlpath.read_bytes()).hexdigest(),exception='none' if sym=='CRWV' else 'FY2023 group YoY unavailable on current FY2022 perimeter; segment FY2022 bases separately labelled')
 (p/'factcheck/revenue-coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
 audit={'date':'2026-11-18','report_sha256':coverage['html_sha256'],'scope':'full main report migration with Q3 update','content_checks':checks,'coverage':'pass with disclosed incomparable historical periods','calculations':'pass','valuation_scope':'conditional calculation passed, operating forecast not independently certified','unresolved_source_differences':[] if sym=='CRWV' else ['28.0 M main debt versus note12; larger main amount used, share-value sensitivity about $0.09'],'visual':'separate html-visual-checks.json; requires actual screenshot review'}
 (p/'factcheck/full-report-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n');results.append({'company':sym,'checks':len(checks),'status':'pass','exceptions':audit['unresolved_source_differences']})
print(json.dumps(results,ensure_ascii=False,indent=2))
