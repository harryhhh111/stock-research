"""复算 RISC-V 专题底表。所有金额输入为千元，输出为百万元；路径相对脚本。"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
D = json.loads((ROOT/'data/financial-inputs.json').read_text())

def calc(r, prev=None):
    out = {k: (v/1000 if isinstance(v,(int,float)) else v) for k,v in r.items()}
    for k in ['gross','operating','net','rd']:
        if r.get(k) is not None: out[k+'_margin_pct']=r[k]/r['revenue']*100
    if prev and prev.get('revenue'):out['revenue_yoy_pct']=(r['revenue']/prev['revenue']-1)*100
    if all(r.get(k) is not None for k in ['cfo','ppe_cash','intangibles_cash']):
        out['cash_capex']=(r['ppe_cash']+r['intangibles_cash'])/1000
        out['fcf']=(r['cfo']-r['ppe_cash']-r['intangibles_cash'])/1000
        if r.get('other_nc_cash') is not None:out['fcf_after_other_nc_cash']=out['fcf']-r['other_nc_cash']/1000
    if r.get('equity_open') is not None:out['roe_pct']=r['net']/((r['equity_open']+r['equity'])/2)*100
    for k,v in r.get('segments',{}).items():
        out.setdefault('segment_metrics',{})[k]={'revenue_M':v/1000,'share_pct':v/r['revenue']*100,'yoy_pct':((v/prev['segments'][k]-1)*100 if prev and prev.get('segments',{}).get(k) else None)}
    return out
R={}
for company,periods in D.items():
 if company=='valuation':continue
 R[company]={}
 for period,row in periods.items():
  prev=periods.get(str(int(period)-1)) if period.isdigit() else periods.get(str(int(period[:4])-1)+period[4:])
  R[company][period]=calc(row,prev)
# 全部可加总项目按累计差分；EPS和加权股数不作差分。
a=D['andes'];base=a['2026H1'];q1=a['2026Q1'];
for period,hi,lo in [('2026Q2',base,q1),('2026Q3',a['20269M'],base),('2025Q4',a['2025'],a['20259M'])]:
 row={k:hi[k]-lo[k] for k in ['revenue','gross','operating','net','rd','selling','admin','credit_loss','cfo','ppe_cash','intangibles_cash','other_nc_cash'] if hi.get(k) is not None and lo.get(k) is not None}
 if hi.get('segments') and lo.get('segments'):row['segments']={k:hi['segments'][k]-lo['segments'][k] for k in hi['segments']}
 prev=a.get('2025'+period[4:]);R['andes'][period]=calc(row,prev)
 for k,v in row.items():
  if isinstance(v,(int,float)):assert abs(lo[k]+v-hi[k])<1e-6
for co,periods in D.items():
 if co=='valuation':continue
 for period,row in periods.items():
  if row.get('segments'):assert sum(row['segments'].values())==row['revenue'],(co,period)
# TTM：FY25 + 26YTD - 25YTD。财务指标各自用实际可取得的最新期间。
for co,ytd in [('andes','9M'),('eswin','Q1')]:
 t={k:D[co]['2025'][k]+D[co]['2026'+ytd][k]-D[co]['2025'+ytd][k] for k in ['revenue','gross','operating','net','cfo','ppe_cash','intangibles_cash'] if all(D[co][p].get(k) is not None for p in ['2025','2026'+ytd,'2025'+ytd])}
 R[co]['TTM_'+ytd]=calc(t)
# 最新可得现金流TTM仅截至H1，不能冒称截至Q3。
t={k:a['2025'][k]+a['2026H1'][k]-(a['2025Q1'][k]+a['2025Q2'][k]) for k in ['cfo','ppe_cash','intangibles_cash','other_nc_cash']}
R['andes']['cashflow_TTM_H1']={k:v/1000 for k,v in t.items()}
R['andes']['cashflow_TTM_H1']['fcf']=(t['cfo']-t['ppe_cash']-t['intangibles_cash'])/1000
v=D['valuation']; shares=v['andes_shares']; cap=v['andes_price']*shares/1e6
R['valuation']={'andes_marketcap_M_TWD':cap,'andes_ps_ttm':cap/R['andes']['TTM_9M']['revenue'],'andes_pb_sep_before_oct_raise':cap/(a['20269M']['equity']/1000),'andes_pb_proforma_raise':cap/((a['20269M']['equity']+1326000)/1000),'andes_new_shares_pct':6800000/50650911*100,'sifive_implied_new_money_pct':400/3650*100}
R['eswin']['2026Q1']['cfo_without_receivable_release_M']=(170557-363770-258922)/1000
# 异常检测不能等同原因已核实；费用桥先在原始千元口径勾稽。
bridges={}
bridge_inputs=dict(a)
bridge_inputs['2026Q2']={k:base[k]-q1[k] for k in ['revenue','gross','rd','selling','admin','credit_loss','operating']}
for period,row in bridge_inputs.items():
 if all(k in row for k in ['gross','rd','selling','admin','credit_loss','operating']):
  expenses=sum(row[k] for k in ['rd','selling','admin','credit_loss'])
  residual=row['gross']-expenses-row['operating']
  assert residual==0,(period,'毛利至经营利润桥未勾稽',residual)
  bridges[period]={'gross_M':row['gross']/1000,'rd_M':row['rd']/1000,'selling_M':row['selling']/1000,'admin_M':row['admin']/1000,'credit_loss_M':row['credit_loss']/1000,'total_expenses_M':expenses/1000,'expense_ratio_pct':expenses/row['revenue']*100,'operating_M':row['operating']/1000,'residual_thousand':residual}
flags=[]
for co,periods in R.items():
 if not isinstance(periods,dict):continue
 for period,row in periods.items():
  if not isinstance(row,dict) or 'gross' not in row or 'revenue' not in row:continue
  if row['gross']>row['revenue']:
   flags.append({'company':co,'period':period,'gross_margin_pct':row['gross_margin_pct'],'implied_cogs_M':row['revenue']-row['gross'],'status':'原因未核实；不据此推断定价权或盈利改善','next_evidence':'原始单季成本、同期重述及成本冲回附注'})
(ROOT/'anomaly-review.json').write_text(json.dumps({'expense_bridges':bridges,'unresolved_flags':flags,'note':'勾稽通过只证明输入算术一致；Q3输入为二手公告，未证明原始披露及经济原因。'},ensure_ascii=False,indent=2))
(ROOT/'calculation-results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
print('✅ 分部加总、累计拆季勾稽通过；利润率、ROE、FCF、TTM及适用估值已重算。')
print(json.dumps(R['valuation'],ensure_ascii=False,indent=2))
print('异常原因未核实项：',len(flags),'；详见anomaly-review.json。算术通过不等于成因核验通过。')
