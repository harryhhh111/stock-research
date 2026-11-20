from pathlib import Path
from html import escape as e
import json,re
P=Path(__file__).resolve().parent;ROOT=P.parent
D=json.loads((P/'financials.json').read_text());V=json.loads((P/'valuation_results.json').read_text())
A=D['annual'];Q=D['quarters'];R=D['products'];C=D['cumulative']
def num(v,n=1):return '—' if v is None else f'{v:,.{n}f}'
def pct(v,n=1):return num(v,n)+'%'
def table(head,rows,caption=''):
 return '<div class="table-wrap"><table><caption>'+caption+'</caption><thead><tr>'+''.join('<th>'+str(x)+'</th>' for x in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(('<th scope="row">' if i==0 else '<td>')+str(x)+('</th>' if i==0 else '</td>') for i,x in enumerate(row))+'</tr>' for row in rows)+'</tbody></table></div>'
def source(*ids):return '<p class="source">来源：'+ ' · '.join(f'<a href="#src-{i}">[{i}]</a>' for i in ids)+'；比例、同比和差分为复算。</p>'
def ratios(d):return [d['gross']/d['revenue']*100,d['op']/d['revenue']*100,d['net']/d['revenue']*100]
def financial_table(keys,data,title):
 rows=[]
 for label,m in [('营业收入','revenue'),('毛利','gross'),('经营利润','op'),('净利润（优先分配前）','net'),('经营现金流 CFO','cfo'),('现金购建资产 CapEx','capex'),('自由现金流 FCF=CFO−CapEx','fcf'),('股份支付费用 SBC','sbc')]:rows.append([label]+[num(data[k][m]) for k in keys])
 for i,label in enumerate(['毛利率','经营利润率','净利率']):rows.append([label]+[pct(ratios(data[k])[i]) for k in keys])
 return table(['指标']+keys,rows,title)
def product_table(keys,annual=False):
 names={'roof':'屋顶产品（住宅＋非住宅）','insulation':'保温材料与服务','complement':'配套建材（含已并表Kodiak）','software':'软件产品与服务'};rows=[]
 for m,label in names.items():
  row=[label]
  for k in keys:
   total=(A[k] if annual else Q[k])['revenue'];v=R[k][m]
   prev=str(int(k)-1) if annual else '2025'+k[4:]
   old=R.get(prev,{}).get(m)
   yoy='不适用：未并表' if v==0 else '无同口径基期' if old is None else '新增并表 / 零基数' if old==0 else '同比 '+pct((v/old-1)*100)
   if annual and k=='2023' and m=='software':yoy='同比 '+pct((v/44.985276-1)*100)
   row.append(f'{num(v)}<small>{yoy}<br>占集团 {pct(v/total*100)}</small>')
  rows.append(row)
 rows.append(['集团合计']+[num((A[k] if annual else Q[k])['revenue']) for k in keys])
 return table(['业务']+keys,rows,'QXO合并口径；M美元；每格依次为收入、同比、集团占比。零表示该业务未并表。')
# SVG charts use the same financial input as the exact tables.
colors=['#194e72','#38799b','#46a9a0','#b9babe']
def stacked():
 vals=[1996,1644,1240,15];names=['屋顶','保温与服务','配套建材','软件'];x=0;sh=[]
 for i,(v,name) in enumerate(zip(vals,names)):
  w=v/4895*900;sh.append(f'<rect x="{x}" y="10" width="{w}" height="44" fill="{colors[i]}"/>');x+=w
  sh.append(f'<text x="{i*225}" y="86" fill="{colors[i]}">{name} {v:,} / {v/4895:.1%}</text>')
 return '<svg viewBox="0 0 920 105" role="img" aria-label="2026Q3收入构成，屋顶40.8%，保温33.6%，配套25.3%，软件0.3%">'+''.join(sh)+'</svg>'
