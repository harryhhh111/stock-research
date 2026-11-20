"""Build annual/quarterly research inputs from preserved filings; standard library.
The HTML-to-row extraction is preserved in annual-table-extracts.json.
"""
from pathlib import Path
import json,re,math,datetime
ROOT=Path(__file__).resolve().parents[2]
C=ROOT/'CRWV'; N=ROOT/'Nebius公司研究'
def clean(s):return re.sub(r'\s+',' ',s.replace('\u200b','')).strip()
def numbers(cells):
 out=[]
 for cell in cells:
  t=clean(cell).replace('$','').replace(',','').replace(' ','')
  if t in ['—','–']:out.append(0.0)
  elif re.fullmatch(r'\(?-?\d+(?:\.\d+)?\)?',t):out.append(float(t.strip('()'))*(-1 if t.startswith('(') else 1))
 return out
def row(rows,label,n,occurrence=0):
 matches=[r for r in rows if r and clean(r[0])==label]
 if not matches:raise ValueError(label)
 return numbers(matches[occurrence][1:])[-n:]
def build():
 cx=json.loads((C/'factcheck/data/annual-table-extracts.json').read_text())['tables'];nx=json.loads((N/'factcheck/data/annual-table-extracts.json').read_text())['tables']
 annual={s:{} for s in ['CRWV','NBIS']}
 cm={'revenue':('226','Revenue'),'cost':('226','Cost of revenue'),'interest_signed':('226','Interest expense, net'),'op':('226','Operating income (loss)'),'net':('226','Net loss and comprehensive loss'),'common_net':('226','Net loss attributable to common stockholders, basic'),'sbc':('374','Stock-based compensation expense'),'da':('374','Depreciation and amortization'),'cfo':('374','Net cash provided by operating activities'),'capex_signed':('374','Purchase of property and equipment, including capitalized internal-use software'),'preferred_dividends_signed':('374','Redeemable convertible preferred stock cash dividends paid'),'eps':('226','Net loss per share attributable to common stockholders, basic (in usd per share )')}
 for key,(i,label) in cm.items():
  vals=row(cx[i],label,3)
  assert len(vals)==3,(key,vals)
  for year,v in zip(['2025','2024','2023'],vals):annual['CRWV'].setdefault(year,{})[key]=v
 nm={'revenue':('413','Revenues'),'cost':('413','Cost of revenues (1)'),'interest_signed':('413','Interest expense'),'op':('413','Loss from operations'),'net':('413','Net income / (loss) from continuing operations'),'parent_net':('413','Net income / (loss) attributable to Nebius Group N.V.'),'sbc':('417','Share-based compensation expense'),'cfo':('417','Net cash provided by / (used in) operating activities – continuing operations'),'capex_signed':('417','Purchases of property and equipment and intangible assets'),'cloud':('502','Nebius'),'avride':('502','Avride'),'tripleten':('502','TripleTen'),'eliminations':('502','Eliminations')}
 for key,(i,label) in nm.items():
  vals=row(nx[i],label,3)
  assert len(vals)==3,(key,vals)
  for year,v in zip(['2023','2024','2025'],vals):annual['NBIS'].setdefault(year,{})[key]=v
 for i,y in enumerate(['2023','2024','2025']):
  z=annual['NBIS'][y];z['da']=[29.3,77.1,417.9][i];z['ebitda']=[-240.7,-226.3,-64.9][i];z['cloud_ebitda']=[-134.1,-128.5,59.0][i];z['avride_ebitda']=[-69.6,-67,-82.7][i];z['tripleten_ebitda']=[-37,-30.8,-41.2][i]
  assert math.isclose(z['cloud']+z['avride']+z['tripleten']+z['eliminations'],z['revenue'],abs_tol=.01)
 for s in annual:
  for y,z in annual[s].items():
   z['interest_expense']=-z.pop('interest_signed');z['cash_capex']=-z.pop('capex_signed');z['fcf']=z['cfo']-z['cash_capex']
   for k in ['op','net']:z[k+'_margin']=z[k]/z['revenue']*100
   z['gross_margin_ex_separate_da']=(z['revenue']-z['cost'])/z['revenue']*100
   if y!='2023':z['revenue_yoy_pct']=(z['revenue']/annual[s][str(int(y)-1)]['revenue']-1)*100
 annual['CRWV']['2023']['revenue_yoy_pct']=(229/15.830-1)*100
 # Year-end balance snapshots; 2023 NBIS legal parent still included disposed Russian assets.
 cb={}
 for key,label in [('cash','Cash and cash equivalents'),('debt_current','Debt, current'),('debt_noncurrent','Debt, non-current'),('equity',"Total stockholders' equity (deficit)")]:
  for y,v in zip(['2025','2024'],row(cx['90'],label,2)):cb.setdefault(y,{})[key]=v
 nb={}
 for key,label in [('cash','Cash and cash equivalents'),('debt_current','Debt, current'),('debt_noncurrent','Debt, non-current'),('equity','Total shareholders’ equity')]:
  for y,v in zip(['2024','2025'],row(nx['412'],label,2)):nb.setdefault(y,{})[key]=v
 for y,z in cb.items():z['debt']=z['debt_current']+z['debt_noncurrent'];z['net_debt']=z['debt']-z['cash']
 for y,z in nb.items():z['debt']=z['debt_current']+z['debt_noncurrent'];z['net_debt']=z['debt']-z['cash']
 cb['2023']={'cash':217.147,'debt_current':171.865,'debt_noncurrent':1351.389,'debt':1523.254,'net_debt':1306.107,'equity':-596.591}
 nb['2023']={'cash_continuing_including_restricted':114.1,'equity':3293.7,'entity_boundary':'pre-divestment parent, assets include Russian discontinued operations'}
 roe={'NBIS':{'2023':241.3/((4488.8+3293.7)/2)*100,'2024':-641.4/((3293.7+3253.7)/2)*100,'2025':82.5/((3253.7+4594.0)/2)*100},'CRWV':{'2023':None,'2024':None,'2025':-1196/((-414+3335)/2)*100}}
 # Valuation is an explicitly conditional cash-flow reverse calculation, not consensus.
 market=json.loads((C/'factcheck/data/full-rebuild/market-snapshot.json').read_text())
 quarterly={'CRWV':json.loads((C/'factcheck/q3-2026-results.json').read_text()),'NBIS':json.loads((N/'factcheck/q3-2026-results.json').read_text())}
 # Q4 2025 recomputed from FY2025 annual and the latest 9M2025 comparison, not preliminary press-release earnings.
 quarterly['NBIS']['q4_2025']={'revenue':529.8-302.1,'op':-611.7-(-361.7),'net':9.8-278.6,'cfo':401.9-(-432.4),'cash_capex':4066-2010,'da':417.9-223.3}
 for period,value in zip(['q1','q2','q3'],[-63.7,-119.1,-112.5]):quarterly['NBIS'][period]['interest']=value
 q4=quarterly['NBIS']['q4_2025']
 for k in ['revenue','op','net','cfo','cash_capex']:
  quarterly['NBIS']['ttm'][k]=q4[k]+sum(quarterly['NBIS'][q][k] for q in ['q1','q2','q3'])
 quarterly['NBIS']['ttm']['fcf']=quarterly['NBIS']['ttm']['cfo']-quarterly['NBIS']['ttm']['cash_capex']
 segments={'annual':{k:{y:annual['NBIS'][y][k] for y in ['2023','2024','2025']} for k in ['cloud','tripleten','avride','eliminations']},'quarterly':{'cloud':[389.7,574.9,973.8],'tripleten':[11.6,10,9.0],'avride':[.9,1.0,1.3],'eliminations':[-3.2,-3.6,-3.3]},'quarterly_prior':{'cloud':[41.4,93.7,131.1],'tripleten':[10.5,12.3,16.2],'avride':[.2,.2,.2],'eliminations':[-1.2,-1.1,-1.4]},'quarterly_ebitda':{'cloud':[174,285.7,518.2],'avride':[-34.1,-40.1,-45.5],'tripleten':[-10.4,-9.4,-6.9]}}
 for i,q in enumerate(['q1','q2','q3']):assert math.isclose(sum(v[i] for v in segments['quarterly'].values()),quarterly['NBIS'][q]['revenue'],abs_tol=.01)
 # The cash-flow endpoint is the year-end 2029; 2030 FCF is the first terminal-year flow.
 base_date=datetime.date(2026,11,16);target=datetime.date(2029,12,31);T=(target-base_date).days/365.25;r=.12;g=.03
 time=[(datetime.date(y,12,31)-base_date).days/365.25 for y in [2026,2027,2028,2029]]
 vals={}
 for s in ['CRWV','NBIS']:
  m=market[s];p=m['close'];shares=m['economic_shares_million'];nd=quarterly[s]['balance']['net_debt_ex_leases'];equity=p*shares/1000;ev=equity+nd/1000
  cash_path=[-2,-5,-3,0] if s=='CRWV' else [-4,-15,-7,0]
  pv_path=sum(v/(1+r)**t for v,t in zip(cash_path,time))
  needed=(ev-pv_path)*(1+r)**T*(r-g)
  rows=[]
  for label,fcf in [('兑现偏低',needed*.7),('支撑基准价',needed),('兑现更强',needed*1.3)]:
   terminal=fcf/(r-g);pvterm=terminal/(1+r)**T;equity_val=pv_path+pvterm-nd/1000;value=max(equity_val,0)*1000/shares
   rows.append({'scenario':label,'fcf2030_billion':fcf,'terminal_value_billion':terminal,'pv_terminal_billion':pvterm,'pv_operating_billion':pv_path+pvterm,'equity_billion_before_floor':equity_val,'per_share':value,'upside_pct':(value/p-1)*100,'terminal_pv_share_of_EV_pct':pvterm/(pv_path+pvterm)*100})
  # Delay includes an additional year of negative FCF, not merely discounting the same value.
  extra_burn=-3 if s=='CRWV' else -7
  delayed_ev=pv_path+extra_burn/(1+r)**(T+1)+needed/(r-g)/(1+r)**(T+1)
  delay_price=max(delayed_ev-nd/1000,0)*1000/shares
  sensitivity=[]
  for rr in [.10,.12,.14]:
   pp=sum(v/(1+rr)**t for v,t in zip(cash_path,time));line=[]
   for gg in [.02,.03,.04]:line.append(max(pp+needed/(rr-gg)/(1+rr)**T-nd/1000,0)*1000/shares)
   sensitivity.append({'discount_rate':rr,'values_for_g_2_3_4pct':line})
  vals[s]={'price_date':'2026-11-16','price':p,'shares_million':shares,'market_cap_billion':equity,'net_debt_billion':nd/1000,'enterprise_value_billion':ev,'discount_rate':r,'terminal_growth':g,'T_years':T,'cash_flow_dates':['2026-12-31','2027-12-31','2028-12-31','2029-12-31'],'time_years':time,'assumed_ufcf_billion':cash_path,'pv_interim_billion':pv_path,'required_2030_ufcf_billion':needed,'required_revenue_at_fcf_margin_15_20_25pct_billion':[needed/a for a in [.15,.20,.25]],'scenarios':rows,'delay_extra_ufcf_billion':extra_burn,'delay_one_year_price':delay_price,'sensitivity':sensitivity,'model_status':'Conditional reverse DCF; transition cash flows and discount/growth assumptions are researcher assumptions, not forecasts or user-confirmed values; no PE skill model.'}
 data={'date':'2026-11-18','annual':annual,'annual_balance':{'CRWV':cb,'NBIS':nb},'roe_pct':roe,'quarterly':quarterly,'segments':segments,'market':market,'valuation':vals}
 for s,project in [('CRWV',C),('NBIS',N)]:
  out={'annual':annual[s],'annual_balance':data['annual_balance'][s],'roe_pct':roe[s],'quarterly':quarterly[s],'market':market[s],'valuation':vals[s]}
  if s=='NBIS':out['segments']=segments
  (project/'factcheck/full-research-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 return data
if __name__=='__main__':
 d=build();print(json.dumps({'annual_periods':{s:sorted(v) for s,v in d['annual'].items()},'valuation_required2030FCF_B':{s:v['required_2030_ufcf_billion'] for s,v in d['valuation'].items()}},ensure_ascii=False,indent=2))
