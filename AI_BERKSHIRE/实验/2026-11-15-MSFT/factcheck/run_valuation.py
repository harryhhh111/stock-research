from pathlib import Path
import importlib.util,json,subprocess,sys,contextlib,io
P=Path(__file__).resolve().parent
R=P.parents[2]/'repo'/'tools'
def load(n):
 s=importlib.util.spec_from_file_location(n,R/(n+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
f=load('financial_rigor');t=load('terminal_value');a=load('report_audit')
log=io.StringIO()
price=523.88;shares=7427;cap=price*shares;eps=18.04
with contextlib.redirect_stdout(log):
 f.verify_market_cap(price,shares*1e6,3.89e12,'USD')
 for field,official,sa in [('FY26收入',331839,331839),('FY26净利润GAAP',133749,133749),('FY26现金短投',76843,76843),('Q1期末现金短投',64509,64509),('期末实股百万',7427,7430)]:f.cross_validate(field,{'Microsoft官方':official,'StockAnalysis':sa},'百万',1)
 ratios=f.verify_valuation(price,eps=eps,bvps=470509/shares,fcf_per_share=59957/shares,revenue_per_share=346445/shares)
 f.three_scenario_valuation(price,eps,shares/1000,.18,.12,.06,30,25,20,3,'USD')
rows=[]
for name,g,pe in [('悲观',.06,20),('基准',.12,25),('乐观',.18,30)]:
 future=eps*(1+g)**3;pv=future*pe/1.1**3+sum(3.92/1.1**y for y in range(1,4))
 rows.append(dict(name=name,growth=g,pe=pe,eps=future,future_price=future*pe,present_value=pv,vs_price=pv/price-1))
# Three-year model ending 2029-11-13; FY2030 is nearest full FY proxy. Cash dividends held flat, no repurchase counted as a second cash return.
reverse={str(pe):((price-sum(3.92/1.1**y for y in range(1,4)))*1.1**3/(eps*pe))**(1/3)-1 for pe in [20,25,30]}
delayed=eps*1.12**2*25/1.1**3+sum(3.92/1.1**y for y in range(1,4))
compression=eps*1.12**3*20/1.1**3+sum(3.92/1.1**y for y in range(1,4))
# Stable debt/equity per share and normalized profit growth assumptions; k=.7% is illustrative net cash yield, not measured dividend minus dilution forecast.
spec={'roic':.25,'g':[.02,.03,.04],'p':[.25,.5,.25],'irr10':[],'k':.007}
for growth,g in zip([.06,.12,.18],spec['g']):
 pe=t.exit_pe(.25,g,.10)[0];profit=134375*(1+growth)**10
 spec['irr10'].append(t.irr_from_terminal(profit,cap,pe,10,.007)*100)
(P/'terminal-config.json').write_text(json.dumps({'MSFT':spec},indent=2))
def call(tool,args):
 proc=subprocess.run([sys.executable,str(R/(tool+'.py'))]+list(map(str,args)),text=True,capture_output=True)
 log.write('\nCOMMAND '+tool+' '+' '.join(map(str,args))+'\n'+proc.stdout+proc.stderr+'\nEXIT '+str(proc.returncode)+'\n');return proc.returncode
args=['audit','--currency','USD','--r',.10,'--roic',.25,'--g','.02,.03,.04','--beta',1,'--discrete-risks','AI投资回报不及预期:情景,反垄断拆分:未建模,重大安全事故:未建模']
call('terminal_value',args)
for growth,g in zip([.06,.12,.18],spec['g']):
 pe=t.exit_pe(.25,g,.10)[0];call('terminal_value',['pe','--roic',.25,'--g',g,'--r',.10]);call('terminal_value',['irr','--profit',134375*(1+growth)**10,'--mcap',cap,'--pe',pe,'--years',10,'--payout',.007])
for delta in [.02,.01]:call('terminal_value',['flip','--config',P/'terminal-config.json','--name','MSFT','--r',.10,'--delta',delta,'--currency','USD'])
call('terminal_value',args)
sens=[]
for r in [.08,.09,.10,.11,.12]:
 rr=t.evaluate(spec,r);mean=t.weighted_stats([x['irr'] for x in rr],spec['p'])[0];sens.append(dict(r=r,mean_irr=mean,rows=rr,within_repo_band=.09<=r<=.115))
summary=dict(price=price,shares_million=shares,mcap_million=cap,adjusted_eps_ttm=eps,adjusted_pe=price/eps,gaap_pe=price/19.15,fcf_yield=59957/cap,ratios=ratios,scenarios=rows,reverse_growth=reverse,delayed_present_value=delayed,compressed_present_value=compression,delayed_extra_cost_present_value=delayed-25/1.1**3,dividend_assumption=3.92,dividend_source='https://news.microsoft.com/source/2026/09/15/microsoft-announces-quarterly-dividend-increase-7/',fy2026_roe_gaap=133749/((343479+442387)/2),fy2026_roe_adjusted=128786/((343479+442387)/2),ttm_roe_gaap=142631/((363076+470509)/2),ttm_roe_adjusted=134375/((363076+470509)/2),terminal_spec=spec,sensitivity=sens,limitations=['Adjusted TTM EPS18.04 excludes OpenAI investment effects only, NOT fully normalized operating EPS. FY26Q4 includes Anthropic investment gains3.2bn pretax plus other one-offs not separately removed; forecast base may be overstated. Uses rounded quarterly EPS; net income TTM134375 separately reconciled.','Terminal IRR is repo approximate geometric return plus fixed net yield, not exact dated cash flow IRR.','Probabilities .25/.5/.25 are illustrative researcher weights, not calibrated odds.','r10% is researcher hurdle. No contemporaneous risk-free rate fetched; repo built-in USD4.7% is stale Aug2026 assumption, not present market rate.','Current stock count from Sep30 vs Nov13 price; 3.89T market cap and7.43B shares are third-party rounded figures.','ROE displayed by tool EPS/BVPS uses closing equity; it is not standard average-equity ROE and should not be reported as such.'])
(P/'valuation-results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
(P/'valuation-tool-log.txt').write_text(log.getvalue())
print(json.dumps(summary,ensure_ascii=False,indent=2))
