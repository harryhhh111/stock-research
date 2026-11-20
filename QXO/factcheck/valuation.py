"""Conditional enterprise valuation, MUSD and millions of shares; no forecast is consensus."""
from pathlib import Path
import argparse
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
def model(name, revenues, ebitdas, mult=10.,r=.10,extra=None,*,benchmark=price):
 years=list(range(2027,2027+len(revenues)));extra=extra or [120,80,40,0]+[0]*max(0,len(years)-4)
 wc=0;rows=[];rev_prev=18500.
 for i,(year,rev,ebit) in enumerate(zip(years,revenues,ebitdas)):
  sbc=.0075*rev;dep=.015*rev;capex=.018*rev;dwc=.12*(rev-rev_prev);cashcost=extra[i]
  fcff=(ebit-sbc-cashcost)*.75+dep*.25-capex-dwc
  t=year-2026;pv=fcff/(1+r)**t;rows.append(dict(year=year,revenue=rev,ebitda=ebit,margin=ebit/rev,sbc=sbc,dep=dep,capex=capex,dwc=dwc,integration=cashcost,fcff=fcff,pv=pv));rev_prev=rev
 terminal=ebitdas[-1]*mult;terminalPV=terminal/(1+r)**len(years);ev=sum(x['pv'] for x in rows)+terminalPV;p=to_price(ev)
 return dict(name=name,rows=rows,r=r,multiple=mult,EV=ev,price=p,upside=p/benchmark-1,terminal_pv=terminalPV,terminal_weight=terminalPV/ev)
scenarios=[model('既有业务延续',[18500,19000,19500,20000],[2100,2300,2500,2700]),model('整合目标兑现',[19500,21000,23000,25000],[2400,2900,3450,4000]),model('延迟两年且投入增加',[18500,19000,19800,21000,23000,25000],[2100,2250,2450,2700,3300,4000],extra=[180,160,120,100,60,0]),model('兑现但终值压至8倍',[19500,21000,23000,25000],[2400,2900,3450,4000],mult=8)]
# Solve 2030 EBITDA while holding revenue path and EBITDA ramp shape fixed.
def required(mult=10,r=.10,*,benchmark=price):
 lo,hi=0.,10000.
 for _ in range(100):
  e=(lo+hi)/2;rr=model('反推',[19500,21000,23000,25000],[e*.60,e*.725,e*.8625,e],mult,r)
  if rr['EV']<claims(benchmark)+netdebt:lo=e
  else:hi=e
 return (lo+hi)/2
def results(benchmark, benchmark_date):
    updated_scenarios = [
        {**scenario, 'upside': scenario['price'] / benchmark - 1}
        for scenario in scenarios
    ]
    sensitivity = [
        {'r': rate, 'multiple': multiple, 'required_2030_ebitda': required(multiple, rate, benchmark=benchmark)}
        for rate in [.08, .10, .12] for multiple in [8, 10, 12]
    ]
    return {
        'price': benchmark, 'price_date': benchmark_date, 'capital': capital,
        'net_debt_including_finance_leases': netdebt,
        'basic_marketcap': benchmark * capital['common'],
        'basic_EV': benchmark * capital['common'] + capital['debt_principal'] - capital['cash'],
        'economic_EV_required': claims(benchmark) + netdebt,
        'claims_current': claims(benchmark), 'scenarios': updated_scenarios,
        'required_2030_ebitda': required(benchmark=benchmark), 'sensitivity': sensitivity
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--price', type=float, required=True)
    parser.add_argument('--price-date', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.price <= 0:
        parser.error('price must be positive')
    result = results(args.price, args.price_date)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"Required 2030 EBITDA: {result['required_2030_ebitda']:.1f} MUSD")
