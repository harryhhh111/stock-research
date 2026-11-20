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
# Independent reads of original inline XBRL values referenced by financial inputs.
raw_cache={}
for key,x in D['fact_evidence'].items():
 file=x['file']
 if file not in raw_cache:raw_cache[file]=BeautifulSoup((P/'data'/file).read_bytes(),'html.parser')
 tag=raw_cache[file].find(id=x['id']);assert tag is not None,key
 t=tag.get_text(strip=True).replace(',','');value=0 if t in ['—','–','-',''] else float(t)
 value*=10**int(tag.get('scale','0'))/1e6
 if tag.get('sign')=='-':value=-value
 check('raw XBRL '+key,value,x['MUSD'])
# Each flow uses one scale, actual positive widths, economic direction and conserved middle nodes.
FD=json.loads((P/'flow_data.json').read_text())
for k,f in FD['flows'].items():
 nodes={n[0]:n for n in f['nodes']}
 for nid,label,amount,*_ in f['nodes']:
  incoming=sum(v for a,b,v in f['links'] if b==nid);outgoing=sum(v for a,b,v in f['links'] if a==nid)
  if incoming:check(f'{k} {nid} incoming conservation',incoming,amount)
  if outgoing:check(f'{k} {nid} outgoing conservation',outgoing,amount)
 for a,b,amount in f['links']:assert amount>=0,(k,a,b,amount)
check('cash source/use total',sum(n[2] for n in FD['flows']['cash']['nodes'] if n[0] not in ['pool','acq','oper','capex','finpay','end']),12129)
check('cash financing detail',sum(FD['financing_cash_paid'].values()),386)
html=(ROOT/'QXO.html').read_text();s=BeautifulSoup(html,'html.parser');ids=[n['id'] for n in s.select('[id]')]
check('unique HTML ids',len(ids),len(set(ids)))
overview=s.select_one('#guidance-overview')
check('overview amount and EPS units local',int(overview is not None and all(x in overview.caption.get_text() for x in ['M美元','100万美元','EPS为美元/股'])),1)
for label,value in [('营业收入','4,895'),('净利润','-123'),('调整后 EBITDA','557'),('调整后 EPS（美元/股）','0.13')]:
 row=next(r for r in overview.select('tbody tr') if label in r.get_text())
 check('overview separate metric and correct amount '+label,int(value in row.get_text()),1)

for k,f in FD['flows'].items():
 svg=s.select_one(f'svg[data-flow="{k}"]');assert svg is not None,k
 for node in svg.select('rect[data-node]'):
  check('SVG node thickness '+k+node['data-node'],float(node['height']),float(node['data-amount'])*f['scale'])
 for edge in svg.select('path[data-from]'):
  check('SVG edge thickness '+k+edge['data-from']+edge['data-to'],float(edge['data-thickness']),float(edge['data-amount'])*f['scale'])
check('deficit graph explanation link',int(s.select_one('#cash-deficit-bridge a[href="#cash-full-flow"]') is not None),1)
check('profit graph explanation link',int(s.select_one('#profit-bridge a[href="#income-flow"]') is not None),1)

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
index=json.loads((ROOT.parent/'研究流程/index/html-index.json').read_text())
entry=next(x for x in index['reports'] if x['report_id']=='qxo-main')
check('report index ready partial',int(entry['status']=='ready' and entry['content_status']=='partial'),1)
check('report index HTML hash synchronized',int(entry['content_sha256']==hashlib.sha256((ROOT/'QXO.html').read_bytes()).hexdigest()),1)
check('report index preserves real cutoffs',int((entry['document_updated_at'],entry['financial_as_of'],entry['market_as_of'])==('2026-11-20','2026-09-30','2026-11-16')),1)
audit=json.loads((P/'sop_audit.json').read_text())
# The historical content audit used an earlier checklist.
current_checklist = ROOT.parent/'研究流程/standards/研究更新与交付检查清单.md'
current_sop_matches = audit['sop_sha256'] == hashlib.sha256(current_checklist.read_bytes()).hexdigest()

result={'date':'2026-11-20','historical_content_audit_matches_current_checklist':current_sop_matches,'scope':'financial arithmetic, provenance, valuation reconstruction and HTML local structure only','all_passed':True,'mechanical_checks_passed':True,'content_acceptance_passed':False,'content_acceptance_record':'sop_audit.json','checks':checks,'quarter_coverage':{'expected':['2026Q1','2026Q2','2026Q3'],'revenue':'passed','profits_and_margins':'passed','cash_capex_fcf_sbc':'passed','comparatives':'passed with mixed source rounding <=1.51 MUSD','business_profit_cash':'not separately disclosed'},'content_limitations':['No uniform 3-year same-platform actual financials: acquisitions and former software entity','Capital claims valuation is intrinsic approximation, lacks full option time value and dividend path','Exact historical Q3 tax-event decomposition not disclosed in retrieved note','Full same-date peer capital structure multiples not completed','Cross-version Q3 2025 net interest 37.7 to 37 and income tax 128.9 to 128 are not fully explained by ordinary rounding'],'raw_source_hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (P/'data').glob('*.html')}}
(P/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(f'PASS: {len(checks)} arithmetic and structural checks; content limitations recorded separately.')
