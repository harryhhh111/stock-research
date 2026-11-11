"""复算报告底表；仅依赖标准库，从脚本位置读取冻结输入。"""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
D=json.loads((P/'data/2026-10-29-inputs.json').read_text())
R={}
for y,x in D['years'].items():
 R[y]={'fcf':x['cfo']-x['capex'],'gross_margin':1-x['cost']/x['revenue'],'op_margin':x['op']/x['revenue'],'net_margin':x['net']/x['revenue'],'roe':x['net']/((x['equity']+x['begin_equity'])/2),'capex_revenue':x['capex']/x['revenue'],'capex_cfo':x['capex']/x['cfo']}
for k in ['q3_2025','q3_2026','ytd_2025','ytd_2026']:
 x=D[k];R[k]={'fcf':x['cfo']-x['capex'],'op_margin':x['op']/x['revenue'],'common_net_margin':x['common_net']/x['revenue'],'gross_margin':1-x['cost']/x['revenue']}
a,b=D['ytd_2025'],D['ytd_2026'];f=D['years']['2025']
ttm={k:f[k]+b[k]-a[k] for k in ['revenue','op','cfo','capex']}
ttm['common_net']=f['net']+b['common_net']-a['common_net'];ttm['fcf']=ttm['cfo']-ttm['capex'];ttm['eps']=10.81+16.33-7.99
R['ttm']=ttm
R['valuation']={}
for price in [321.89,290.54]:
 mc=price*12294
 R['valuation'][str(price)]={'common_market_cap_proxy':mc,'pe_ttm_eps':price/ttm['eps'],'pe_2025_eps':price/10.81,'fcf_yield':ttm['fcf']/mc,'pb_common':mc/(677549-18023),'ev_partial':mc+19000+125102-265098,'fcf_5y_needed_at_3pct':mc*.03,'fcf_growth_5y':(mc*.03/ttm['fcf'])**.2-1}
R['cloud_increment_share']=(30709-15157)/(127577-102346)
R['q3_op_bridge']={'services':39157-33527,'cloud':11121-3594,'bets':-2047+1426,'corporate':-7655+4467}
assert sum(R['q3_op_bridge'].values())==40576-31228
assert ttm['fcf']==19747
(P/'2026-10-29-计算结果.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
print(json.dumps(R,ensure_ascii=False,indent=2))
