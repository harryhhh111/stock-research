"""Conditional enterprise valuation, MUSD and millions of shares; no forecast is consensus."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
price=12.01
capital={'common':1039.958653,'prefunded':42.,'existing_awards':33.4,'A_conversion':219.,'A_floor':1000.,'B_shares_low':34.84845,'B_shares_high':28.44755,'B_stated':575.,'C_conversion':3000/23.25,'C_floor':3000.,'debt_principal':9100.,'finance_leases':192.,'cash':528.,'warrants':[(109.5,4.566),(54.75,6.849),(54.75,13.698)]}
# Intrinsic-value approximation to capital claims. B's future settlement price is approximated by model price.
# No claim to option time value or a unique market-implied expectation.
def claims(p):
 c=capital;B=c['B_shares_low']*p if p<16.5 else c['B_stated'] if p<=20.2126 else c['B_shares_high']*p
 return (c['common']+c['prefunded']+c['existing_awards'])*p+max(c['A_floor'],c['A_conversion']*p)+B+max(c['C_floor'],c['C_conversion']*p)+sum(n*max(p-k,0) for n,k in c['warrants'])
netdebt=capital['debt_principal']+capital['finance_leases']-capital['cash']
def to_price(ev):
 residual=ev-netdebt
 if residual<=claims(0):return 0.
 lo,hi=0.,200.
 for _ in range(120):
  mid=(lo+hi)/2
  if claims(mid)<residual:lo=mid
  else:hi=mid
 return (lo+hi)/2
# FCFF=(EBITDA - future SBC - integration cash costs)*(1-tax)+tax*physical depreciation-capex-deltaWC.
# Operating leases are expensed in EBITDA; financing leases are included in net debt. No double cash subtraction of operating leases.
def model(name, revenues, ebitdas, mult=10.,r=.10,extra=None):
 years=list(range(2027,2027+len(revenues)));extra=extra or [120,80,40,0]+[0]*max(0,len(years)-4)
 wc=0;rows=[];rev_prev=18500.
 for i,(year,rev,ebit) in enumerate(zip(years,revenues,ebitdas)):
  sbc=.0075*rev;dep=.015*rev;capex=.018*rev;dwc=.12*(rev-rev_prev);cashcost=extra[i]
  fcff=(ebit-sbc-cashcost)*.75+dep*.25-capex-dwc
  t=year-2026;pv=fcff/(1+r)**t;rows.append(dict(year=year,revenue=rev,ebitda=ebit,margin=ebit/rev,sbc=sbc,dep=dep,capex=capex,dwc=dwc,integration=cashcost,fcff=fcff,pv=pv));rev_prev=rev
 terminal=ebitdas[-1]*mult;terminalPV=terminal/(1+r)**len(years);ev=sum(x['pv'] for x in rows)+terminalPV;p=to_price(ev)
 return dict(name=name,rows=rows,r=r,multiple=mult,EV=ev,price=p,upside=p/price-1,terminal_pv=terminalPV,terminal_weight=terminalPV/ev)
scenarios=[model('既有业务延续',[18500,19000,19500,20000],[2100,2300,2500,2700]),model('整合目标兑现',[19500,21000,23000,25000],[2400,2900,3450,4000]),model('延迟两年且投入增加',[18500,19000,19800,21000,23000,25000],[2100,2250,2450,2700,3300,4000],extra=[180,160,120,100,60,0]),model('兑现但终值压至8倍',[19500,21000,23000,25000],[2400,2900,3450,4000],mult=8)]
# Solve 2030 EBITDA while holding revenue path and EBITDA ramp shape fixed.
def required(mult=10,r=.10):
 lo,hi=0.,10000.
 for _ in range(100):
  e=(lo+hi)/2;rr=model('反推',[19500,21000,23000,25000],[e*.60,e*.725,e*.8625,e],mult,r)
  if rr['EV']<claims(price)+netdebt:lo=e
  else:hi=e
 return (lo+hi)/2
sens=[{'r':r,'multiple':m,'required_2030_ebitda':required(m,r)} for r in [.08,.10,.12] for m in [8,10,12]]
res={'price':price,'price_date':'2026-11-16 16:00 EST','capital':capital,'net_debt_including_finance_leases':netdebt,'basic_marketcap':price*capital['common'],'basic_EV':price*capital['common']+capital['debt_principal']-capital['cash'],'economic_EV_required':claims(price)+netdebt,'claims_current':claims(price),'scenarios':scenarios,'required_2030_ebitda':required(),'sensitivity':sens}
(P/'valuation_results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
if __name__=='__main__':
 print(json.dumps({k:v for k,v in res.items() if k not in ['capital','scenarios','sensitivity']},indent=2))
 print([(x['name'],round(x['price'],2),round(x['EV']),round(x['terminal_weight'],3)) for x in scenarios]);print(sens)
