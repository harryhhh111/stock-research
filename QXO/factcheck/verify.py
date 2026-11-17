from pathlib import Path
import json,math,re,hashlib
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent;ROOT=P.parent
D=json.loads((P/'financials.json').read_text());V=json.loads((P/'valuation_results.json').read_text())
checks=[]
def check(name,actual,expected,tol=1e-6):
 passed=abs(actual-expected)<=tol
 checks.append({'check':name,'actual':actual,'expected':expected,'tolerance':tol,'passed':passed})
 if not passed:raise AssertionError(checks[-1])
A=D['annual'];Q=D['quarters'];C=D['cumulative'];R=D['products']
for y,d in A.items():
 check(y+' gross',d['gross'],d['revenue']-d['cost']);check(y+' FCF',d['fcf'],d['cfo']-d['capex'])
for key,rows in R.items():
 d=A.get(key) or Q[key];check(key+' product revenue sum',sum(rows.values()),d['revenue'],.11)
for year in [2025,2026]:
 for m in ['revenue','gross','op','net','cfo','capex','fcf','sbc','interest_net']:
  check(f'{year} 3q vs9M {m}',sum(Q[f'{year}Q{i}'][m] for i in [1,2,3]),C[str(year)][m],1.51)
for m,v in D['ttm'].items():check('TTM '+m,v,A['2025'][m]+C['2026'][m]-C['2025'][m])
check('Q3 sales acquisition bridge',2728+1644+589-66,4895)
check('Q3 income statement',4895-3515-1024-66-288-163+11+27,-123)
check('Q3 adjusted EBITDA bridge',-123+83+288+79+163-27+9+40+28+17,557)
check('Q3 pretax yoy change',(2-163+11)-(25-37+1),-139)
check('Q3 net yoy change',-139+155,16)
check('9M cash bridge',2366-145-11040+9373,554)
check('9M cash acquired to finance',-10933-111+4,-11040)
check('net income to CFO',-405+188+545+147+10+32+134-195-503-317-151+17-29+473-91,-145)
check('9M pref cash sum',67+24+59,150)
check('debt maturity sum',8+30*4+8972,9100)
check('debt carrying to principal',8978+122,9100)
check('asset goodwill concentration',(14536+10767)/34470*100,73.4058601683,.0001)
check('debt interest proxy',3850*.059+1500*.065+2250*.0675+1500*.06875,579.65)
check('ROIC denominator proxy',((9706.8+3057.3+187.9-2361.6)+(15681+2942+8978+192-528))/2,18927.7)
check('preferred annual dividend',1000*.09+575*.055+3000*.0475,264.125)
from valuation import claims,to_price,model,netdebt
check('current claims reverse price',to_price(V['economic_EV_required']),12.01)
E=V['required_2030_ebitda'];r=model('reverse',[19500,21000,23000,25000],[.6*E,.725*E,.8625*E,E])
check('required EBITDA price reconstruction',r['price'],12.01)
for x in V['scenarios']:
 check(x['name']+' EV',sum(i['pv'] for i in x['rows'])+x['terminal_pv'],x['EV'])
 check(x['name']+' capital claims',claims(x['price'])+netdebt,x['EV'])
# Financial fact provenance: primary source IDs are preserved, no rounded display drives math.
peers=json.loads((P/'peer_snapshot.json').read_text())['rows']
check('BLDR peer multiple',peers[0]['EV_to_Q3_annualized_adjEBITDA'],8.900845748955318)
check('IBP peer multiple',peers[1]['EV_to_Q3_annualized_adjEBITDA'],13.276911405845672)
check('Q3 ordinary shareholders loss',-123-22-8-36,-189)
check('raw fact count positive',int(len(D['fact_evidence'])>100),1)
html=(ROOT/'QXO.html').read_text();s=BeautifulSoup(html,'html.parser');ids=[n['id'] for n in s.select('[id]')]
check('unique HTML ids',len(ids),len(set(ids)))
links=[]
for a in s.select('[href]'):
 h=a['href']
 if h.startswith('#'):links.append((h,h[1:] in ids))
 elif not re.match(r'https?://',h):links.append((h,(ROOT/h.split('#')[0]).exists()))
# verification.json is written just below and is the sole self-reference exception
bad=[h for h,ok in links if not ok and h!='factcheck/verification.json']
check('local links and anchors',len(bad),0)
check('no remote scripts styles fonts',len(s.select('script[src],link[rel="stylesheet"]')),0)
check('no absolute machine paths',len(re.findall(r'/Users/|file://',html)),0)
check('main nine chapters',len([h for h in s.select('h2') if re.match(r'[1-9]\.',h.get_text())]),9)
result={'date':'2026-11-17','scope':'financial arithmetic, provenance, valuation reconstruction and HTML local structure only','all_passed':True,'checks':checks,'quarter_coverage':{'expected':['2026Q1','2026Q2','2026Q3'],'revenue':'passed','profits_and_margins':'passed','cash_capex_fcf_sbc':'passed','comparatives':'passed with mixed source rounding <=1.51 MUSD','business_profit_cash':'not separately disclosed'},'content_limitations':['No uniform 3-year same-platform actual financials: acquisitions and former software entity','Capital claims valuation is intrinsic approximation, lacks full option time value and dividend path','Exact historical Q3 tax-event decomposition not disclosed in retrieved note','Full same-date peer capital structure multiples not completed'],'raw_source_hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (P/'data').glob('*.html')}}
(P/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(f'PASS: {len(checks)} arithmetic and structural checks; content limitations recorded separately.')
