"""Recalculate S-1 financials from preserved original table extraction; no network required."""
from pathlib import Path
import json, re, hashlib
BASE = Path(__file__).resolve().parent
src = json.loads((BASE/'data/2026-10-26-S1-extract.json').read_text())
def numbers(table, label):
    rows = src['tables'][table]['rows']
    row = next(r for r in rows if r[0] == label)
    vals=[]
    for cell in row[1:]:
        t=re.sub(r'[$,%\s,]','',cell)
        if t in ('—','–','-'): vals.append(0.)
        elif re.fullmatch(r'\(?-?\d+(?:\.\d+)?\)?',t):
            vals.append(-float(t[1:-1]) if t.startswith('(') else float(t))
    return vals
rev=numbers('income','Revenue');op=numbers('income','Operating loss');net=numbers('income','Net loss')
cfo=numbers('cashflow','Net cash provided by (used in) operating activities');capex=[-x for x in numbers('cashflow','Purchases of property and equipment')]
cost=numbers('functional_costs','Cost of revenue (1)');rd=numbers('functional_costs','Research and development (2)')
cons=numbers('revenue_type','Consumption-based');sub=numbers('revenue_type','Subscription-based')
geo=numbers('geography','United States');compute=numbers('income','Compute and infrastructure')
assert len(rev)==5
assert all(abs(a+b-c)<.01 for a,b,c in zip(cons,sub,rev))
assert hashlib.sha256((BASE/'data/2026-10-26-S1.html').read_bytes()).hexdigest()==src['sha256']
periods=['2023','2024','2025','H1 2025','H1 2026']
out={'unit':'USD million','source':src['source'],'source_sha256':src['sha256'],'periods':{}}
lines=['# Anthropic 财务复算结果','', '核对日期：2026-10-29；单位：百万美元；原值来自保留的 S-1 表格提取。','', '|期间|收入|同比 %|毛利率 %|经营利润率 %|净利率 %|CFO|现金CapEx|简化FCF|用量收入占比 %|美国占比 %|算力费用/收入 %|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for i,p in enumerate(periods):
    prev={1:0,2:1,4:3}.get(i)
    d={'revenue':rev[i],'yoy_pct':None if prev is None else (rev[i]/rev[prev]-1)*100,'gross_profit':rev[i]-cost[i],'gross_margin_pct':(rev[i]-cost[i])/rev[i]*100,'operating_margin_pct':op[i]/rev[i]*100,'net_margin_pct':net[i]/rev[i]*100,'cfo':cfo[i],'cash_capex':capex[i],'simple_fcf':cfo[i]-capex[i],'consumption_share_pct':cons[i]/rev[i]*100,'us_share_pct':geo[i]/rev[i]*100,'compute_share_pct':compute[i]/rev[i]*100,'rd_share_pct':rd[i]/rev[i]*100}
    out['periods'][p]=d
    vals=[p,rev[i],d['yoy_pct'],d['gross_margin_pct'],d['operating_margin_pct'],d['net_margin_pct'],cfo[i],capex[i],d['simple_fcf'],d['consumption_share_pct'],d['us_share_pct'],d['compute_share_pct']]
    lines.append('|'+ '|'.join('不适用' if v is None else f'{v:,.2f}' if isinstance(v,(int,float)) else v for v in vals)+'|')
q=numbers('quarterly','Revenue');out['quarterly']={'revenues':q,'q2_2026_yoy_pct':(q[-1]/q[1]-1)*100,'q2_2026_qoq_pct':(q[-1]/q[-2]-1)*100,'q3_2026_media_revenue':16800,'q3_qoq_pct':(16800/q[-1]-1)*100,'ttm_through_q3_media':sum(q[-3:])+16800}
commitments={'Broadcom':161200,'Google':114500,'Amazon':110000,'Microsoft':44900,'SpaceXAI':120500,'Nscale':44600,'Lambda':41300}
out['named_contracts_mixed_basis']=commitments;out['named_contracts_sum_not_rigid_debt']=sum(commitments.values())
ttm=out['quarterly']['ttm_through_q3_media'];out['valuation']={}
for equity in [1500000,2000000]:
 out['valuation'][str(equity)]={'PS_2025':equity/rev[2],'PS_H1_annualized':equity/(rev[4]*2),'PS_Q3_annualized':equity/(16800*4),'PS_TTM':equity/ttm,'PS_2028_190bn':equity/190000,'PS_2028_200bn':equity/200000,'fcf_yield_H1_annualized_pct':((cfo[4]-capex[4])*2)/equity*100,'required_2028_fcf_at35x_12pct_2yrs':equity*1.12**2/35}
scenarios=[]
for name,r,m in [('压力',100000,.05),('基准',150000,.15),('乐观',200000,.25)]:
 f=r*m;scenarios.append({'name':name,'revenue_2028':r,'fcf_margin':m,'fcf':f,'terminal_equity_35x':f*35,'present_equity_discount12pct_2yrs':f*35/1.12**2})
out['scenarios']=scenarios
out['additional_checks']={
 'consumption_yoy_pct':[(cons[1]/cons[0]-1)*100,(cons[2]/cons[1]-1)*100,(cons[4]/cons[3]-1)*100],
 'subscription_yoy_pct':[(sub[1]/sub[0]-1)*100,(sub[2]/sub[1]-1)*100,(sub[4]/sub[3]-1)*100],
 'geography_H1_yoy_pct':{'US':(11763/820-1)*100,'international':(4523/343-1)*100},
 'q1_2026_yoy_pct':(4731/376-1)*100,'q3_media_yoy_pct':(16800/1382-1)*100,
 'q2_operating_margin_pct':974/11555*100,'qoq_increment_q2':11555-4731,'qoq_increment_q3':16800-11555,
 'H1_net_loss_bridge':-693+1111-72388-8757-21,'H1_adjusted_op_bridge':-693+2185+126,
 'H1_working_capital_bridge':-4982+2094+2679-3+1380,
 'capex_yoy_pct':[(15/2-1)*100,(131/15-1)*100,(482/18-1)*100],
 'ClassA_share_growth_pct':[(1901267/1779060-1)*100,(2157398/1901267-1)*100],
 'mechanical_ROE_not_economic_pct':{'2025':-41965/((-9801-50505)/2)*100,'H1_2026_not_annualized':-80748/((-50505-127619)/2)*100},
 'fixed_cost_20pct_revenue_stress_op':16286*.8-16979,
 'required_fcf_margin_pct_at200bn_revenue':{str(e):v['required_2028_fcf_at35x_12pct_2yrs']/200000*100 for e,v in out['valuation'].items()}}
lines+=['','## 其他复算' ,'', '```json',json.dumps({k:v for k,v in out.items() if k not in ['periods','source_sha256']},ensure_ascii=False,indent=2),'```','', '✅ 收入模式加总、原文件校验和通过；同比、占比、利润率、简化 FCF 与估值已复算。','简化 FCF 不扣未来采购承诺，不代表已覆盖融资租赁本金、未来租赁爬坡和所有扩张现金支出。ROE/PB 因普通股权益为负不作经济回报判断；ROIC 因历史资本结构和投入资本重分类不足不生成伪精确值。']
(BASE/'核验结果.md').write_text('\n'.join(lines)+'\n')
(BASE/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2))