def waterfall(items,label):
 w=930;h=270;pad=42;bottom=211;xs=78;bw=58;gap=(w-xs-20)/len(items)
 current=0;steps=[];ext=[0]
 for name,v,total in items:
  start=0 if total else current;end=v if total else current+v
  steps.append((name,v,start,end,total));current=end;ext.extend([start,end])
 lo,hi=min(ext),max(ext);span=hi-lo or 1;scale=155/span;coord=lambda v:bottom-(v-lo)*scale
 svg=[f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><title>{label}</title><line x1="25" y1="{coord(0)}" x2="915" y2="{coord(0)}" stroke="#ccd3d7"/>']
 for i,(name,v,start,end,total) in enumerate(steps):
  x=xs+i*gap;y=min(coord(start),coord(end));height=abs(end-start)*scale
  col='#194e72' if total else '#388c77' if v>=0 else '#b7674f'
  svg.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{height}" fill="{col}"/>')
  if i<len(steps)-1:svg.append(f'<line x1="{x+bw}" y1="{coord(end)}" x2="{x+gap}" y2="{coord(end)}" stroke="#aab3b8"/>')
  val=end if total else v
  svg.append(f'<text x="{x+bw/2}" y="{max(20,y-8)}" text-anchor="middle">{num(val,0)}</text>')
  for j,line in enumerate(name.split('/')):svg.append(f'<text x="{x+bw/2}" y="{239+j*16}" text-anchor="middle">{e(line)}</text>')
 svg.append('</svg>');return ''.join(svg)
from flow_graphs import render as flow,metadata as flow_metadata
blocks={}
blocks['guidance-overview']=table(['性质 / 期间','指标与数值','如何理解'],[
 ['季度实绩 · 2026Q3','营业收入 '+num(Q['2026Q3']['revenue'],0),'同比 +79.4%；包含新增收购并表贡献'],
 ['季度实绩 · 2026Q3','净利润 '+num(Q['2026Q3']['net'],0)+'（亏损）','集团合并净亏损；优先股分配前，非普通股股东应占亏损'],
 ['季度实绩 · 2026Q3','调整后 EBITDA 557','同比 +85.0%；公司非GAAP口径，不等于净利润或现金流'],
 ['季度实绩 · 2026Q3','调整后 EPS（美元/股）<br>0.13','同比减少 0.01 美元/股（−7.1%）；公司非GAAP口径'],
 ['期后管理层披露 · 2026年10月','集团日销售同比 +5%；较早持有的屋顶及配套产品线增长9%','期后一个月、日均口径；不能当Q4完整增长，也不是所有产品销量增长'],
 ['管理层远期目标 · 2030年','现有业务调整后 EBITDA 4,000；额外小型并购机会最多再贡献约1,500','4,000已含整合、市场和效率假设；合计5,500还要求未来并购，不能无偿加入基准估值'],
 ['管理层收入愿景 · 十年内','年收入50,000','含并购；不是2027收入指引，不自动带来每股价值增长'],
 ['近季/全年量化指引','已查Q3业绩稿及10-Q：未列Q4或2026全年收入、GAAP净利润区间','不凭公司长期目标编造短期指引']
 ],'单位：金额为M美元（1 M美元＝100万美元）；EPS为美元/股，比例为%。披露核查截至2026-11-17；实绩、期后口径与目标分列。[5][6]').replace('<table>','<table class="narrative" id="guidance-overview">',1)
blocks['annual-products']=product_table(['2023','2024','2025'],True)+source(1,2,7)
blocks['quarter-products']=product_table(['2026Q1','2026Q2','2026Q3'])+source(3,4,5)
blocks['annual-finance']=financial_table(['2023','2024','2025'],A,'三完整财年；QXO合并；M美元，利润率除外。2024用2025年报比较列。')+source(1,2)
blocks['quarter-finance']=financial_table(['2025Q4','2026Q1','2026Q2','2026Q3'],Q,'单季度；单位：M美元，利润率为%。2025Q4为全年减9M；Q2/Q3现金流按累计拆季。')+source(2,3,4,5)
rows=[]
for key,label in [('revenue','营业收入'),('op','经营利润'),('net','净利润'),('cfo','CFO'),('capex','现金CapEx'),('fcf','FCF'),('sbc','SBC')]:
 row=[label]
 for q in [1,2,3]:
  d=Q[f'2026Q{q}'][key];old=Q[f'2025Q{q}'][key];prev=Q['2025Q4' if q==1 else f'2026Q{q-1}'][key]
  fmt=lambda a,b:'Δ '+num(a-b) if a<=0 or b<=0 or key!='revenue' else pct((a/b-1)*100)
  row.append(f'{num(old)} → {num(d)}<small>同比 {fmt(d,old)}；环比 {fmt(d,prev)}</small>')
 rows.append(row)
for i,label in enumerate(['毛利率','经营利润率','净利率']):
 row=[label]
 for q in [1,2,3]:
  r=ratios(Q[f'2026Q{q}'])[i];old=ratios(Q[f'2025Q{q}'])[i];prev=ratios(Q['2025Q4' if q==1 else f'2026Q{q-1}'])[i]
  row.append(f'{pct(old)} → {pct(r)}<small>同比 {num(r-old)}个百分点；环比 {num(r-prev)}个百分点</small>')
 rows.append(row)
blocks['quarter-compare']=table(['指标','Q1：2025→2026','Q2：2025→2026','Q3：2025→2026'],rows,'同比、环比；金额变化用Δ（M美元），跨零不报百分比。Q1环比基期2025Q4。')+source(2,3,4,5)
blocks['cumulative']=financial_table(['2025','2026'],C,'9M累计（各年1月1日—9月30日）；单位：M美元，利润率为%。')+source(5)
blocks['ttm']=financial_table(['2026-09 TTM'],{'2026-09 TTM':D['ttm']},'TTM：2025-10-01—2026-09-30；2025全年＋2026年9M−2025年9M；单位：M美元，利润率为%。')+source(2,5)
blocks['revenue-chart']=flow('income')+source(5)
blocks['income-flow-table']=table(['2026Q3收入来源','M美元','集团利润形成（不是产品费用分摊）','M美元'],[
 ['屋顶产品','1,996','销售成本','3,515'],['保温与服务','1,644','毛利＝收入−销售成本','1,380'],['配套建材','1,240','其中：销售管理费','1,024'],['软件与服务','15','其中：折旧','66'],['集团收入合计','4,895','其中：摊销','288'],['—','—','其中：经营利润','2']], '2026Q3 QXO合并，M美元；收入来源合计4895，毛利1380＝1024＋66＋288＋2，毛利及其拆分不重复加总。')+source(5)
blocks['cash-use-chart']=waterfall([('CFO',-145,True),('现金/CapEx',-111,False),('FCF',-256,True),('优先股/现金分配',-150,False),('分配后/现金缺口',-406,True)],'2026年9M，经营现金至自由现金及优先分配后缺口，M美元')+source(5)
blocks['profit-chart']=waterfall([('毛利',1380,True),('销售管理费',-1024,False),('折旧',-66,False),('摊销',-288,False),('经营利润',2,True),('净利息',-163,False),('其他收益',11,False),('税收收益',27,False),('净亏损',-123,True)],'2026Q3毛利至净亏损，M美元')+source(5)
blocks['cash-chart']=flow('cash')+source(5)
blocks['cash-flow-table']=table(['现金来源（含期初余额）','M美元','现金净用途及期末余额','M美元'],[
 ['期初含受限现金','2,366','并购净现金支付','10,933'],['新增借款（循环26＋定期2993＋债券3000）','6,019','经营活动净耗现','145'],['普通股净发行','748','现金CapEx','111'],['C优先股净发行','2,989','融资现金支出（下表）','386'],['股权奖励行权收入','3','期末含受限现金','554'],['其他投资净流入','4','—','—'],['合计','12,129','合计','12,129']], '2026年9M，M美元；集团净额口径，来源和用途分别加总，不是全部客户/供应商逐笔现金。')+source(5)
blocks['cash-financing-table']=table(['融资现金支出明细','M美元'],[[k,num(v,0)] for k,v in flow_metadata['financing_cash_paid'].items()]+[['合计',num(sum(flow_metadata['financing_cash_paid'].values()),0)]],'融资现金支出386的互斥明细；2026年9M，M美元。')+source(5)
rows=[]
for y,d in A.items():rows.append([y,num(d['assets']),num(d['equity']),num(d['cash']),num(d['roe'],2)+'%'])
rows.append(['2026-09-30','34,470.0','15,681.0','528.0','9M简单年化 −4.25%（见口径）'])
blocks['balance']=table(['期末','总资产','股东权益（含A/B，不含C）','非受限现金','总权益ROE'],rows,'单位：金额为M美元，ROE为%；历史ROE=净利润/平均总股东权益；有大额期中融资，经济解释力有限。')+source(1,2,5)
rows=[]
for y in ['2023','2024','2025']:
 d=A[y];dv={'2023':(1.051,0),'2024':(17.4,32.3),'2025':(0,104.8)}[y]
 rows.append([y,num(d['capex']),num(d['fcf']),num(dv[0]),num(dv[1]),'0（未发现常规回购）',num(10556.5 if y=='2025' else 0),{'2023':'0.664448','2024':'409.4','2025':'674.5'}[y]])
rows.append(['2026年9M','111.0','−256.0','0.0','150.0','0（期后仅有授权）','10,933.0','1,039.8'])
blocks['capital-allocation']=table(['期间','现金CapEx','FCF','普通股现金股息','优先股现金分配','普通股回购','并购净现金支付','期末普通股（百万股）'],rows,'现金资本分配；单位：金额为M美元，期末普通股为百万股。并购已扣取得现金，未把股票对价当现金。2023无业务收购现金，另有资产收购0.279。')+source(1,2,5)
rows=[]
for s in V['scenarios']:
 last=s['rows'][-1];rows.append([s['name'],str(last['year']),num(last['revenue']),num(last['ebitda']),pct(last['margin']*100),f"{s['multiple']:.0f}× / {s['r']:.0%}",f"${s['price']:.2f}",pct(s['upside']*100),pct(s['terminal_weight']*100)])
blocks['scenarios']=table(['【我的推演】','目标年','收入','调整后EBITDA','对应利润率','终值倍数/折现率','每股现值（美元/股）','相对$12.01','终值现值占比'],rows,'单位：收入与调整后EBITDA为M美元，每股现值为美元/股，倍数为倍，比例为%。条件估值；现金流与终值均折现，资本结构按下述内在价值近似。不是预测或目标价。')
rows=[]
for r in [.08,.10,.12]:rows.append([pct(r*100)]+[num(next(x['required_2030_ebitda'] for x in V['sensitivity'] if x['r']==r and x['multiple']==m)) for m in [8,10,12]])
blocks['sensitivity']=table(['折现率 / 2030终值倍数','8倍','10倍','12倍'],rows,'支撑$12.01所需2030年调整后EBITDA（M美元）；固定收入路径及EBITDA爬坡比例，其余输入见模型。')
rows=[]
for s in V['scenarios']:
 for x in s['rows']:rows.append([s['name'],x['year'],num(x['revenue']),num(x['ebitda']),num(x['sbc']),num(x['integration']),num(x['dep']),num(x['capex']),num(x['dwc']),num(x['fcff']),num(x['pv'])])
blocks['forecast-inputs']=table(['路径','财年','收入','EBITDA','SBC经济成本','整合现金费','实物折旧','现金CapEx','新增营运资金','企业现金流','折现值'],rows,'【我的推演】全部为M美元；分路径逐年输入与输出。保留负营运资金变动，表示释放现金。')
rows=[['仅普通股市值',num(V['basic_marketcap'])],['简式EV=普通股市值＋债务本金−现金',num(V['basic_EV'])],['经济索取权口径EV（含融资租赁）',num(V['economic_EV_required'])],['调整后的净债务（含融资租赁）',num(V['net_debt_including_finance_leases'])],['支撑现价所需2030调整后EBITDA（10倍、10%）',num(V['required_2030_ebitda'])]]
blocks['valuation-snapshot']=table(['指标','M美元'],rows,'单位：表内金额为M美元；股价为美元/股，股数为百万股。行情2026-11-16常规收盘$12.01；普通股1,039.958653百万股，截至2026-11-06；资产负债截至2026-09-30。')+source(5,8)
AUD=json.loads((P/'sop_audit.json').read_text())
auditrows=[]
for x in AUD['items']:
 links=' · '.join(f'<a href="#{a}">{a}</a>' for a in x['evidence'])
 auditrows.append([x['id'],e(x['requirement']),e(x['result']),links+'<small>'+e(x['review'])+'</small>'])
counts=AUD['summary']
blocks['sop-audit']='<div id="sop-review"><p><b>逐项内容验收：</b>'+f"共{counts['total']}项；通过{counts['passed']}项，未通过{counts['failed']}项，不适用{counts['not_applicable']}项，待复核{counts['pending']}项。"+'这些是按正文证据作出的审阅判断，不是由算术测试数推导。<a href="factcheck/sop_audit.json">逐项记录JSON</a>。</p>'+table(['编号','SOP要求','本轮结果','证据位置 / 实质判断'],auditrows,'完整研究验收逐项映射；2026-11-17内容结论沿用；2026-11-18复核单位与混合量纲，保留原未通过项。').replace('<table>','<table class="audit-table">',1)+'</div>'
blocks['coverage-matrix']='<div id="coverage-review">'+table(['指标组 / 主体','预期单季','实际单季','同比及环比基期','来源 / 拆季','结果及边界'],[
 ['集团及已披露主要产品收入','2026Q1/Q2/Q3','1730.2 / 3246 / 4895；四条产品线逐季列示','2025各同季；Q1环比2025Q4','[3][4][5]主表及产品线附注','覆盖通过；并表范围不可比，跨版本差异原因另列未通过'],
 ['集团经营利润、净利和利润率','2026Q1/Q2/Q3','经营−251.9 / −42 / 2；净利−227.1 / −55 / −123；各利润率已复算','2025各同季；Q1环比2025Q4','[2]全年减[5]2025年9M得Q4，[3—5]当年单季','覆盖及算术通过；2025比较列税项与版本成因未通过'],
 ['集团CFO / 现金CapEx / FCF','2026Q1/Q2/Q3','CFO70.6 / −216.6 / 1；CapEx22.5 / 31.5 / 57；FCF48.1 / −248.1 / −56','2025各同季；Q1环比2025Q4','Q1原表，Q2=H1−Q1；Q3=9M−H1；拆季见financials.json','覆盖通过；原始精度不同，容差不当成因证据'],
 ['集团SBC','2026Q1/Q2/Q3','39.2 / 28.8 / 79','2025各同季；Q1环比2025Q4','[3—5]；Q2按累计差分保留来源精度','覆盖通过；未把费用金额当发行股数'],
 ['产品线经营利润 / CFO / CapEx','同期间披露范围','集团仅一个报告分部；未单列四条产品的独立三表','不伪造同比 / 环比','[2—5]分部附注；收购贡献另列','公司未披露：以集团三表与收购后贡献说明，不按收入分摊']
 ],'季度覆盖与成因确认分开；金额M美元，利润率在正文精确表。')+'</div>'
html=(ROOT/'QXO.html').read_text()
for key,value in blocks.items():
 pattern=r'<!-- BEGIN:'+re.escape(key)+r' -->.*?<!-- END:'+re.escape(key)+r' -->'
 assert re.search(pattern,html,re.S),key
 html=re.sub(pattern,lambda _:f'<!-- BEGIN:{key} -->\n{value}\n<!-- END:{key} -->',html,flags=re.S)
(ROOT/'QXO.html').write_text(html)
print('Updated',len(blocks),'data/chart blocks')
