from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;F=json.loads((P/'data/facts.json').read_text())
metrics={
'revenue':['us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax'],
'cost':['us-gaap:CostOfRevenue','us-gaap:CostOfGoodsAndServicesSold'],
'op':['us-gaap:OperatingIncomeLoss'],'net':['us-gaap:NetIncomeLoss'],
'cfo':['us-gaap:NetCashProvidedByUsedInOperatingActivities'],
'capex':['us-gaap:PaymentsToAcquireProductiveAssets','us-gaap:PaymentsToAcquirePropertyPlantAndEquipment'],
'sbc':['us-gaap:ShareBasedCompensation'],
'equity':['us-gaap:StockholdersEquity'],'assets':['us-gaap:Assets'],
'cash':['us-gaap:CashAndCashEquivalentsAtCarryingValue'],
'interest_net':['us-gaap:InterestIncomeExpenseNonoperatingNet']}
evidence={}
def get(file,metric,start,end):
 for tag in metrics.get(metric,[metric]):
  a=[x for x in F[file] if x['tag']==tag and not x.get('dimensions') and x['start']==start and x['end']==end]
  if a:
   x=a[0];v=x['value']/1e6
   evidence[f'{file}:{metric}:{start}:{end}']={**x,'file':file+'.html','MUSD':v};return v
 return None
def period(file,start,end):
 d={m:get(file,m,start,end) for m in ['revenue','cost','op','net','cfo','capex','sbc','interest_net']}
 d['gross']=d['revenue']-d['cost'];d['fcf']=None if d['cfo'] is None else d['cfo']-d['capex'];return d
annual={}
for y,file in [(2023,'2024FY'),(2024,'2025FY'),(2025,'2025FY')]:
 d=period(file,f'{y}-01-01',f'{y}-12-31')
 for m in ['equity','assets','cash']:d[m]=get(file,m,None,f'{y}-12-31')
 annual[str(y)]=d
quarters={}
for year in [2025,2026]:
 for q,file in [(1,'2026Q1'),(2,'2026Q2'),(3,'2026Q3')]:
  start=f'{year}-{(q-1)*3+1:02d}-01';end=f'{year}-{q*3:02d}-'+('31' if q in [1,4] else '30')
  d=period(file,start,end)
  cum=period(file,f'{year}-01-01',end)
  if q>1:
   for m in ['cfo','capex','sbc']:
    if d[m] is None:d[m]=cum[m]-sum(quarters[f'{year}Q{j}'][m] for j in range(1,q))
  d['fcf']=d['cfo']-d['capex'];quarters[f'{year}Q{q}']=d
q4={m:annual['2025'][m]-period('2026Q3','2025-01-01','2025-09-30')[m] for m in ['revenue','cost','op','net','cfo','capex','sbc','interest_net','gross','fcf']};quarters['2025Q4']=q4
cum26=period('2026Q3','2026-01-01','2026-09-30');cum25=period('2026Q3','2025-01-01','2025-09-30')
ttm={m:annual['2025'][m]+cum26[m]-cum25[m] for m in ['revenue','cost','op','net','cfo','capex','sbc','interest_net','gross','fcf']}
# Product categories: source disclosed classifications, never invent divisional earnings.
products={
 '2023':{'roof':0,'insulation':0,'complement':0,'software':54.517},
 '2024':{'roof':0,'insulation':0,'complement':0,'software':56.9},
 '2025':{'roof':5191,'insulation':0,'complement':1592.7,'software':58.5},
 '2026Q1':{'roof':1262.7,'insulation':0,'complement':452.9,'software':14.6},
 '2026Q2':{'roof':2002,'insulation':0,'complement':1229,'software':15},
 '2026Q3':{'roof':1996,'insulation':1644,'complement':1240,'software':15},
 '2025Q1':{'roof':0,'insulation':0,'complement':0,'software':13.5},
 '2025Q2':{'roof':1466,'insulation':0,'complement':426,'software':14},
 '2025Q3':{'roof':2086,'insulation':0,'complement':628,'software':14}}
# Fiscal 2022 revenue from FY2024 comparative discussion, extracted tags if available.
prior_equity={2022:9.551,2023:7.471,2024:5052.9}
for y,d in annual.items():
 y=int(y);d['roe']=d['net']/((prior_equity[y-1]+d['equity'])/2)*100
 d['gross_margin']=d['gross']/d['revenue']*100;d['op_margin']=d['op']/d['revenue']*100;d['net_margin']=d['net']/d['revenue']*100
r={'annual':annual,'quarters':quarters,'cumulative':{'2025':cum25,'2026':cum26},'ttm':ttm,'products':products,'units':'MUSD, shares in million unless specified','sources':'data/sources.json','fact_evidence':evidence}
(P/'financials.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
print(json.dumps({k:r[k] for k in ['annual','quarters','ttm']},indent=2))
